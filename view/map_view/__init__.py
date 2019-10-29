from logging import getLogger
from time import perf_counter
from math import ceil

from view import *
from database import CONFIG_DB_CURSOR
from ui.button import create_two_state_button
from ui.button.zoom_in_button import ZoomInButton
from ui.button.zoom_out_button import ZoomOutButton
from ui.button.open_schedule_button import OpenScheduleButton
from ui.button.open_constructor_button import OpenConstructorButton
from ui.button.open_shop_details_button import OpenShopDetailsButton
from ui.shader_sprite.map_view_shader_sprite import MapViewShaderSprite
from ui.sprite.main_map_sprite import MainMapSprite
from ui.sprite.main_environment_sprite import MainEnvironmentSprite
from ui.sprite.mini_map_sprite import MiniMapSprite
from ui.sprite.mini_environment_sprite import MiniEnvironmentSprite


class MapView(MapBaseView):
    def __init__(self, controller, map_id):
        def on_click_zoom_in_button(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate(instant=True)
            self.controller.on_zoom_in()

        def on_click_zoom_out_button(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate(instant=True)
            self.controller.on_zoom_out()

        def on_leave_action():
            self.on_map_move_mode_available()

        def on_hover_action():
            self.on_map_move_mode_unavailable()

        def on_open_schedule(button):
            button.on_deactivate(instant=True)
            button.state = 'normal'
            self.controller.on_open_schedule()

        def on_open_constructor(button):
            button.on_deactivate(instant=True)
            button.state = 'normal'
            self.controller.on_open_constructor()

        def on_open_shop_details(button):
            self.controller.on_open_shop_details(self.shop_buttons.index(button))

        super().__init__(controller, logger=getLogger(f'root.app.game.map.{map_id}.view'))
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        self.mini_map_offset = (0, 0)
        self.main_map_sprite = MainMapSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.environment_sprite = MainEnvironmentSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.mini_map_sprite = MiniMapSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.mini_environment_sprite = MiniEnvironmentSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.is_mini_map_activated = False
        self.mini_map_timer = 0.0
        self.mini_map_opacity = 0
        self.mini_map_frame_position = (0, 0)
        self.mini_map_frame_width = 0
        self.mini_map_frame_height = 0
        self.base_offset_lower_left_limit = (0, 0)
        self.base_offset_upper_right_limit = (0, 0)
        self.zoom_in_button, self.zoom_out_button \
            = create_two_state_button(ZoomInButton(on_click_action=on_click_zoom_in_button,
                                                   on_hover_action=on_hover_action, on_leave_action=on_leave_action,
                                                   parent_viewport=self.viewport),
                                      ZoomOutButton(on_click_action=on_click_zoom_out_button,
                                                    on_hover_action=on_hover_action, on_leave_action=on_leave_action,
                                                    parent_viewport=self.viewport))
        self.open_schedule_button = OpenScheduleButton(on_click_action=on_open_schedule, parent_viewport=self.viewport)
        self.open_constructor_button = OpenConstructorButton(on_click_action=on_open_constructor,
                                                             parent_viewport=self.viewport)
        self.buttons = [self.zoom_in_button, self.zoom_out_button, self.open_schedule_button,
                        self.open_constructor_button]
        self.shop_buttons = []
        self.shops_track_required_state = []
        self.shop_buttons_offsets = []
        CONFIG_DB_CURSOR.execute('''SELECT COUNT(*) FROM shops_config WHERE map_id = ?''', (self.map_id, ))
        for shop_id in range(CONFIG_DB_CURSOR.fetchone()[0]):
            self.shop_buttons.append(OpenShopDetailsButton(map_id=self.map_id, shop_id=shop_id,
                                                           on_click_action=on_open_shop_details,
                                                           on_hover_action=on_hover_action,
                                                           on_leave_action=on_leave_action))
            CONFIG_DB_CURSOR.execute('''SELECT track_required FROM shops_config 
                                        WHERE map_id = ? AND shop_id = ?''', (self.map_id, shop_id))
            self.shops_track_required_state.append(CONFIG_DB_CURSOR.fetchone()[0])
            CONFIG_DB_CURSOR.execute('''SELECT button_x, button_y FROM shops_config 
                                        WHERE map_id = ? AND shop_id = ?''', (self.map_id, shop_id))
            self.shop_buttons_offsets.append(CONFIG_DB_CURSOR.fetchone())

        self.buttons.extend(self.shop_buttons)
        for b in self.shop_buttons:
            b.on_change_base_offset(self.base_offset)
            b.on_change_scale(self.zoom_factor)

        self.map_move_mode_available = False
        self.map_move_mode = False
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)
        self.shader_sprite = MapViewShaderSprite(view=self)
        USER_DB_CURSOR.execute('''SELECT SUM(t.constructions_locked) FROM (
                                      SELECT COUNT(track_number) AS constructions_locked FROM tracks 
                                      WHERE locked = 1 AND map_id = ?
                                      UNION
                                      SELECT COUNT(tier) AS constructions_locked FROM environment 
                                      WHERE locked = 1 AND map_id = ?
                                  ) AS t''', (self.map_id, self.map_id))
        self.constructions_locked = USER_DB_CURSOR.fetchone()[0]

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.map_move_mode_available = True
        self.shader_sprite.create()
        self.main_map_sprite.create()
        self.environment_sprite.create()
        if self.zoom_out_activated:
            self.zoom_in_button.on_activate()
        else:
            self.zoom_out_button.on_activate()

        self.on_activate_open_constructor_button()
        self.on_activate_shop_buttons()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.is_mini_map_activated = False

    @final
    def on_update(self):
        cpu_time = perf_counter()
        if self.is_mini_map_activated and not self.map_move_mode \
                and cpu_time - self.mini_map_timer > MINI_MAP_FADE_OUT_TIMER:
            self.is_mini_map_activated = False

        self.on_update_mini_map_opacity()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.mini_map_sprite.on_change_screen_resolution(self.screen_resolution)
        self.mini_environment_sprite.on_change_screen_resolution(self.screen_resolution)
        self.base_offset_lower_left_limit = (self.viewport.x1,
                                             self.viewport.y1 + get_bottom_bar_height(self.screen_resolution))
        self.base_offset_upper_right_limit = (self.viewport.x2 - MAP_WIDTH // round(1 / self.zoom_factor),
                                              self.viewport.y2 - MAP_HEIGHT // round(1 / self.zoom_factor)
                                              - get_top_bar_height(self.screen_resolution))
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.mini_map_frame_width = self.get_mini_map_frame_width()
        self.mini_map_frame_height = self.get_mini_map_frame_height()
        self.mini_map_frame_position = self.get_mini_map_frame_position()
        self.zoom_in_button.on_change_screen_resolution(self.screen_resolution)
        self.zoom_out_button.on_change_screen_resolution(self.screen_resolution)
        self.open_schedule_button.on_change_screen_resolution(self.screen_resolution)
        self.open_constructor_button.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.main_map_sprite.on_update_opacity(self.opacity)
        self.environment_sprite.on_update_opacity(self.opacity)

    @final
    def on_change_base_offset(self, new_base_offset):
        super().on_change_base_offset(new_base_offset)
        self.main_map_sprite.on_change_base_offset(self.base_offset)
        self.environment_sprite.on_change_base_offset(self.base_offset)
        for b in self.shop_buttons:
            b.on_change_base_offset(self.base_offset)

    @final
    def on_change_scale(self, zoom_factor):
        super().on_change_scale(zoom_factor)
        self.main_map_sprite.on_change_scale(self.zoom_factor)
        self.environment_sprite.on_change_scale(self.zoom_factor)
        self.base_offset_upper_right_limit = (self.viewport.x2 - MAP_WIDTH // round(1 / self.zoom_factor),
                                              self.viewport.y2 - MAP_HEIGHT // round(1 / self.zoom_factor)
                                              - get_top_bar_height(self.screen_resolution))
        if self.zoom_out_activated:
            self.base_offset = (self.base_offset[0] // 2
                                + (self.viewport.x2 - self.viewport.x1) // 4,
                                self.base_offset[1] // 2
                                + (self.viewport.y2 - self.viewport.y1) // 4)
        else:
            self.base_offset = (2 * self.base_offset[0] - (self.viewport.x2 - self.viewport.x1) // 2,
                                2 * self.base_offset[1] - (self.viewport.y2 - self.viewport.y1) // 2)

        self.check_base_offset_limits()
        self.mini_map_frame_width = self.get_mini_map_frame_width()
        self.mini_map_frame_height = self.get_mini_map_frame_height()
        self.mini_map_frame_position = self.get_mini_map_frame_position()
        for b in self.shop_buttons:
            b.on_change_scale(self.zoom_factor)

        self.controller.on_save_and_commit_last_known_base_offset(self.base_offset)

    @final
    @mini_map_is_not_active
    def on_activate_mini_map(self):
        self.is_mini_map_activated = True
        self.mini_environment_sprite.create()
        self.mini_map_sprite.create()

    @final
    def on_update_mini_map_opacity(self):
        if self.is_mini_map_activated and self.mini_map_opacity < 255:
            self.mini_map_opacity += 17

        if not self.is_mini_map_activated and self.mini_map_opacity > 0:
            self.mini_map_opacity -= 17

        self.mini_map_sprite.on_update_opacity(self.mini_map_opacity)
        self.mini_environment_sprite.on_update_opacity(self.mini_map_opacity)

    @final
    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        self.main_map_sprite.on_unlock_track(self.unlocked_tracks)
        self.mini_map_sprite.on_unlock_track(self.unlocked_tracks)

    @final
    def on_unlock_environment(self, tier):
        self.environment_sprite.on_unlock_environment(tier)
        self.mini_environment_sprite.on_unlock_environment(tier)

    @final
    def on_deactivate_zoom_buttons(self):
        self.zoom_in_button.on_deactivate(instant=True)
        self.zoom_out_button.on_deactivate(instant=True)

    @final
    def on_activate_zoom_buttons(self):
        if self.zoom_out_activated:
            self.zoom_in_button.on_activate(instant=True)
        else:
            self.zoom_out_button.on_activate(instant=True)

    @final
    @view_is_active
    @cursor_is_on_the_map
    @left_mouse_button
    @map_move_mode_available
    def handle_mouse_press(self, x, y, button, modifiers):
        self.map_move_mode = True

    @final
    @map_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_activate_mini_map()
        self.base_offset = (self.base_offset[0] + dx, self.base_offset[1] + dy)
        self.check_base_offset_limits()
        self.mini_map_frame_position = self.get_mini_map_frame_position()
        self.controller.on_change_base_offset(self.base_offset)

    @final
    @map_move_mode_enabled
    @left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.map_move_mode = False
        self.mini_map_timer = perf_counter()
        self.controller.on_save_and_commit_last_known_base_offset(self.base_offset)

    @final
    def check_base_offset_limits(self):
        if self.base_offset[0] > self.base_offset_lower_left_limit[0]:
            self.base_offset = (self.base_offset_lower_left_limit[0], self.base_offset[1])

        if self.base_offset[0] < self.base_offset_upper_right_limit[0]:
            self.base_offset = (self.base_offset_upper_right_limit[0], self.base_offset[1])

        if self.base_offset[1] > self.base_offset_lower_left_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_lower_left_limit[1])

        if self.base_offset[1] < self.base_offset_upper_right_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_upper_right_limit[1])

    @final
    def on_activate_shop_buttons(self):
        for shop_id in range(len(self.shop_buttons)):
            if self.unlocked_tracks >= self.shops_track_required_state[shop_id]:
                self.shop_buttons[shop_id].on_activate()

    @final
    def on_deactivate_shop_buttons(self):
        for shop_id in range(len(self.shop_buttons)):
            self.shop_buttons[shop_id].on_deactivate()

    @final
    def on_activate_open_constructor_button(self, instant=False):
        if self.constructions_locked > 0:
            self.open_constructor_button.on_activate(instant=instant)
        else:
            self.open_constructor_button.on_disable(instant=instant)

    @final
    def on_unlock_construction(self):
        self.constructions_locked -= 1

    @final
    @view_is_active
    def on_close_schedule(self):
        self.on_activate_zoom_buttons()
        self.on_activate_shop_buttons()
        self.open_schedule_button.on_activate(instant=True)

    @final
    @view_is_active
    def on_close_constructor(self):
        self.on_activate_zoom_buttons()
        self.on_activate_shop_buttons()
        self.on_activate_open_constructor_button(instant=True)

    @final
    def get_mini_map_frame_position(self):
        return (ceil(-self.base_offset[0] / (MAP_WIDTH // round(1 / self.zoom_factor))
                     * get_mini_map_width(self.screen_resolution))
                + get_mini_map_position(self.screen_resolution)[0],
                ceil((get_bottom_bar_height(self.screen_resolution)
                      - self.base_offset[1]) / (MAP_HEIGHT // round(1 / self.zoom_factor))
                     * get_mini_map_height(self.screen_resolution)) + get_mini_map_position(self.screen_resolution)[1])

    @final
    def get_mini_map_frame_height(self):
        return int((self.viewport.y2 - self.viewport.y1
                    - get_bottom_bar_height(self.screen_resolution) - get_top_bar_height(self.screen_resolution))
                   / (MAP_HEIGHT // round(1 / self.zoom_factor)) * get_mini_map_height(self.screen_resolution))

    @final
    def get_mini_map_frame_width(self):
        return int((self.viewport.x2 - self.viewport.x1) / (MAP_WIDTH // round(1 / self.zoom_factor))
                   * get_mini_map_width(self.screen_resolution))

    @final
    def on_recalculate_base_offset_for_new_screen_resolution(self, screen_resolution):
        self.base_offset = (self.base_offset[0] + (screen_resolution[0] - self.screen_resolution[0]) // 2,
                            self.base_offset[1] + (screen_resolution[1] - self.screen_resolution[1]) // 2)

    @final
    def on_map_move_mode_available(self):
        self.map_move_mode_available = True

    @final
    def on_map_move_mode_unavailable(self):
        self.map_move_mode_available = False

    @final
    @view_is_active
    def on_close_map_switcher(self):
        self.on_activate_zoom_buttons()
        self.on_activate_shop_buttons()
        self.on_map_move_mode_available()
