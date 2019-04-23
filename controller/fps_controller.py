from logging import getLogger

from controller import *


class FPSController(Controller):
    """
    Implements FPS controller.
    FPS object is responsible for real-time FPS calculation.
    """
    def __init__(self, app_controller):
        """
        :param app_controller:          App controller (parent controller)
        """
        super().__init__(parent_controller=app_controller, logger=getLogger('root.app.fps.controller'))

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
        Activates FPS object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates FPS object: controller, view and model.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    @controller_is_active
    def on_update_fps(self, fps):
        """
        Notifies the model about FPS value update.

        :param fps:                     new FPS value
        """
        self.model.on_update_fps(fps)

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

    def on_update_display_fps(self, display_fps):
        """
        Notifies the model about display_fps flag value update.

        :param display_fps:                     new flag value
        """
        self.model.on_update_display_fps(display_fps)
        if display_fps:
            self.fade_out_animation.on_deactivate()
            self.fade_in_animation.on_activate()
        else:
            self.fade_in_animation.on_deactivate()
            self.fade_out_animation.on_activate()
