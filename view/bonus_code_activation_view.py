from hashlib import sha512
from logging import getLogger
from typing import final

from database import ACTIVATIONS_LEFT, BONUS_CODE_MATRIX, BONUS_VALUE, CODE_TYPE, ACTIVATION_AVAILABLE, \
    REQUIRED_LEVEL, IS_ACTIVATED, USER_DB_CURSOR
from ui.label.bonus_code_interactive_label import BonusCodeInteractiveLabel
from ui.button.activate_bonus_code_button import ActivateBonusCodeButton
from ui.button.cancel_bonus_code_activation_button import CancelBonusCodeActivationButton
from ui.shader_sprite.bonus_code_view_shader_sprite import BonusCodeViewShaderSprite
from ui.bonus_code_info_cell import BonusCodeInfoCell
from view import AppBaseView, view_is_not_active, view_is_active


@final
class BonusCodeActivationView(AppBaseView):
    def __init__(self, controller):
        def on_activate_bonus_code(button):
            self.controller.parent_controller.on_activate_new_bonus_code(
                sha512(self.bonus_code_interactive_label.text.encode('utf-8')).hexdigest()
            )
            self.controller.parent_controller.on_close_bonus_code()

        def on_cancel_bonus_code_activation(button):
            self.controller.parent_controller.on_close_bonus_code()

        super().__init__(controller, logger=getLogger('root.app.bonus_code_activation.view'))
        USER_DB_CURSOR.execute('SELECT level FROM game_progress')
        self.level = USER_DB_CURSOR.fetchone()[0]
        self.bonus_code_interactive_label = BonusCodeInteractiveLabel(parent_viewport=self.viewport)
        self.activate_bonus_code_button = ActivateBonusCodeButton(
            on_click_action=on_activate_bonus_code, parent_viewport=self.viewport
        )
        self.cancel_bonus_code_activation_button = CancelBonusCodeActivationButton(
            on_click_action=on_cancel_bonus_code_activation, parent_viewport=self.viewport
        )
        self.buttons = [self.activate_bonus_code_button, self.cancel_bonus_code_activation_button]
        self.shader_sprite = BonusCodeViewShaderSprite(view=self)
        self.bonus_code_info_cell = BonusCodeInfoCell(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend(
            [
                self.bonus_code_interactive_label.on_window_resize, self.shader_sprite.on_window_resize,
                *self.bonus_code_info_cell.on_window_resize_handlers
            ]
        )
        self.on_append_window_handlers()
        self.on_text_handlers.append(self.on_text)
        self.on_key_press_handlers.append(self.on_key_press)

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.bonus_code_interactive_label.create()
        self.activate_bonus_code_button.on_disable()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.bonus_code_info_cell.on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.bonus_code_interactive_label.on_update_current_locale(self.current_locale)
        self.bonus_code_info_cell.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.bonus_code_interactive_label.on_update_opacity(self.opacity)
        self.bonus_code_info_cell.on_update_opacity(self.opacity)

    @view_is_active
    def on_text(self, text):
        characters_before = len(self.bonus_code_interactive_label)
        self.bonus_code_interactive_label.on_text(text)
        characters_after = len(self.bonus_code_interactive_label)
        if (difference := characters_after - characters_before) > 0:
            self.controller.on_increment_bonus_code_abuse_counter(difference)

        self.on_check_bonus_code_availability()

    @view_is_active
    def on_key_press(self, symbol, modifiers):
        characters_before = len(self.bonus_code_interactive_label)
        self.bonus_code_interactive_label.on_key_press(symbol, modifiers)
        characters_after = len(self.bonus_code_interactive_label)
        if (difference := characters_after - characters_before) > 0:
            self.controller.on_increment_bonus_code_abuse_counter(difference)

        self.on_check_bonus_code_availability()

    def on_check_bonus_code_availability(self):
        if (user_input_hash := sha512(self.bonus_code_interactive_label.text.encode('utf-8')).hexdigest()) \
                in BONUS_CODE_MATRIX:
            activated_bonus_counter = 0
            for code in BONUS_CODE_MATRIX:
                if BONUS_CODE_MATRIX[code][CODE_TYPE] == BONUS_CODE_MATRIX[user_input_hash][CODE_TYPE]:
                    activated_bonus_counter += BONUS_CODE_MATRIX[code][IS_ACTIVATED]

            if BONUS_CODE_MATRIX[user_input_hash][ACTIVATIONS_LEFT] > 0 \
                    and BONUS_CODE_MATRIX[user_input_hash][REQUIRED_LEVEL] <= self.level \
                    and BONUS_CODE_MATRIX[user_input_hash][ACTIVATION_AVAILABLE] and activated_bonus_counter == 0:
                self.controller.on_reset_bonus_code_abuse_counter()
                self.activate_bonus_code_button.on_activate()
                self.bonus_code_info_cell.on_activate()
                self.bonus_code_info_cell.on_assign_data(user_input_hash)
            else:
                self.activate_bonus_code_button.on_disable()
                self.bonus_code_info_cell.on_deactivate(instant=True)

        else:
            self.activate_bonus_code_button.on_disable()
            self.bonus_code_info_cell.on_deactivate(instant=True)

