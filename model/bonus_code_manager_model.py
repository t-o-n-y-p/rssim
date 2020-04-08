from logging import getLogger
from typing import final

from database import BONUS_CODE_MATRIX, USER_DB_CURSOR, ACTIVATION_AVAILABLE, ACTIVATIONS_LEFT, IS_ACTIVATED, \
    BONUS_TIME, CODE_TYPE, MAXIMUM_BONUS_TIME, BONUS_VALUE, TRUE, FALSE
from model import GameBaseModel


@final
class BonusCodeManagerModel(GameBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.game.bonus_code_manager.model'))

    def on_save_state(self):
        for code in BONUS_CODE_MATRIX:
            USER_DB_CURSOR.execute(
                '''UPDATE bonus_codes SET activation_available = ?, activations_left = ?, is_activated = ?, 
                bonus_time = ? WHERE sha512_hash = ?''',
                (
                    BONUS_CODE_MATRIX[code][ACTIVATION_AVAILABLE], BONUS_CODE_MATRIX[code][ACTIVATIONS_LEFT],
                    BONUS_CODE_MATRIX[code][IS_ACTIVATED], BONUS_CODE_MATRIX[code][BONUS_TIME], code
                )
            )

    def on_update_time(self, dt):
        for code in BONUS_CODE_MATRIX:
            if BONUS_CODE_MATRIX[code][IS_ACTIVATED]:
                BONUS_CODE_MATRIX[code][BONUS_TIME] -= int(self.game_time_fraction + dt * self.dt_multiplier)
                if BONUS_CODE_MATRIX[code][BONUS_TIME] <= 0:
                    BONUS_CODE_MATRIX[code][IS_ACTIVATED] = FALSE
                    if BONUS_CODE_MATRIX[code][CODE_TYPE] == 'exp_bonus':
                        self.controller.parent_controller.on_deactivate_exp_bonus_code()
                    elif BONUS_CODE_MATRIX[code][CODE_TYPE] == 'money_bonus':
                        self.controller.parent_controller.on_deactivate_money_bonus_code()
                    elif BONUS_CODE_MATRIX[code][CODE_TYPE] == 'construction_time_bonus':
                        self.controller.parent_controller.on_deactivate_construction_time_bonus_code()

        super().on_update_time(dt)

    def on_deactivate_exp_bonus_code(self):
        super().on_deactivate_exp_bonus_code()
        self.view.on_send_exp_bonus_expired_notification()

    def on_deactivate_money_bonus_code(self):
        super().on_deactivate_money_bonus_code()
        self.view.on_send_money_bonus_expired_notification()

    def on_deactivate_construction_time_bonus_code(self):
        super().on_deactivate_construction_time_bonus_code()
        self.view.on_send_construction_time_bonus_expired_notification()

    def on_activate_new_bonus_code(self, sha512_hash):
        BONUS_CODE_MATRIX[sha512_hash][ACTIVATIONS_LEFT] -= 1
        BONUS_CODE_MATRIX[sha512_hash][IS_ACTIVATED] = TRUE
        BONUS_CODE_MATRIX[sha512_hash][BONUS_TIME] = BONUS_CODE_MATRIX[sha512_hash][MAXIMUM_BONUS_TIME]
        if BONUS_CODE_MATRIX[sha512_hash][CODE_TYPE] == 'exp_bonus':
            self.on_activate_exp_bonus_code(BONUS_CODE_MATRIX[sha512_hash][BONUS_VALUE] - 1)
        elif BONUS_CODE_MATRIX[sha512_hash][CODE_TYPE] == 'money_bonus':
            self.on_activate_money_bonus_code(BONUS_CODE_MATRIX[sha512_hash][BONUS_VALUE] - 1)
        elif BONUS_CODE_MATRIX[sha512_hash][CODE_TYPE] == 'construction_time_bonus':
            self.on_activate_construction_time_bonus_code(BONUS_CODE_MATRIX[sha512_hash][BONUS_VALUE] - 1)

    @staticmethod
    def get_bonus_code_type(sha512_hash):
        return BONUS_CODE_MATRIX[sha512_hash][CODE_TYPE]

    @staticmethod
    def get_bonus_code_value(sha512_hash):
        return BONUS_CODE_MATRIX[sha512_hash][BONUS_VALUE]
