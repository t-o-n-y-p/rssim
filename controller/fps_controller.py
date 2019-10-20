from logging import getLogger

from controller import *


@final
class FPSController(AppBaseController):
    def __init__(self, app_controller):
        super().__init__(parent_controller=app_controller, logger=getLogger('root.app.fps.controller'))

    def on_update_fps(self, fps):
        self.model.on_update_fps(fps)

    def on_update_display_fps(self, display_fps):
        self.model.on_update_display_fps(display_fps)
        if display_fps:
            self.fade_out_animation.on_deactivate()
            self.fade_in_animation.on_activate()
        else:
            self.fade_in_animation.on_deactivate()
            self.fade_out_animation.on_activate()
