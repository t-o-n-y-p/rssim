from view import *


class TrainRouteView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups)
        self.base_offset = (-3456, -1688)
        self.screen_resolution = (1280, 720)
        self.zoom_out_activated = False
        self.zoom_factor = 1.0

    def on_update(self):
        pass

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
