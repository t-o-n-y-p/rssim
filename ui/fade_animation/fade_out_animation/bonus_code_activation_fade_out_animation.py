from logging import getLogger
from typing import final

from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class BonusCodeActivationFadeOutAnimation(FadeOutAnimation):
    def __init__(self, bonus_code_activation_view):
        super().__init__(
            animation_object=bonus_code_activation_view,
            logger=getLogger('root.app.bonus_code_activation.fade_out_animation')
        )
