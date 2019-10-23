from logging import getLogger

from view import *


class DispatcherView(GameBaseView):
    def __init__(self, map_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.view'))
        self.map_id = map_id

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
