from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class BonusCodeManagerFadeInAnimation(FadeInAnimation):
    def __init__(self, bonus_code_manager_view):
        super().__init__(animation_object=bonus_code_manager_view,
                         logger=getLogger('root.app.game.bonus_code_manager.fade_in_animation'))
