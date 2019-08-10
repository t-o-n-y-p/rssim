from logging import getLogger
from ctypes import windll
from hashlib import sha512

from database import CONFIG_DB_CURSOR
from view import *
from ui.label.bonus_code_interactive_label import BonusCodeInteractiveLabel
from ui.button.activate_bonus_code_button import ActivateBonusCodeButton
from ui.button.cancel_bonus_code_activation_button import CancelBonusCodeActivationButton
from ui.shader_sprite.bonus_code_view_shader_sprite import BonusCodeViewShaderSprite


class BonusCodeView(View):
    def __init__(self):
        def on_activate_bonus_code(button):
            self.controller.on_activate_new_bonus_code(
                sha512(self.bonus_code_interactive_label.text.encode('utf-8')).hexdigest())
            self.controller.parent_controller.on_close_bonus_code()

        def on_cancel_bonus_code_activation(button):
            self.controller.parent_controller.on_close_bonus_code()

        super().__init__(logger=getLogger('root.app.bonus_code.view'))
        USER_DB_CURSOR.execute('SELECT level FROM game_progress')
        self.level = USER_DB_CURSOR.fetchone()[0]
        self.bonus_code_interactive_label = BonusCodeInteractiveLabel(parent_viewport=self.viewport)
        self.activate_bonus_code_button = ActivateBonusCodeButton(on_click_action=on_activate_bonus_code,
                                                                  parent_viewport=self.viewport)
        self.cancel_bonus_code_activation_button \
            = CancelBonusCodeActivationButton(on_click_action=on_cancel_bonus_code_activation,
                                              parent_viewport=self.viewport)
        self.buttons = [self.activate_bonus_code_button, self.cancel_bonus_code_activation_button]
        self.shader_sprite = BonusCodeViewShaderSprite(view=self)
        self.bonus_code_matrix = None
        self.on_text_handlers = [self.on_text, ]
        self.on_key_press_handlers = [self.on_key_press, ]

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
        self.bonus_code_interactive_label.create()
        self.activate_bonus_code_button.on_disable()
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
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.bonus_code_interactive_label.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.bonus_code_interactive_label.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.bonus_code_interactive_label.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()

    def on_level_up(self, level):
        self.level = level

    @view_is_active
    def on_text(self, text):
        self.bonus_code_interactive_label.on_text(text)
        self.on_check_bonus_code_availability()

    @view_is_active
    def on_key_press(self, symbol, modifiers):
        self.bonus_code_interactive_label.on_key_press(symbol, modifiers)
        self.on_check_bonus_code_availability()

    def on_check_bonus_code_availability(self):
        user_input_hash = sha512(self.bonus_code_interactive_label.text.encode('utf-8')).hexdigest()
        if user_input_hash in self.bonus_code_matrix:
            activated_bonus_counter = 0
            for code in self.bonus_code_matrix:
                if self.bonus_code_matrix[code][CODE_TYPE] == self.bonus_code_matrix[user_input_hash][CODE_TYPE]:
                    activated_bonus_counter += int(self.bonus_code_matrix[code][IS_ACTIVATED])

            if self.bonus_code_matrix[user_input_hash][ACTIVATIONS_LEFT] > 0 \
                    and self.bonus_code_matrix[user_input_hash][REQUIRED_LEVEL] <= self.level \
                    and self.bonus_code_matrix[user_input_hash][ACTIVATION_AVAILABLE] and activated_bonus_counter == 0:
                self.activate_bonus_code_button.on_activate()
            else:
                self.activate_bonus_code_button.on_disable()
