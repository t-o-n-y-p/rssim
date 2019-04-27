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

        :param app:          App controller (parent controller)
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

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Settings object: controller and model. Model activates the view if necessary.
        Determines which screen was activated before.
        """
        self.is_activated = True
        self.model.on_activate()
        self.parent_controller.on_deactivate_current_view()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Settings object: controller, view and model.
        Activates view which was activated before settings screen.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        if self.navigated_from_main_menu:
            self.navigated_from_main_menu = False

        if self.navigated_from_game:
            self.navigated_from_game = False
            self.parent_controller.game_to_settings_transition_animation.on_deactivate()
            self.parent_controller.settings_to_game_transition_animation.on_activate()

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

    def on_update_fade_animation_state(self, new_state):
        """
        Notifies fade-in/fade-out animations about state update.

        :param new_state:                       indicates if fade animations were enabled or disabled
        """
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
