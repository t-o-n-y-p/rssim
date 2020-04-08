from ctypes import windll
from logging import getLogger
from typing import final

from win32api import GetCursorPos
from win32gui import GetActiveWindow, GetWindowRect, SetWindowPos
from win32con import HWND_TOP, SWP_NOREDRAW

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, TRUE, FALSE
from i18n import ENGLISH, RUSSIAN
from ui import WINDOW
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
from ui.fps_display import FPSDisplay
from view import app_window_move_mode_enabled, cursor_is_over_the_app_header, game_is_not_fullscreen, AppBaseView, \
    view_is_not_active, view_is_active, left_mouse_button


@final
class AppView(AppBaseView):
    def __init__(self, controller):
        def on_close_game(button):
            WINDOW.dispatch_event('on_close')

        def on_iconify_game(button):
            WINDOW.minimize()

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
            self.controller.on_update_current_locale(ENGLISH)
            self.controller.on_update_clock_state(clock_24h_enabled=False)

        def on_set_ru_locale(button):
            self.controller.on_update_current_locale(RUSSIAN)
            self.controller.on_update_clock_state(clock_24h_enabled=True)

        super().__init__(controller, logger=getLogger('root.app.view'))
        self.shader_sprite = AppViewShaderSprite(view=self)
        self.title_label = AppTitleLabel(parent_viewport=self.viewport)
        self.fps_display = FPSDisplay(parent_viewport=self.viewport)
        self.us_flag_sprite = USFlagSprite(parent_viewport=self.viewport)
        self.ru_flag_sprite = RUFlagSprite(parent_viewport=self.viewport)
        self.close_game_button = CloseGameButton(on_click_action=on_close_game, parent_viewport=self.viewport)
        self.iconify_button = IconifyButton(on_click_action=on_iconify_game, parent_viewport=self.viewport)
        self.fullscreen_button, self.restore_button = create_two_state_button(
            FullscreenButton(on_click_action=on_app_window_fullscreen, parent_viewport=self.viewport),
            RestoreButton(on_click_action=on_app_window_restore, parent_viewport=self.viewport)
        )
        self.en_locale_button = ENLocaleButton(on_click_action=on_set_en_locale, parent_viewport=self.viewport)
        self.ru_locale_button = RULocaleButton(on_click_action=on_set_ru_locale, parent_viewport=self.viewport)
        self.buttons = [
            self.close_game_button, self.iconify_button, self.fullscreen_button, self.restore_button,
            self.en_locale_button, self.ru_locale_button
        ]
        self.on_window_resize_handlers.extend(
            [
                *self.fps_display.on_window_resize_handlers, self.title_label.on_window_resize,
                self.shader_sprite.on_window_resize, self.us_flag_sprite.on_window_resize,
                self.ru_flag_sprite.on_window_resize
            ]
        )
        self.on_append_window_handlers()
        self.app_window_move_mode = False
        self.app_window_move_offset = (0, 0)
        self.game_window_handler = GetActiveWindow()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = GetCursorPos()
        self.on_mouse_press_handlers.append(self.on_mouse_press)
        self.on_mouse_release_handlers.append(self.on_mouse_release)
        self.on_mouse_drag_handlers.append(self.on_mouse_drag)
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        self.fullscreen_mode = USER_DB_CURSOR.fetchone()[0]
        self.fullscreen_mode_available = False
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        self.screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        if (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)) in self.screen_resolution_config:
            self.fullscreen_mode_available = True

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.title_label.create()
        self.us_flag_sprite.create()
        self.ru_flag_sprite.create()
        if self.fullscreen_mode_available:
            if self.fullscreen_mode:
                self.restore_button.on_activate()
            else:
                self.fullscreen_button.on_activate()

        else:
            self.fullscreen_button.on_disable()

        USER_DB_CURSOR.execute('SELECT display_fps FROM graphics')
        if USER_DB_CURSOR.fetchone()[0]:
            self.fps_display.on_activate()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.fps_display.on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.fps_display.on_update_opacity(self.opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
        self.us_flag_sprite.on_update_opacity(self.opacity)
        self.ru_flag_sprite.on_update_opacity(self.opacity)

    def on_fullscreen_mode_turned_on(self):
        self.fullscreen_mode = TRUE
        WINDOW.set_fullscreen(fullscreen=self.fullscreen_mode)

    def on_fullscreen_mode_turned_off(self):
        self.fullscreen_mode = FALSE
        WINDOW.set_fullscreen(fullscreen=self.fullscreen_mode)

    @game_is_not_fullscreen
    @cursor_is_over_the_app_header
    @left_mouse_button
    @view_is_active
    def on_mouse_press(self, x, y, button, modifiers):
        self.app_window_move_mode = True
        self.app_window_move_offset = (x, self.viewport.y2 - y)

    @app_window_move_mode_enabled
    @left_mouse_button
    def on_mouse_release(self, x, y, button, modifiers):
        self.app_window_move_mode = False

    @app_window_move_mode_enabled
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.absolute_mouse_pos = GetCursorPos()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        SetWindowPos(
            self.game_window_handler, HWND_TOP,
            self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
            self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
            self.game_window_position[2] - self.game_window_position[0],
            self.game_window_position[3] - self.game_window_position[1], SWP_NOREDRAW
        )
