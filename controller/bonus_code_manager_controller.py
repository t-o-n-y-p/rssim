from logging import getLogger

from controller import *
from model.bonus_code_manager_model import BonusCodeManagerModel
from view.bonus_code_manager_view import BonusCodeManagerView
from ui.fade_animation.fade_in_animation.bonus_code_manager_fade_in_animation import BonusCodeManagerFadeInAnimation
from ui.fade_animation.fade_out_animation.bonus_code_manager_fade_out_animation import BonusCodeManagerFadeOutAnimation


@final
class BonusCodeManagerController(GameBaseController):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller,
                         logger=getLogger('root.app.game.bonus_code_manager.controller'))
        self.view = BonusCodeManagerView(controller=self)
        self.model = BonusCodeManagerModel(controller=self, view=self.view)
        self.fade_in_animation = BonusCodeManagerFadeInAnimation(self.view)
        self.fade_out_animation = BonusCodeManagerFadeOutAnimation(self.view)

    def on_activate_new_bonus_code(self, sha512_hash):
        self.model.on_activate_new_bonus_code(sha512_hash)
