from logging import getLogger
from time import perf_counter

from view import *
from database import CONFIG_DB_CURSOR
from ui.button.open_schedule_button import OpenScheduleButton
from ui.button.open_constructor_button import OpenConstructorButton
from ui.button.open_shop_details_button import OpenShopDetailsButton
from ui.shader_sprite.map_view_shader_sprite import MapViewShaderSprite
from ui.sprite.main_map_sprite import MainMapSprite
from ui.sprite.main_environment_sprite import MainEnvironmentSprite


class MapView(MapBaseView):
    def __init__(self, controller, map_id):
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

        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.view'))
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        self.mini_map_offset = (0, 0)
        self.main_map_sprite = MainMapSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.environment_sprite = MainEnvironmentSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.mini_map_timer = 0.0
        USER_DB_CURSOR.execute('''SELECT last_known_base_offset FROM map_position_settings WHERE map_id = ?''',
                               (self.map_id,))
        self.base_offset = [float(p) for p in USER_DB_CURSOR.fetchone()[0].split(',')]
        USER_DB_CURSOR.execute('''SELECT last_known_zoom FROM map_position_settings 
                                  WHERE map_id IN (SELECT last_known_map_id FROM graphics)''')
        self.zoom = Fraction(USER_DB_CURSOR.fetchone()[0])
        self.base_offset_lower_left_limit = (0, 0)
        self.base_offset_upper_right_limit = (0, 0)
        self.open_schedule_button = OpenScheduleButton(on_click_action=on_open_schedule, parent_viewport=self.viewport)
        self.open_constructor_button = OpenConstructorButton(on_click_action=on_open_constructor,
                                                             parent_viewport=self.viewport)
        self.buttons = [self.open_schedule_button, self.open_constructor_button]
        self.shop_buttons = []
        CONFIG_DB_CURSOR.execute('''SELECT COUNT(*) FROM shops_config WHERE map_id = ?''', (self.map_id, ))
        for shop_id in range(CONFIG_DB_CURSOR.fetchone()[0]):
            self.shop_buttons.append(OpenShopDetailsButton(map_id=self.map_id, shop_id=shop_id,
                                                           on_click_action=on_open_shop_details,
                                                           on_hover_action=on_hover_action,
                                                           on_leave_action=on_leave_action))

        CONFIG_DB_CURSOR.execute('''SELECT track_required FROM shops_config 
                                    WHERE map_id = ?''', (self.map_id, ))
        self.shops_track_required_state = tuple(s[0] for s in CONFIG_DB_CURSOR.fetchall())
        self.buttons.extend(self.shop_buttons)
        for b in self.shop_buttons:
            b.position = b.get_position()
            b.on_change_scale()

        self.map_move_mode_available = False
        self.map_move_mode = False
        self.on_mouse_press_handlers.append(self.on_mouse_press)
        self.on_mouse_release_handlers.append(self.on_mouse_release)
        self.on_mouse_drag_handlers.append(self.on_mouse_drag)
        self.on_mouse_scroll_handlers.append(self.on_mouse_scroll)
        self.shader_sprite = MapViewShaderSprite(view=self)
        USER_DB_CURSOR.execute('''SELECT SUM(t.constructions_locked) FROM (
                                      SELECT COUNT(track_number) AS constructions_locked FROM tracks 
                                      WHERE locked = 1 AND map_id = ?
                                      UNION
                                      SELECT COUNT(tier) AS constructions_locked FROM environment 
                                      WHERE locked = 1 AND map_id = ?
                                  ) AS t''', (self.map_id, self.map_id))
        self.constructions_locked = USER_DB_CURSOR.fetchone()[0]
        self.is_mini_map_timer_activated = False

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        MAP_CAMERA.position = -self.base_offset[0], -self.base_offset[1]
        MAP_CAMERA.zoom = self.zoom
        self.map_move_mode_available = True
        self.shader_sprite.create()
        self.main_map_sprite.create()
        self.environment_sprite.create()
        self.on_activate_open_constructor_button()
        self.on_activate_shop_buttons()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_update(self):
        if self.is_mini_map_timer_activated and not self.map_move_mode \
                and perf_counter() - self.mini_map_timer > MINI_MAP_FADE_OUT_TIMER:
            self.controller.on_deactivate_mini_map()
            self.is_mini_map_timer_activated = False

    @final
    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.base_offset_lower_left_limit = (self.viewport.x1,
                                             self.viewport.y1 + get_bottom_bar_height(self.screen_resolution))
        self.base_offset_upper_right_limit = (self.viewport.x2 - MAP_WIDTH * self.zoom,
                                              self.viewport.y2 - MAP_HEIGHT * self.zoom
                                              - get_top_bar_height(self.screen_resolution))
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.open_schedule_button.on_change_screen_resolution(self.screen_resolution)
        self.open_constructor_button.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.main_map_sprite.on_update_opacity(self.opacity)
        self.environment_sprite.on_update_opacity(self.opacity)

    @final
    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        self.main_map_sprite.on_unlock_track(self.unlocked_tracks)

    @final
    def on_unlock_environment(self, tier):
        self.environment_sprite.on_unlock_environment(tier)

    @final
    @view_is_active
    @cursor_is_on_the_map
    @left_mouse_button
    @map_move_mode_available
    def on_mouse_press(self, x, y, button, modifiers):
        self.map_move_mode = True

    @final
    @map_move_mode_enabled
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.controller.on_activate_mini_map()
        self.base_offset = (self.base_offset[0] + dx, self.base_offset[1] + dy)
        self.check_base_offset_limits()

    @final
    @map_move_mode_enabled
    @left_mouse_button
    def on_mouse_release(self, x, y, button, modifiers):
        self.map_move_mode = False
        self.mini_map_timer = perf_counter()
        self.is_mini_map_timer_activated = True
        self.controller.on_save_and_commit_last_known_base_offset()

    @final
    @view_is_active
    @cursor_is_on_the_map
    @map_move_mode_available
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        MAP_CAMERA.zoom -= scroll_y * MAP_ZOOM_STEP
        self.on_recalculate_base_offset_for_new_zoom(MAP_CAMERA.zoom)
        self.base_offset_upper_right_limit = (self.viewport.x2 - MAP_WIDTH * MAP_CAMERA.zoom,
                                              self.viewport.y2 - MAP_HEIGHT * MAP_CAMERA.zoom
                                              - get_top_bar_height(self.screen_resolution))
        self.check_base_offset_limits()
        self.controller.on_save_and_commit_last_known_base_offset()
        self.zoom = Fraction(MAP_CAMERA.zoom)
        self.controller.on_save_and_commit_last_known_zoom()

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

        if self.is_activated:
            MAP_CAMERA.position = -self.base_offset[0], -self.base_offset[1]

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
        self.on_activate_shop_buttons()
        self.open_schedule_button.on_activate(instant=True)

    @final
    @view_is_active
    def on_close_constructor(self):
        self.on_activate_shop_buttons()
        self.on_activate_open_constructor_button(instant=True)

    @final
    def on_recalculate_base_offset_for_new_screen_resolution(self, screen_resolution):
        self.base_offset = (self.base_offset[0] + (screen_resolution[0] - self.screen_resolution[0]) // 2,
                            self.base_offset[1] + (screen_resolution[1] - self.screen_resolution[1]) // 2)

    @final
    def on_recalculate_base_offset_for_new_zoom(self, new_zoom):
        multiplier = new_zoom / self.zoom
        if multiplier > 1:
            self.base_offset = (self.base_offset[0] - (multiplier - 1) * (self.viewport.x2 - self.viewport.x1) // 2,
                                self.base_offset[1] - (multiplier - 1) * (self.viewport.x2 - self.viewport.x1) // 2)
        elif multiplier < 1:
            self.base_offset = (self.base_offset[0] + multiplier * (self.viewport.x2 - self.viewport.x1) // 2,
                                self.base_offset[1] + multiplier * (self.viewport.x2 - self.viewport.x1) // 2)

    @final
    def on_map_move_mode_available(self):
        self.map_move_mode_available = True

    @final
    def on_map_move_mode_unavailable(self):
        self.map_move_mode_available = False

    @final
    @view_is_active
    def on_close_map_switcher(self):
        self.on_activate_shop_buttons()
        self.on_map_move_mode_available()
