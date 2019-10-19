from logging import getLogger

from controller import *


@final
class BonusCodeController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.bonus_code.controller'))

    def on_activate_new_bonus_code(self, sha512_hash):
        self.model.on_activate_new_bonus_code(sha512_hash)

    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

    def on_level_up(self, level):
        self.view.on_level_up(level)
