from logging import getLogger

from controller import *


@final
class BonusCodeManagerController(AppBaseController, GameBaseController):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller, logger=getLogger('root.app.bonus_code_manager.controller'))

    def on_activate_new_bonus_code(self, sha512_hash):
        self.model.on_activate_new_bonus_code(sha512_hash)

    def on_change_bonus_expired_notification_state(self, notification_state):
        self.view.on_change_bonus_expired_notification_state(notification_state)
