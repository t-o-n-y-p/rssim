from pyglet.window import mouse
from pyglet.text import Label
from pyglet.gl import GL_QUADS
from pyshaders import from_files_names
from win32api import GetCursorPos
from win32gui import GetActiveWindow, GetWindowRect, SetWindowPos
from win32con import HWND_TOP, SWP_NOREDRAW

from .view_base import View
from .button import CloseGameButton, IconifyGameButton, FullscreenButton, RestoreButton, OpenSettingsButton


def _game_window_is_active(fn):
    def _handle_if_game_window_is_active(*args, **kwargs):
        if args[0].surface.visible:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_active


def _game_is_not_fullscreen(fn):
    def _handle_if_game_window_is_not_fullscreen(*args, **kwargs):
        if not args[0].surface.fullscreen:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_not_fullscreen


def _app_window_move_mode_enabled(fn):
    def _handle_if_app_window_move_mode_enabled(*args, **kwargs):
        if args[0].app_window_move_mode:
            fn(*args, **kwargs)

    return _handle_if_app_window_move_mode_enabled


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


class AppView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups):
        def on_close_game(button):
            self.controller.on_close_game()

        def on_iconify_game(button):
            self.surface.minimize()

        def on_app_window_fullscreen(button):
            self.controller.on_fullscreen_mode_turned_on()

        def on_app_window_restore(button):
            self.controller.on_fullscreen_mode_turned_off()

        def on_open_settings(button):
            button.on_deactivate()
            self.controller.settings.on_activate()

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
        self.screen_resolution = (1280, 720)
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
        self.shader = from_files_names('shaders/main_frame/shader.vert', 'shaders/main_frame/shader.frag')
        self.title_label = None
        self.main_frame_sprite = None
        self.close_game_button = CloseGameButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                 on_click_action=on_close_game)
        self.iconify_game_button = IconifyGameButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                     on_click_action=on_iconify_game)
        self.fullscreen_button = FullscreenButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                  on_click_action=on_app_window_fullscreen)
        self.restore_button = RestoreButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                            on_click_action=on_app_window_restore)
        self.open_settings_button = OpenSettingsButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                       on_click_action=on_open_settings)
        self.fullscreen_button.paired_button = self.restore_button
        self.restore_button.paired_button = self.fullscreen_button
        self.buttons.append(self.close_game_button)
        self.buttons.append(self.iconify_game_button)
        self.buttons.append(self.fullscreen_button)
        self.buttons.append(self.restore_button)
        self.buttons.append(self.open_settings_button)
        self.app_window_move_mode = False
        self.app_window_move_offset = (0, 0)
        self.game_window_handler = GetActiveWindow()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = GetCursorPos()
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)

    def on_update(self):
        pass

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.title_label = Label('Railway Station Simulator', font_name='Arial',
                                 font_size=int(16 / 40 * self.top_bar_height),
                                 x=10, y=self.screen_resolution[1] - self.top_bar_height // 2,
                                 anchor_x='left', anchor_y='center', batch=self.ui_batch,
                                 group=self.groups['button_text'])
        if self.main_frame_sprite is None:
            self.main_frame_sprite\
                = self.main_frame_batch.add(4, GL_QUADS, self.groups['main_frame'],
                                            ('v2f/static', (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0)))

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.main_frame_sprite.delete()
        self.main_frame_sprite = None
        self.title_label.delete()
        self.title_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution, fullscreen):
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
        if not fullscreen:
            self.surface.set_size(screen_resolution[0], screen_resolution[1])

        self.title_label.y = self.screen_resolution[1] - self.top_bar_height // 2
        self.title_label.font_size = int(16 / 40 * self.top_bar_height)
        self.close_game_button.x_margin = self.screen_resolution[0] - self.top_bar_height
        self.close_game_button.y_margin = self.screen_resolution[1] - self.top_bar_height
        self.close_game_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                               int(19 / 40 * self.top_bar_height))
        self.fullscreen_button.x_margin = self.screen_resolution[0] - self.top_bar_height * 2 + 2
        self.fullscreen_button.y_margin = self.screen_resolution[1] - self.top_bar_height
        self.fullscreen_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                               int(19 / 40 * self.top_bar_height))
        self.restore_button.x_margin = self.screen_resolution[0] - self.top_bar_height * 2 + 2
        self.restore_button.y_margin = self.screen_resolution[1] - self.top_bar_height
        self.restore_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                            int(19 / 40 * self.top_bar_height))
        self.iconify_game_button.x_margin = self.screen_resolution[0] - self.top_bar_height * 3 + 4
        self.iconify_game_button.y_margin = self.screen_resolution[1] - self.top_bar_height
        self.iconify_game_button.on_size_changed((self.top_bar_height, self.top_bar_height),
                                                 int(19 / 40 * self.top_bar_height))
        self.open_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        self.open_settings_button.y_margin = 0
        self.open_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                  int(30 / 80 * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_fullscreen_mode_turned_on(self):
        self.surface.set_fullscreen(fullscreen=True)
        self.restore_button.on_activate()
        self.fullscreen_button.on_deactivate()

    def on_fullscreen_mode_turned_off(self):
        self.surface.set_fullscreen(fullscreen=False)
        self.restore_button.on_deactivate()
        self.fullscreen_button.on_activate()

    @_game_window_is_active
    @_game_is_not_fullscreen
    @_left_mouse_button
    @_view_is_active
    def handle_mouse_press(self, x, y, button, modifiers):
        y = self.surface.height - y
        if x in range(0, self.surface.width - 100) and y in range(0, 33):
            self.app_window_move_mode = True
            self.app_window_move_offset = (x, y)

    @_game_window_is_active
    @_left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.app_window_move_mode = False

    @_game_window_is_active
    @_app_window_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.absolute_mouse_pos = GetCursorPos()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        SetWindowPos(self.game_window_handler, HWND_TOP,
                     self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
                     self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
                     self.game_window_position[2] - self.game_window_position[0],
                     self.game_window_position[3] - self.game_window_position[1], SWP_NOREDRAW)

    def on_draw_main_frame(self):
        self.shader.use()
        self.shader.uniforms.screen_resolution = self.screen_resolution
        self.shader.uniforms.base_offset = ((-1) * self.controller.game.map.view.base_offset[0],
                                            (-1) * self.controller.game.map.view.base_offset[1])
        self.shader.uniforms.bottom_bar_height = self.bottom_bar_height
        self.shader.uniforms.top_bar_height = self.top_bar_height
        self.shader.uniforms.top_left_cell \
            = (self.controller.game.map.constructor.view.track_cells_positions[0][0],
               self.controller.game.map.constructor.view.track_cells_positions[0][1] + self.bottom_bar_height - 1)
        self.shader.uniforms.top_right_cell \
            = (self.controller.game.map.constructor.view.environment_cell_positions[0][0],
               self.controller.game.map.constructor.view.environment_cell_positions[0][1] + self.bottom_bar_height - 1)
        self.shader.uniforms.game_frame_opacity = self.controller.game.view.game_frame_opacity
        self.shader.uniforms.schedule_opacity = self.controller.game.map.scheduler.view.schedule_opacity
        self.shader.uniforms.constructor_opacity = self.controller.game.map.constructor.view.constructor_opacity
        self.shader.uniforms.settings_is_activated = int(self.controller.settings.view.is_activated)
        self.shader.uniforms.zoom_buttons_activated \
            = int(self.controller.game.map.view.zoom_in_button.is_activated
                  or self.controller.game.map.view.zoom_out_button.is_activated)
        self.shader.uniforms.track_build_button_is_activated \
            = int(len(self.controller.game.map.constructor.view.buy_buttons) > 0)
        self.shader.uniforms.mini_map_opacity = self.controller.game.map.view.mini_map_opacity
        self.shader.uniforms.zoom_out_activated = int(self.controller.game.map.view.zoom_out_activated)
        self.shader.uniforms.mini_map_position = self.controller.game.map.view.mini_map_position
        self.shader.uniforms.mini_map_width = self.controller.game.map.view.mini_map_width
        self.shader.uniforms.mini_map_height = self.controller.game.map.view.mini_map_height
        self.main_frame_sprite.draw(GL_QUADS)
        self.shader.clear()
