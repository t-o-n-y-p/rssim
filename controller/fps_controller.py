from logging import getLogger

from controller import *


class FPSController(Controller):
    def __init__(self, app_controller):
        super().__init__(parent_controller=app_controller, logger=getLogger('root.app.fps.controller'))

    def on_update_view(self):
        self.view.on_update()

    @controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    @controller_is_active
    def on_update_fps(self, fps):
        self.model.on_update_fps(fps)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
