from logging import getLogger
from ctypes import windll

from win32api import GetCursorPos
from win32gui import GetActiveWindow, GetWindowRect, SetWindowPos
from win32con import HWND_TOP, SWP_NOREDRAW

from view import *
from ui import *
from database import CONFIG_DB_CURSOR
from ui.button import create_two_state_button
from ui.button.close_game_button import CloseGameButton
from ui.button.iconify_button import IconifyButton
from ui.button.fullscreen_button import FullscreenButton
from ui.button.restore_button import RestoreButton
from ui.button.en_locale_button import ENLocaleButton
from ui.button.ru_locale_button import RULocaleButton
from ui.label.app_title_label import AppTitleLabel
from ui.shader_sprite.app_view_shader_sprite import AppViewShaderSprite
from ui.sprite.us_flag_sprite import USFlagSprite
from ui.sprite.ru_flag_sprite import RUFlagSprite


class AppView(View):
    def __init__(self):
        def on_close_game(button):
            self.controller.on_close_game()

        def on_iconify_game(button):
            SURFACE.minimize()

        def on_app_window_fullscreen(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.controller.on_fullscreen_button_click()

        def on_app_window_restore(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.controller.on_restore_button_click()

        def on_set_en_locale(button):
            self.controller.on_update_current_locale('en')
            self.controller.on_update_clock_state(clock_24h_enabled=False)

        def on_set_ru_locale(button):
            self.controller.on_update_current_locale('ru')
            self.controller.on_update_clock_state(clock_24h_enabled=True)

        super().__init__(logger=getLogger('root.app.view'))
        self.title_label = AppTitleLabel(parent_viewport=self.viewport)
        self.us_flag_sprite = USFlagSprite(parent_viewport=self.viewport)
        self.ru_flag_sprite = RUFlagSprite(parent_viewport=self.viewport)
        self.close_game_button = CloseGameButton(on_click_action=on_close_game, parent_viewport=self.viewport)
        self.iconify_button = IconifyButton(on_click_action=on_iconify_game, parent_viewport=self.viewport)
        self.fullscreen_button, self.restore_button \
            = create_two_state_button(FullscreenButton(on_click_action=on_app_window_fullscreen,
                                                       parent_viewport=self.viewport),
                                      RestoreButton(on_click_action=on_app_window_restore,
                                                    parent_viewport=self.viewport))
        self.en_locale_button = ENLocaleButton(on_click_action=on_set_en_locale, parent_viewport=self.viewport)
        self.ru_locale_button = RULocaleButton(on_click_action=on_set_ru_locale, parent_viewport=self.viewport)
        self.buttons = [self.close_game_button, self.iconify_button, self.fullscreen_button, self.restore_button,
                        self.en_locale_button, self.ru_locale_button]
        self.app_window_move_mode = False
        self.app_window_move_offset = (0, 0)
        self.game_window_handler = GetActiveWindow()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = GetCursorPos()
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)
        self.shader_sprite = AppViewShaderSprite(view=self)

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.shader_sprite.create()
        self.title_label.create()
        self.us_flag_sprite.create()
        self.ru_flag_sprite.create()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = 0
        self.viewport.y1 = 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        SURFACE.set_size(screen_resolution[0], screen_resolution[1])
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.us_flag_sprite.on_change_screen_resolution(self.screen_resolution)
        self.ru_flag_sprite.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
        self.us_flag_sprite.on_update_opacity(self.opacity)
        self.ru_flag_sprite.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    @staticmethod
    def on_fullscreen_mode_turned_on():
        SURFACE.set_fullscreen(fullscreen=True)

    @staticmethod
    def on_fullscreen_mode_turned_off():
        SURFACE.set_fullscreen(fullscreen=False)

    @game_is_not_fullscreen
    @cursor_is_over_the_app_header
    @left_mouse_button
    @view_is_active
    def handle_mouse_press(self, x, y, button, modifiers):
        self.app_window_move_mode = True
        self.app_window_move_offset = (x, self.viewport.y2 - y)

    @app_window_move_mode_enabled
    @left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.app_window_move_mode = False

    @app_window_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.absolute_mouse_pos = GetCursorPos()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        SetWindowPos(self.game_window_handler, HWND_TOP,
                     self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
                     self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
                     self.game_window_position[2] - self.game_window_position[0],
                     self.game_window_position[3] - self.game_window_position[1], SWP_NOREDRAW)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()
