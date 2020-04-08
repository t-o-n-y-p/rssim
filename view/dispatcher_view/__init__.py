from abc import ABC
from logging import getLogger
from typing import final

from view import MapBaseView, view_is_not_active, view_is_active


class DispatcherView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.view'))
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
