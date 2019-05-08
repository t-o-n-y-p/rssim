from logging import getLogger

from ui.fade_animation.fade_out_animation import *


class AppFadeOutAnimation(FadeOutAnimation):
    """
    Implements fade-out animation for App view.
    """
    def __init__(self, app_controller):
        """
        Properties:
            main_menu_fade_out_animation        fade-out animation for main menu view
            license_fade_out_animation          fade-out animation for license view
            onboarding_fade_out_animation       fade-out animation for onboarding view
            game_fade_out_animation             fade-out animation for game view
            settings_fade_out_animation         fade-out animation for settings view
            fps_fade_out_animation              fade-out animation for FPS view

        :param app_controller:                  App controller
        """
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
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.main_menu_fade_out_animation.on_activate()
        self.license_fade_out_animation.on_activate()
        self.onboarding_fade_out_animation.on_activate()
        self.game_fade_out_animation.on_activate()
        self.settings_fade_out_animation.on_activate()
        self.fps_fade_out_animation.on_activate()
