from time import perf_counter

from pyglet.sprite import Sprite
from pyglet.window import mouse
from pyglet import resource

from .view_base import View
from .button import ZoomInButton, ZoomOutButton, OpenScheduleButton, OpenConstructorButton


def _map_move_mode_available(fn):
    def _turn_on_move_mode_if_map_move_mode_available(*args, **kwargs):
        if args[0].map_move_mode_available and not args[0].controller.scheduler.view.is_activated \
                and not args[0].controller.constructor.view.is_activated:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_available


def _map_move_mode_enabled(fn):
    def _turn_on_move_mode_if_map_move_mode_enabled(*args, **kwargs):
        if args[0].map_move_mode:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_enabled


def _left_mouse_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


def _cursor_is_on_the_map(fn):
    def _enable_map_move_mode_if_cursor_is_on_the_map(*args, **kwargs):
        if args[1] in range(0, args[0].screen_resolution[0]) \
                and args[2] in range(80, args[0].screen_resolution[1] - 35):
            fn(*args, **kwargs)

    return _enable_map_move_mode_if_cursor_is_on_the_map


def _mini_map_is_not_active(fn):
    def _handle_if_mini_map_is_not_activated(*args, **kwargs):
        if not args[0].is_mini_map_activated:
            fn(*args, **kwargs)

    return _handle_if_mini_map_is_not_activated


class MapView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups):
        def on_zoom_in_button(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_zoom_in()

        def on_zoom_out_button(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_zoom_out()

        def on_leave_action():
            self.map_move_mode_available = True

        def on_hover_action():
            self.map_move_mode_available = False

        def on_open_schedule(button):
            button.on_deactivate()
            self.controller.on_open_schedule()

        def on_open_constructor(button):
            button.on_deactivate()
            self.controller.on_open_constructor()

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]
        self.map_offset = ()
        self.mini_map_offset = ()
        self.main_map = resource.image(f'full_map_{self.unlocked_tracks}.dds')
        self.environment = resource.image(f'full_map_e_0.dds')
        self.main_map_sprite = None
        self.environment_sprite = None
        self.mini_map_sprite = None
        self.mini_environment_sprite = None
        self.is_mini_map_activated = False
        self.mini_map_timer = 0.0
        self.mini_map_opacity = 0
        self.screen_resolution = (1280, 720)
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
        self.base_offset = (-3456, -1688)
        self.base_offset_lower_left_limit = (0, 0)
        self.base_offset_upper_right_limit = (-6912, -3376)
        self.mini_map_position = (2 * self.screen_resolution[0] // 3,
                                  self.screen_resolution[1] - self.top_bar_height - 6
                                  - (self.screen_resolution[0] // 3 - 6) // 2)
        self.mini_map_width = self.screen_resolution[0] // 3 - 6
        self.mini_map_height = (self.screen_resolution[0] // 3 - 6) // 2
        self.zoom_factor = 1.0
        self.zoom_out_activated = False
        self.zoom_in_button = ZoomInButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                           on_click_action=on_zoom_in_button, on_hover_action=on_hover_action,
                                           on_leave_action=on_leave_action)
        self.zoom_out_button = ZoomOutButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                             on_click_action=on_zoom_out_button, on_hover_action=on_hover_action,
                                             on_leave_action=on_leave_action)
        self.open_schedule_button = OpenScheduleButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                       on_click_action=on_open_schedule)
        self.open_constructor_button = OpenConstructorButton(surface=self.surface, batch=self.ui_batch,
                                                             groups=self.groups, on_click_action=on_open_constructor)
        self.zoom_in_button.paired_button = self.zoom_out_button
        self.zoom_out_button.paired_button = self.zoom_in_button
        self.buttons.append(self.zoom_in_button)
        self.buttons.append(self.zoom_out_button)
        self.buttons.append(self.open_schedule_button)
        self.buttons.append(self.open_constructor_button)
        self.map_move_mode_available = True
        self.map_move_mode = False
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)

    def on_update(self):
        if self.is_activated and self.main_map_sprite.opacity < 255:
            self.main_map_sprite.opacity += 15
            self.environment_sprite.opacity += 15

        if not self.is_activated and self.main_map_sprite is not None:
            if self.main_map_sprite.opacity > 0:
                self.main_map_sprite.opacity -= 15
                if self.main_map_sprite.opacity <= 0:
                    self.main_map_sprite.delete()
                    self.main_map_sprite = None

            if self.environment_sprite.opacity > 0:
                self.environment_sprite.opacity -= 15
                if self.environment_sprite.opacity <= 0:
                    self.environment_sprite.delete()
                    self.environment_sprite = None

        if self.is_mini_map_activated and self.mini_map_sprite.opacity < 255:
            self.mini_map_sprite.opacity += 15
            self.mini_environment_sprite.opacity += 15
            self.mini_map_opacity += 15

        if not self.is_mini_map_activated and self.mini_map_sprite is not None:
            if self.mini_map_sprite.opacity > 0:
                self.mini_map_opacity -= 15
                self.mini_map_sprite.opacity -= 15
                if self.mini_map_sprite.opacity <= 0:
                    self.mini_map_sprite.delete()
                    self.mini_map_sprite = None

            if self.mini_environment_sprite.opacity > 0:
                self.mini_environment_sprite.opacity -= 15
                if self.mini_environment_sprite.opacity <= 0:
                    self.mini_environment_sprite.delete()
                    self.mini_environment_sprite = None

        if self.is_mini_map_activated and not self.map_move_mode and perf_counter() - self.mini_map_timer > 1:
            self.is_mini_map_activated = False

    @_mini_map_is_not_active
    def on_activate_mini_map(self):
        self.is_mini_map_activated = True
        self.mini_environment_sprite = Sprite(self.environment, x=self.mini_map_position[0],
                                              y=self.mini_map_position[1],
                                              batch=self.batch, group=self.groups['mini_environment'])
        self.mini_environment_sprite.opacity = 0
        self.mini_environment_sprite.scale = self.mini_map_width / 8192
        self.mini_map_sprite = Sprite(self.main_map, x=self.mini_map_position[0],
                                      y=self.mini_map_position[1]
                                      + int(self.mini_map_offset[1] * (self.screen_resolution[0] // 3 - 6) / 8192),
                                      batch=self.batch, group=self.groups['mini_map'])
        self.mini_map_sprite.opacity = 0
        self.mini_map_sprite.scale = self.mini_map_width / 8192

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_change_map_offset()
        if self.main_map_sprite is None:
            self.main_map_sprite = Sprite(self.main_map, x=self.base_offset[0] + self.map_offset[0],
                                          y=self.base_offset[1] + self.map_offset[1],
                                          batch=self.batch, group=self.groups['main_map'])
            self.main_map_sprite.opacity = 0
            self.main_map_sprite.scale = self.zoom_factor

            self.environment_sprite = Sprite(self.environment, x=self.base_offset[0], y=self.base_offset[1],
                                             batch=self.batch, group=self.groups['environment'])
            self.environment_sprite.opacity = 0
            self.environment_sprite.scale = self.zoom_factor

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

        if self.zoom_out_activated:
            self.zoom_in_button.on_activate()
        else:
            self.zoom_out_button.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.is_mini_map_activated = False
        self.main_map_sprite.delete()
        self.main_map_sprite = None
        self.environment_sprite.delete()
        self.environment_sprite = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        if self.is_activated:
            self.main_map_sprite.position = (self.base_offset[0] + self.map_offset[0],
                                             self.base_offset[1] + self.map_offset[1])
            self.environment_sprite.position = self.base_offset

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number
        self.main_map = resource.image(f'full_map_{track_number}.dds')
        self.on_change_map_offset()

        if self.is_activated:
            self.main_map_sprite.image = self.main_map
            self.main_map_sprite.position = (self.base_offset[0] + self.map_offset[0],
                                             self.base_offset[1] + self.map_offset[1])

        if self.is_mini_map_activated:
            self.mini_map_sprite.image = self.main_map
            self.mini_map_sprite.update(y=self.mini_map_position[1]
                                        + int(self.mini_map_offset[1] * (self.screen_resolution[0] // 3 - 6) / 8192),
                                        scale=self.mini_map_width / 8192)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        self.on_change_map_offset()

        if self.is_activated:
            self.main_map_sprite.scale = zoom_factor
            self.environment_sprite.scale = zoom_factor

        if zoom_out_activated:
            self.base_offset_upper_right_limit = (self.screen_resolution[0] - 4096, self.screen_resolution[1] - 2048)
            self.base_offset = (self.base_offset[0] // 2 + self.screen_resolution[0] // 4,
                                self.base_offset[1] // 2 + self.screen_resolution[1] // 4)
        else:
            self.base_offset_upper_right_limit = (self.screen_resolution[0] - 8192, self.screen_resolution[1] - 4096)
            self.base_offset = (self.base_offset[0] * 2 - self.screen_resolution[0] // 2,
                                self.base_offset[1] * 2 - self.screen_resolution[1] // 2)

        self.check_base_offset_limits()

    def on_change_screen_resolution(self, screen_resolution):
        if self.zoom_out_activated:
            self.base_offset_upper_right_limit = (screen_resolution[0] - 4096, screen_resolution[1] - 2048)
        else:
            self.base_offset_upper_right_limit = (screen_resolution[0] - 8192, screen_resolution[1] - 4096)

        self.base_offset = (self.base_offset[0] + (screen_resolution[0] - self.screen_resolution[0]) // 2,
                            self.base_offset[1] + (screen_resolution[1] - self.screen_resolution[1]) // 2)
        self.check_base_offset_limits()
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
        self.mini_map_position = (2 * self.screen_resolution[0] // 3,
                                  self.screen_resolution[1] - self.top_bar_height - 6
                                  - (self.screen_resolution[0] // 3 - 6) // 2)
        self.mini_map_width = self.screen_resolution[0] // 3 - 6
        self.mini_map_height = (self.screen_resolution[0] // 3 - 6) // 2
        if self.is_mini_map_activated:
            self.mini_environment_sprite.update(x=self.mini_map_position[0], y=self.mini_map_position[1],
                                                scale=self.mini_map_width / 8192)
            self.mini_map_sprite.update(x=self.mini_map_position[0],
                                        y=self.mini_map_position[1]
                                        + int(self.mini_map_offset[1] * (self.screen_resolution[0] // 3 - 6) / 8192),
                                        scale=self.mini_map_width / 8192)

        self.zoom_in_button.x_margin = 0
        self.zoom_in_button.y_margin = self.screen_resolution[1] - self.top_bar_height - self.bottom_bar_height + 2
        self.zoom_in_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                            int(30 / 80 * self.bottom_bar_height))
        self.zoom_out_button.x_margin = 0
        self.zoom_out_button.y_margin = self.screen_resolution[1] - self.top_bar_height - self.bottom_bar_height + 2
        self.zoom_out_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                             int(30 / 80 * self.bottom_bar_height))
        self.open_schedule_button.x_margin = self.screen_resolution[0] - 11 * self.bottom_bar_height // 2 + 2
        self.open_schedule_button.y_margin = 0
        self.open_schedule_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                  int(32 / 80 * self.bottom_bar_height))
        self.open_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                     int(34 / 80 * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_deactivate_zoom_buttons(self):
        self.zoom_in_button.on_deactivate()
        self.zoom_out_button.on_deactivate()

    def on_activate_zoom_buttons(self):
        if self.zoom_out_activated:
            self.zoom_in_button.on_activate()
        else:
            self.zoom_out_button.on_activate()

    @_view_is_active
    @_cursor_is_on_the_map
    @_left_mouse_button
    @_map_move_mode_available
    def handle_mouse_press(self, x, y, button, modifiers):
        self.map_move_mode = True
        self.on_activate_mini_map()

    @_map_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.base_offset = (self.base_offset[0] + dx, self.base_offset[1] + dy)
        self.check_base_offset_limits()
        self.controller.on_change_base_offset(self.base_offset)

    @_left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.map_move_mode = False
        self.mini_map_timer = perf_counter()

    def check_base_offset_limits(self):
        if self.base_offset[0] > self.base_offset_lower_left_limit[0]:
            self.base_offset = (self.base_offset_lower_left_limit[0], self.base_offset[1])

        if self.base_offset[0] < self.base_offset_upper_right_limit[0]:
            self.base_offset = (self.base_offset_upper_right_limit[0], self.base_offset[1])

        if self.base_offset[1] > self.base_offset_lower_left_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_lower_left_limit[1])

        if self.base_offset[1] < self.base_offset_upper_right_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_upper_right_limit[1])

    def on_change_map_offset(self):
        if self.zoom_out_activated:
            if self.unlocked_tracks < 5:
                self.map_offset = (0, 896)
                self.mini_map_offset = (0, 1792)
            elif self.unlocked_tracks < 9:
                self.map_offset = (0, 768)
                self.mini_map_offset = (0, 1536)
            elif self.unlocked_tracks < 21:
                self.map_offset = (0, 512)
                self.mini_map_offset = (0, 1024)
            else:
                self.map_offset = (0, 0)
                self.mini_map_offset = (0, 0)
        else:
            if self.unlocked_tracks < 5:
                self.map_offset = (0, 1792)
                self.mini_map_offset = (0, 1792)
            elif self.unlocked_tracks < 9:
                self.map_offset = (0, 1536)
                self.mini_map_offset = (0, 1536)
            elif self.unlocked_tracks < 21:
                self.map_offset = (0, 1024)
                self.mini_map_offset = (0, 1024)
            else:
                self.map_offset = (0, 0)
                self.mini_map_offset = (0, 0)
