from logging import getLogger

from controller import *


class BonusCodeController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.bonus_code.controller'))

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_save_state(self):
        self.model.on_save_state()

    def on_activate_new_bonus_code(self, sha512_hash):
        self.model.on_activate_new_bonus_code(sha512_hash)

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)

    def on_update_time(self, game_time):
        self.model.on_update_time(game_time)

    def on_level_up(self, level):
        self.view.on_level_up(level)