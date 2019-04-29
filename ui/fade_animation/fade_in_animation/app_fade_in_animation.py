from logging import getLogger

from ui.fade_animation.fade_in_animation import *
from database import USER_DB_CURSOR


class AppFadeInAnimation(FadeInAnimation):
    """
    Implements fade-in animation for App view.
    """
    def __init__(self, app_controller):
        """
        Properties:
            main_menu_fade_in_animation         fade-in animation for main menu view
            license_fade_in_animation           fade-in animation for license view
            game_fade_in_animation              fade-in animation for game view
            settings_fade_in_animation          fade-in animation for settings view
            fps_fade_in_animation               fade-in animation for FPS view

        :param app_controller:                  App controller
        """
        super().__init__(animation_object=app_controller, logger=getLogger('root.app.fade_in_animation'))
        self.main_menu_fade_in_animation = None
        self.license_fade_in_animation = None
        self.game_fade_in_animation = None
        self.settings_fade_in_animation = None
        self.fps_fade_in_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        """
        Activates the animation and initializes opacity chart position.
        """
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.main_menu_fade_in_animation.on_activate()
        # activate FPS animation only if FPS monitor is enabled
        USER_DB_CURSOR.execute('SELECT display_fps FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]):
            self.fps_fade_in_animation.on_activate()
