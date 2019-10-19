from logging import getLogger

from database import USER_DB_CURSOR
from ui import *
from ui.sprite import MapSprite
from textures import get_full_map


@final
class MainMapSprite(MapSprite):
    def __init__(self, map_id, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.main_map_sprite'),
                         parent_viewport=parent_viewport)
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        self.texture = get_full_map(map_id=self.map_id, tracks=unlocked_tracks)
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']

    def get_position(self):
        return (self.base_offset[0],
                self.base_offset[1] + (MAP_HEIGHT - self.texture.height) // round(2 / self.scale))

    def on_unlock_track(self, track):
        self.on_update_texture(get_full_map(map_id=self.map_id, tracks=track))
        self.on_position_changed()
