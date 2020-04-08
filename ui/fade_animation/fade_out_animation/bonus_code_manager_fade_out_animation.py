from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class BonusCodeManagerFadeOutAnimation(FadeOutAnimation):
    def __init__(self, bonus_code_manager_view):
        super().__init__(
            animation_object=bonus_code_manager_view,
            logger=getLogger('root.app.game.bonus_code_manager.fade_out_animation')
        )
