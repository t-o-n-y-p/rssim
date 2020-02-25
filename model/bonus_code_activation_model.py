from logging import getLogger

from model import *
from database import on_commit


@final
class BonusCodeActivationModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.bonus_code_activation.model'))
        USER_DB_CURSOR.execute('''SELECT bonus_codes_abuse_counter FROM game_progress''')
        self.bonus_code_abuse_counter = USER_DB_CURSOR.fetchone()[0]

    def on_increment_bonus_code_abuse_counter(self, value):
        self.bonus_code_abuse_counter += value
        self.on_save_and_commit_bonus_code_abuse_counter()
        if self.bonus_code_abuse_counter >= ALLOWED_BONUS_CODE_INPUT:
            self.controller.parent_controller.on_close_bonus_code()
            self.controller.parent_controller.on_save_and_commit_bonus_code_abuse()

    def on_reset_bonus_code_abuse_counter(self):
        self.bonus_code_abuse_counter = 0
        self.on_save_and_commit_bonus_code_abuse_counter()

    def on_save_and_commit_bonus_code_abuse_counter(self):
        USER_DB_CURSOR.execute('''UPDATE game_progress SET bonus_codes_abuse_counter = ?''',
                               (self.bonus_code_abuse_counter, ))
        on_commit()
