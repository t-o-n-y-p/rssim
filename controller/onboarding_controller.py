from logging import getLogger

from controller import *


class OnboardingController(Controller):
    def __init__(self, app):
        """
        :param app:                     App controller (parent controller)
        """
        super().__init__(parent_controller=app, logger=getLogger('root.app.onboarding.controller'))

    def on_update_view(self):
        """
        Notifies the view and fade-in/fade-out animations.
        """
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)

    def on_activate_view(self):
        """
        Activates the view if user opened onboarding screen in the app.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view if user closed onboarding screen. Notifies the model to turn off onboarding.
        """
        self.view.on_deactivate()
        self.model.on_save_and_commit_onboarding_state()

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()

    def on_update_fade_animation_state(self, new_state):
        """
        Notifies fade-in/fade-out animations about state update.

        :param new_state:                       indicates if fade animations were enabled or disabled
        """
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)