from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class BonusCodeActivationFadeInAnimation(FadeInAnimation):
    def __init__(self, bonus_code_activation_view):
        super().__init__(animation_object=bonus_code_activation_view,
                         logger=getLogger('root.app.bonus_code_activation.fade_in_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
