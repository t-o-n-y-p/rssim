from logging import getLogger

from database import CONFIG_DB_CURSOR
from ui import *
from ui.sprite import MapSprite
from textures import RED_SIGNAL_IMAGE, GREEN_SIGNAL_IMAGE


class SignalSprite(MapSprite):
    def __init__(self, map_id, track, base_route, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.sprite'),
                         parent_viewport=parent_viewport)
        self.map_id = map_id
        self.texture = RED_SIGNAL_IMAGE
        CONFIG_DB_CURSOR.execute('''SELECT x, y, flip_needed FROM signal_config 
                                    WHERE track = ? AND base_route = ? AND map_id = ?''',
                                 (track, base_route, self.map_id))
        x, y, flip_needed = CONFIG_DB_CURSOR.fetchone()
        self.signal_offset = (x, y)
        if flip_needed:
            self.rotation = 180.0

        self.batch = BATCHES['main_batch']
        self.group = GROUPS['signal']

    def get_position(self):
        return (self.base_offset[0] + int(self.signal_offset[0] * self.scale),
                self.base_offset[1] + int(self.signal_offset[1] * self.scale))

    def on_change_state(self, state):
        if state == 'green_signal':
            self.on_update_texture(GREEN_SIGNAL_IMAGE)
        else:
            self.on_update_texture(RED_SIGNAL_IMAGE)