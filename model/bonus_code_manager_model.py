from logging import getLogger

from model import *
from database import USER_DB_CURSOR, BONUS_CODE_MATRIX


@final
class BonusCodeManagerModel(GameBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.game.bonus_code_manager.model'))
        self.bonus_code_matrix = BONUS_CODE_MATRIX

    def on_save_state(self):
        for code in self.bonus_code_matrix:
            USER_DB_CURSOR.execute('''UPDATE bonus_codes SET activation_available = ?, activations_left = ?, 
                                      is_activated = ?, bonus_time = ? WHERE sha512_hash = ?''',
                                   (int(self.bonus_code_matrix[code][ACTIVATION_AVAILABLE]),
                                    self.bonus_code_matrix[code][ACTIVATIONS_LEFT],
                                    int(self.bonus_code_matrix[code][IS_ACTIVATED]),
                                    self.bonus_code_matrix[code][BONUS_TIME], code))

    def on_update_time(self, dt):
        for code in self.bonus_code_matrix:
            if self.bonus_code_matrix[code][IS_ACTIVATED]:
                self.bonus_code_matrix[code][BONUS_TIME] -= int(self.game_time_fraction + dt * self.dt_multiplier)
                if self.bonus_code_matrix[code][BONUS_TIME] <= 0:
                    self.bonus_code_matrix[code][IS_ACTIVATED] = False
                    if self.bonus_code_matrix[code][CODE_TYPE] == 'exp_bonus':
                        self.controller.parent_controller.on_deactivate_exp_bonus_code()
                    elif self.bonus_code_matrix[code][CODE_TYPE] == 'money_bonus':
                        self.controller.parent_controller.on_deactivate_money_bonus_code()
                    elif self.bonus_code_matrix[code][CODE_TYPE] == 'construction_time_bonus':
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
        self.bonus_code_matrix[sha512_hash][ACTIVATIONS_LEFT] -= 1
        self.bonus_code_matrix[sha512_hash][IS_ACTIVATED] = True
        self.bonus_code_matrix[sha512_hash][BONUS_TIME] = self.bonus_code_matrix[sha512_hash][MAXIMUM_BONUS_TIME]
        if self.bonus_code_matrix[sha512_hash][CODE_TYPE] == 'exp_bonus':
            self.on_activate_exp_bonus_code(self.bonus_code_matrix[sha512_hash][BONUS_VALUE] - 1)
        elif self.bonus_code_matrix[sha512_hash][CODE_TYPE] == 'money_bonus':
            self.on_activate_money_bonus_code(self.bonus_code_matrix[sha512_hash][BONUS_VALUE] - 1)
        elif self.bonus_code_matrix[sha512_hash][CODE_TYPE] == 'construction_time_bonus':
            self.on_activate_construction_time_bonus_code(self.bonus_code_matrix[sha512_hash][BONUS_VALUE] - 1)

    def get_bonus_code_type(self, sha512_hash):
        return self.bonus_code_matrix[sha512_hash][CODE_TYPE]

    def get_bonus_code_value(self, sha512_hash):
        return self.bonus_code_matrix[sha512_hash][BONUS_VALUE]
