from logging import getLogger

from ui.fade_animation.fade_in_animation import *


@final
class AppFadeInAnimation(FadeInAnimation):
    def __init__(self, app_view):
        super().__init__(animation_object=app_view, logger=getLogger('root.app.fade_in_animation'))
        self.main_menu_fade_in_animation = None
        self.license_fade_in_animation = None
        self.onboarding_fade_in_animation = None
        self.game_fade_in_animation = None
        self.settings_fade_in_animation = None
        self.bonus_code_activation_fade_in_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.main_menu_fade_in_animation.on_activate()
