from logging import getLogger

from view import *


class TrainRouteView(View):
    def __init__(self, map_id, track, train_route):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.view'))
        self.map_id = map_id

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity

    @final
    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
