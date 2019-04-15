from sys import exit
from logging import getLogger

from controller import *


class AppController(Controller):
    """
    Implements App controller.
    App object is responsible for high-level properties, UI and events.
    """
    def __init__(self, loader):
        """
        Properties:
            game                        Game object controller
            settings                    Settings object controller
            fps                         FPS object controller
            loader                      RSSim class instance

        :param loader:                  RSSim class instance
        """
        super().__init__(logger=getLogger('root.app.controller'))
        self.main_menu = None
        self.game = None
        self.settings = None
        self.fps = None
        self.loader = loader

    def on_update_view(self):
        """
        Notifies the view, Game view and Settings view to update fade-in/fade-out animations.
        """
        self.view.on_update()
        self.main_menu.on_update_view()
        self.game.on_update_view()
        self.settings.on_update_view()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates App object: controller and model. Model activates the view if necessary.
        When App object is activated, we also activate Game object
        (because game process is started right away) and FPS object (to display FPS counter).
        """
        self.is_activated = True
        self.model.on_activate()
        self.main_menu.on_activate()
        self.game.on_activate()
        self.fps.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates App object: controller, view and model. Also deactivates all child objects.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.main_menu.on_deactivate()
        self.game.on_deactivate()
        self.settings.on_deactivate()
        self.fps.on_deactivate()

    def on_fullscreen_button_click(self):
        """
        Handles Fullscreen button being clicked on.
        We need to apply new screen resolution and switch app window mode to fullscreen
        (if fullscreen mode is available for user display).
        """
        self.on_change_screen_resolution(self.model.fullscreen_resolution)
        if self.model.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_on()

    def on_restore_button_click(self):
        """
        Handles Restore button being clicked on.
        We need to apply new screen resolution and switch app window mode to windowed.
        """
        self.on_fullscreen_mode_turned_off()
        self.on_change_screen_resolution(self.settings.model.windowed_resolution)

    def on_fullscreen_mode_turned_on(self):
        """
        Notifies the model to make the game fullscreen.
        Note that adjusting screen resolution is made by on_change_screen_resolution handler,
        this function only switches the app window mode.
        """
        self.model.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        """
        Notifies the model to make the game windowed.
        Note that adjusting screen resolution is made by on_change_screen_resolution handler,
        this function only switches the app window mode.
        """
        self.model.on_fullscreen_mode_turned_off()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view and all child controllers about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)
        self.main_menu.on_change_screen_resolution(screen_resolution)
        self.game.on_change_screen_resolution(screen_resolution)
        self.settings.on_change_screen_resolution(screen_resolution)
        self.fps.on_change_screen_resolution(screen_resolution)

    def on_close_game(self):
        """
        Handles Close button being clicked on.
        Here we deactivate the app, notify game controller to save game progress and close the app window.
        """
        self.on_deactivate()
        self.game.on_save_and_commit_state()
        exit()

    def on_activate_main_menu_view(self):
        """
        Notifies Game controller to activate the main menu screen
        in case the settings screen was opened from main menu screen and then user closes settings screen.
        """
        self.main_menu.on_activate_view()

    def on_activate_game_view(self):
        """
        Notifies Game controller to activate the game screen
        in case the settings screen was opened from game screen and then user closes settings screen.
        """
        self.game.on_activate_view()

    def on_deactivate_current_view(self):
        """
        Determines where the user is located when Open settings button was clicked on:
        either game screen or main menu screen.
        Corresponding flag is enabled for Settings controller.
        """
        if self.game.view.is_activated:
            self.game.on_deactivate_view()
            self.settings.navigated_from_game = True
        elif self.main_menu.view.is_activated:
            self.main_menu.on_deactivate_view()
            self.settings.navigated_from_main_menu = True

    def on_activate_open_settings_button(self):
        """
        Activates Open settings button back when user closes settings screen.
        """
        self.view.open_settings_button.on_activate()

    def on_update_fps(self, fps):
        """
        Notifies FPS controller about FPS value update.

        :param fps:                     new FPS value
        """
        self.fps.on_update_fps(fps)

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()
        self.settings.on_apply_shaders_and_draw_vertices()
        self.game.on_apply_shaders_and_draw_vertices()

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.model.on_save_and_commit_locale(new_locale)
        self.view.on_update_current_locale(new_locale)
        self.main_menu.on_update_current_locale(new_locale)
        self.game.on_update_current_locale(new_locale)
        self.settings.on_update_current_locale(new_locale)
        self.fps.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        """
        Disables system notifications for the view and all child controllers.
        """
        self.view.on_disable_notifications()
        self.game.on_disable_notifications()
        self.settings.on_disable_notifications()
        self.fps.on_disable_notifications()

    def on_enable_notifications(self):
        """
        Enables system notifications for the view and all child controllers.
        """
        self.view.on_enable_notifications()
        self.game.on_enable_notifications()
        self.settings.on_enable_notifications()
        self.fps.on_enable_notifications()

    def on_append_notification(self, notification):
        """
        When notification is triggered in background, it is added to the list.
        Then, after app is activated, these notifications are destroyed.

        :param notification:                    notification object
        """
        self.loader.notifications.append(notification)

    def on_change_level_up_notification_state(self, notification_state):
        """
        Notifies the Game controller about level up notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.game.on_change_level_up_notification_state(notification_state)

    def on_change_feature_unlocked_notification_state(self, notification_state):
        """
        Notifies the Game controller about feature unlocked notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.game.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        """
        Notifies the Game controller about construction completed notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.game.on_change_construction_completed_notification_state(notification_state)

    def on_change_enough_money_notification_state(self, notification_state):
        """
        Notifies the Game controller about enough money notification state update.

        :param notification_state:              new notification state defined by player
        """
        self.game.on_change_enough_money_notification_state(notification_state)

    def on_resume_game(self):
        self.game.on_resume_game()
