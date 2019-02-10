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
        self.logger.info('START INIT')
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates FPS object: controller and model. Model activates the view if necessary.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates FPS object: controller, view and model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    @controller_is_active
    def on_update_fps(self, fps):
        """
        Notifies the model about FPS value update.

        :param fps:                     new FPS value
        """
        self.logger.info('START ON_UPDATE_FPS')
        self.model.on_update_fps(fps)
        self.logger.info('END ON_UPDATE_FPS')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.view.on_change_screen_resolution(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')
