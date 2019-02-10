from logging import getLogger

from controller import *


class SignalController(Controller):
    def __init__(self, map_controller, track, base_route):
        super().__init__(parent_controller=map_controller,
                         logger=getLogger(f'root.app.game.map.signal.{track}.{base_route}.controller'))
        self.track = track
        self.base_route = base_route

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

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_unlock(self):
        self.model.on_unlock()

    def on_save_state(self):
        self.model.on_save_state()

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_switch_to_green(self):
        self.model.on_switch_to_green()

    def on_switch_to_red(self):
        self.model.on_switch_to_red()
