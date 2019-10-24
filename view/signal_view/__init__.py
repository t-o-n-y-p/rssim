from logging import getLogger

from view import *
from ui.sprite.signal_sprite import SignalSprite


class SignalView(MapBaseView):
    def __init__(self, map_id, track, base_route):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.view'))
        self.map_id = map_id
        self.signal_sprite = SignalSprite(self.map_id, track, base_route, parent_viewport=self.viewport)
        USER_DB_CURSOR.execute('''SELECT state, locked FROM signals 
                                  WHERE track = ? AND base_route = ? AND map_id = ?''',
                               (track, base_route, self.map_id))
        self.state, self.locked = USER_DB_CURSOR.fetchone()
        self.locked = bool(self.locked)

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.signal_sprite.is_located_outside_viewport() and not self.locked:
            self.signal_sprite.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.signal_sprite.on_update_opacity(self.opacity)

    @final
    def on_change_base_offset(self, new_base_offset):
        super().on_change_base_offset(new_base_offset)
        self.signal_sprite.on_change_base_offset(self.base_offset)
        if self.signal_sprite.is_located_outside_viewport():
            self.signal_sprite.delete()
        elif not self.locked:
            self.signal_sprite.create()

    @final
    def on_change_scale(self, zoom_factor):
        super().on_change_scale(zoom_factor)
        self.signal_sprite.on_change_scale(self.zoom_factor)

    @final
    def on_change_state(self, state):
        self.state = state
        self.signal_sprite.on_change_state(self.state)
