from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class BonusCodeManagerFadeOutAnimation(FadeOutAnimation):
    def __init__(self, bonus_code_manager_view):
        super().__init__(animation_object=bonus_code_manager_view,
                         logger=getLogger('root.app.game.bonus_code_manager.fade_out_animation'))

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
