from logging import getLogger
from typing import final

from ui.fade_animation import fade_animation_needed, fade_animation_is_not_active
from ui.fade_animation.fade_out_animation import FadeOutAnimation


@final
class AppFadeOutAnimation(FadeOutAnimation):
    def __init__(self, app_view):
        super().__init__(animation_object=app_view, logger=getLogger('root.app.fade_out_animation'))
        self.main_menu_fade_out_animation = None
        self.license_fade_out_animation = None
        self.onboarding_fade_out_animation = None
        self.game_fade_out_animation = None
        self.settings_fade_out_animation = None
        self.bonus_code_activation_fade_out_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.main_menu_fade_out_animation.on_activate()
        self.license_fade_out_animation.on_activate()
        self.onboarding_fade_out_animation.on_activate()
        self.game_fade_out_animation.on_activate()
        self.settings_fade_out_animation.on_activate()
        self.bonus_code_activation_fade_out_animation.on_activate()
