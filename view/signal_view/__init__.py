from logging import getLogger

from view import *
from ui.sprite.signal_sprite import SignalSprite


class SignalView(View):
    def __init__(self, map_id, track, base_route):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.view'))
        self.map_id = map_id
        self.signal_sprite = SignalSprite(self.map_id, track, base_route, parent_viewport=self.viewport)
        self.state = 'red_signal'
        self.locked = True

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.signal_sprite.on_update_opacity(self.opacity)

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.signal_sprite.is_located_outside_viewport() and not self.locked:
            self.signal_sprite.create()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        self.signal_sprite.on_change_base_offset(self.base_offset)
        if self.signal_sprite.is_located_outside_viewport():
            self.signal_sprite.delete()
        elif not self.locked:
            self.signal_sprite.create()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        self.signal_sprite.on_change_scale(self.zoom_factor)

    def on_unlock(self):
        self.locked = False
        # this workaround is needed for signal to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)

    def on_change_state(self, state):
        self.state = state
        self.signal_sprite.on_change_state(self.state)
