from logging import getLogger

from controller import *


class SettingsController(Controller):
    """
    Implements Settings controller.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self, app):
        """
        Properties:
            navigated_from_main_menu            indicates if settings screen was opened from main menu
            navigated_from_game                 indicates if settings screen was opened from game screen

        :param app:                             App controller (parent controller)
        """
        super().__init__(parent_controller=app, logger=getLogger('root.app.settings.controller'))
        self.navigated_from_main_menu = False
        self.navigated_from_game = False

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations.
        """
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the model about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)

    def on_save_and_commit_state(self):
        """
        Notifies the model to save user-defined settings to user progress database and commit.
        """
        self.model.on_save_and_commit_state()

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        """
        Disables system notifications for the view and all child controllers.
        """
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        """
        Enables system notifications for the view and all child controllers.
        """
        self.view.on_enable_notifications()

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()

    def on_activate_view(self):
        """
        Activates the view and Map controller if user opened game screen in the app.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_update_fade_animation_state(self, new_state):
        """
        Notifies fade-in/fade-out animations about state update.

        :param new_state:                       indicates if fade animations were enabled or disabled
        """
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)

    def on_update_clock_state(self, clock_24h_enabled):
        """
        Notifies the model about clock state update.

        :param clock_24h_enabled:               indicates if 24h clock is enabled
        """
        self.model.on_update_clock_state(clock_24h_enabled)
