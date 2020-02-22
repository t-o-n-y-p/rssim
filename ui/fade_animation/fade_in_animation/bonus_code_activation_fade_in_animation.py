from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class BonusCodeActivationFadeInAnimation(FadeInAnimation):
    def __init__(self, bonus_code_activation_view):
        super().__init__(animation_object=bonus_code_activation_view,
                         logger=getLogger('root.app.bonus_code_activation.fade_in_animation'))
