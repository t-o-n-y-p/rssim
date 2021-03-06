from abc import ABC
from logging import getLogger
from typing import final

from database import USER_DB_CURSOR
from ui.sprite.signal_sprite import SignalSprite
from view import MapBaseView, view_is_not_active


class SignalView(MapBaseView, ABC):
    def __init__(self, controller, map_id, track, base_route):
        super().__init__(
            controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.view')
        )
        self.track, self.base_route = track, base_route
        self.signal_sprite = SignalSprite(self.map_id, self.track, self.base_route, parent_viewport=self.viewport)
        USER_DB_CURSOR.execute(
            '''SELECT state, locked FROM signals WHERE track = ? AND base_route = ? AND map_id = ?''',
            (self.track, self.base_route, self.map_id)
        )
        self.state, self.locked = USER_DB_CURSOR.fetchone()
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.signal_sprite.is_located_outside_viewport() and not self.locked:
            self.signal_sprite.create()

    @final
    def on_update(self):
        if self.signal_sprite.is_located_outside_viewport():
            self.signal_sprite.delete()
        elif not self.locked:
            self.signal_sprite.create()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.signal_sprite.on_update_opacity(self.opacity)

    @final
    def on_change_state(self, state):
        self.state = state
        self.signal_sprite.on_change_state(self.state)
