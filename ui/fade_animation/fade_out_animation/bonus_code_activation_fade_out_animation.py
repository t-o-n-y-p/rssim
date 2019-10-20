from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class BonusCodeActivationFadeOutAnimation(FadeOutAnimation):
    def __init__(self, bonus_code_activation_controller):
        super().__init__(animation_object=bonus_code_activation_controller,
                         logger=getLogger('root.app.bonus_code_activation.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
