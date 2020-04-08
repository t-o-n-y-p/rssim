from logging import getLogger
from typing import final

from controller import AppBaseController
from model.bonus_code_activation_model import BonusCodeActivationModel
from view.bonus_code_activation_view import BonusCodeActivationView
from ui.fade_animation.fade_in_animation.bonus_code_activation_fade_in_animation \
    import BonusCodeActivationFadeInAnimation
from ui.fade_animation.fade_out_animation.bonus_code_activation_fade_out_animation \
    import BonusCodeActivationFadeOutAnimation


@final
class BonusCodeActivationController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.bonus_code_activation.controller'))
        self.view = BonusCodeActivationView(controller=self)
        self.model = BonusCodeActivationModel(controller=self, view=self.view)
        self.fade_in_animation = BonusCodeActivationFadeInAnimation(self.view)
        self.fade_out_animation = BonusCodeActivationFadeOutAnimation(self.view)

    def on_increment_bonus_code_abuse_counter(self, value):
        self.model.on_increment_bonus_code_abuse_counter(value)

    def on_reset_bonus_code_abuse_counter(self):
        self.model.on_reset_bonus_code_abuse_counter()
