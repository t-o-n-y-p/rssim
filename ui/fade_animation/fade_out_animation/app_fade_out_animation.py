from logging import getLogger

from ui.fade_animation.fade_out_animation import *


@final
class AppFadeOutAnimation(FadeOutAnimation):
    def __init__(self, app_controller):
        super().__init__(animation_object=app_controller, logger=getLogger('root.app.fade_out_animation'))
        self.main_menu_fade_out_animation = None
        self.license_fade_out_animation = None
        self.onboarding_fade_out_animation = None
        self.game_fade_out_animation = None
        self.settings_fade_out_animation = None
        self.fps_fade_out_animation = None
        self.bonus_code_fade_out_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        super().on_activate()
        self.main_menu_fade_out_animation.on_activate()
        self.license_fade_out_animation.on_activate()
        self.onboarding_fade_out_animation.on_activate()
        self.game_fade_out_animation.on_activate()
        self.settings_fade_out_animation.on_activate()
        self.fps_fade_out_animation.on_activate()
        self.bonus_code_fade_out_animation.on_activate()
