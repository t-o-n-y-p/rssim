from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class BonusCodeModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.bonus_code.model'))
        self.bonus_code_matrix = {}
        CONFIG_DB_CURSOR.execute('''SELECT * FROM bonus_codes_config''')
        for line in CONFIG_DB_CURSOR.fetchall():
            self.bonus_code_matrix[line[0]] = [*line[1:]]
            USER_DB_CURSOR.execute('''SELECT activation_available, activations_left, is_activated, bonus_time
                                      FROM bonus_codes WHERE sha512_hash = ?''', (line[0], ))
            self.bonus_code_matrix[line[0]].extend(USER_DB_CURSOR.fetchone())
            self.bonus_code_matrix[line[0]][ACTIVATION_AVAILABLE] \
                = bool(self.bonus_code_matrix[line[0]][ACTIVATION_AVAILABLE])
            self.bonus_code_matrix[line[0]][IS_ACTIVATED] \
                = bool(self.bonus_code_matrix[line[0]][IS_ACTIVATED])

    def on_activate_view(self):
        self.view.on_activate()

    def on_save_state(self):
        for code in self.bonus_code_matrix:
            USER_DB_CURSOR.execute('''UPDATE bonus_codes SET activation_available = ?, activations_left = ?, 
                                      is_activated = ?, bonus_time = ? WHERE sha512_hash = ?''',
                                   (int(self.bonus_code_matrix[code][ACTIVATION_AVAILABLE]),
                                    self.bonus_code_matrix[code][ACTIVATIONS_LEFT],
                                    int(self.bonus_code_matrix[code][IS_ACTIVATED]),
                                    self.bonus_code_matrix[code][BONUS_TIME], code))

    def on_activate_new_bonus_code(self, sha512_hash):
        self.bonus_code_matrix[sha512_hash][ACTIVATIONS_LEFT] -= 1
        self.bonus_code_matrix[sha512_hash][IS_ACTIVATED] = True
        self.bonus_code_matrix[sha512_hash][BONUS_TIME] = self.bonus_code_matrix[sha512_hash][MAXIMUM_BONUS_TIME]
        if self.bonus_code_matrix[sha512_hash][CODE_TYPE] == 'exp_bonus':
            self.controller.parent_controller\
                .on_activate_exp_bonus_code(self.bonus_code_matrix[sha512_hash][BONUS_VALUE] - 1)
        elif self.bonus_code_matrix[sha512_hash][CODE_TYPE] == 'money_bonus':
            self.controller.parent_controller\
                .on_activate_money_bonus_code(self.bonus_code_matrix[sha512_hash][BONUS_VALUE] - 1)

    def on_update_time(self, game_time):
        for code in self.bonus_code_matrix:
            if self.bonus_code_matrix[code][IS_ACTIVATED]:
                self.bonus_code_matrix[code][BONUS_TIME] -= 1
                if self.bonus_code_matrix[code][BONUS_TIME] == 0:
                    self.bonus_code_matrix[code][IS_ACTIVATED] = False
                    if self.bonus_code_matrix[code][CODE_TYPE] == 'exp_bonus':
                        self.controller.parent_controller.on_deactivate_exp_bonus_code()
                    elif self.bonus_code_matrix[code][CODE_TYPE] == 'money_bonus':
                        self.controller.parent_controller.on_deactivate_money_bonus_code()
