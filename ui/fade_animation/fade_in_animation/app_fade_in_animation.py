from logging import getLogger

from ui.fade_animation.fade_in_animation import *
from database import USER_DB_CURSOR


class AppFadeInAnimation(FadeInAnimation):
    def __init__(self, app_controller):
        super().__init__(animation_object=app_controller, logger=getLogger('root.app.fade_in_animation'))
        self.main_menu_fade_in_animation = None
        self.license_fade_in_animation = None
        self.onboarding_fade_in_animation = None
        self.game_fade_in_animation = None
        self.settings_fade_in_animation = None
        self.fps_fade_in_animation = None
        self.bonus_code_fade_in_animation = None

    @fade_animation_needed
    @fade_animation_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.current_opacity_chart_index = self.opacity_chart.index(self.animation_object.view.opacity)
        self.animation_object.on_activate_view()
        self.main_menu_fade_in_animation.on_activate()
        # activate FPS animation only if FPS monitor is enabled
        USER_DB_CURSOR.execute('SELECT display_fps FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]):
            self.fps_fade_in_animation.on_activate()
