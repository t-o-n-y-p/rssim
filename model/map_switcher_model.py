from logging import getLogger

from model import *
from database import MAP_SWITCHER_STATE_MATRIX


@final
class MapSwitcherModel(GameBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.game.map_switcher.model'))
        self.map_switcher_state_matrix = MAP_SWITCHER_STATE_MATRIX
        USER_DB_CURSOR.execute('SELECT map_id FROM graphics')
        self.currently_selected_map = USER_DB_CURSOR.fetchone()[0]

    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE graphics SET map_id = ?''', (self.currently_selected_map, ))

    def on_switch_map(self, new_map_id):
        self.currently_selected_map = new_map_id
