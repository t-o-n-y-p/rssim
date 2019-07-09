from logging import getLogger

from controller import *


class FPSController(Controller):
    def __init__(self, app_controller):
        super().__init__(parent_controller=app_controller, logger=getLogger('root.app.fps.controller'))

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_update_fps(self, fps):
        self.model.on_update_fps(fps)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    def on_update_display_fps(self, display_fps):
        self.model.on_update_display_fps(display_fps)
        if display_fps:
            self.fade_out_animation.on_deactivate()
            self.fade_in_animation.on_activate()
        else:
            self.fade_in_animation.on_deactivate()
            self.fade_out_animation.on_activate()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
