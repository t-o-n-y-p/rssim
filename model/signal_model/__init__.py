from logging import getLogger

from model import *
from database import USER_DB_CURSOR


class SignalModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, track, base_route):
        super().__init__(controller, view, map_id,
                         logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.model'))
        self.track = track
        self.base_route = base_route
        USER_DB_CURSOR.execute('''SELECT state, locked FROM signals 
                                  WHERE track = ? AND base_route = ? AND map_id = ?''',
                               (self.track, self.base_route, self.map_id))
        self.state, self.locked = USER_DB_CURSOR.fetchone()
        self.locked = bool(self.locked)

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE signals SET state = ?, locked = ? 
                                  WHERE track = ? AND base_route = ? AND map_id = ?''',
                               (self.state, int(self.locked), self.track, self.base_route, self.map_id))

    @final
    def on_switch_to_green(self):
        self.state = 'green_signal'
        self.view.on_change_state(self.state)

    @final
    def on_switch_to_red(self):
        self.state = 'red_signal'
        self.view.on_change_state(self.state)
