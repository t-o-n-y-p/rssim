from logging import getLogger

from controller import *
from model.fps_model import FPSModel
from view.fps_view import FPSView
from ui.fade_animation.fade_in_animation.fps_fade_in_animation import FPSFadeInAnimation
from ui.fade_animation.fade_out_animation.fps_fade_out_animation import FPSFadeOutAnimation


@final
class FPSController(AppBaseController):
    def __init__(self, app_controller):
        super().__init__(parent_controller=app_controller, logger=getLogger('root.app.fps.controller'))
        self.view = FPSView(controller=self)
        self.model = FPSModel(controller=self, view=self.view)
        self.fade_in_animation = FPSFadeInAnimation(self.view)
        self.fade_out_animation = FPSFadeOutAnimation(self.view)
        self.view.on_init_content()

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
