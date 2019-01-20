from controller import *


class CrossoverController(Controller):
    def __init__(self, map_controller):
        super().__init__(parent_controller=map_controller)
        self.track_param_1 = None
        self.track_param_2 = None
        self.crossover_type = None

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

    def on_save_state(self):
        self.model.on_save_state()

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_force_busy_on(self, positions, train_id):
        self.model.on_force_busy_on(positions, train_id)

    def on_force_busy_off(self, positions):
        self.model.on_force_busy_off(positions)
