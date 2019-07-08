from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class AppFadeOutAnimation(FadeOutAnimation):
    def __init__(self, app_controller):
        super().__init__(animation_object=app_controller, logger=getLogger('root.app.fade_out_animation'))
        self.main_menu_fade_out_animation = None
        self.license_fade_out_animation = None
        self.onboarding_fade_out_animation = None
        self.game_fade_out_animation = None
        self.settings_fade_out_animation = None
        self.fps_fade_out_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_deactivate_view()
        self.main_menu_fade_out_animation.on_activate()
        self.license_fade_out_animation.on_activate()
        self.onboarding_fade_out_animation.on_activate()
        self.game_fade_out_animation.on_activate()
        self.settings_fade_out_animation.on_activate()
        self.fps_fade_out_animation.on_activate()
