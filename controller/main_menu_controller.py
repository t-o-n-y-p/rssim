from logging import getLogger

from controller import *


@final
class MainMenuController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.main_menu.controller'))

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
