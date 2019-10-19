from logging import getLogger

from database import USER_DB_CURSOR
from ui import *
from ui.sprite import UISprite
from textures import get_full_map


@final
class MiniMapSprite(UISprite):
    def __init__(self, map_id, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.mini_map_sprite'),
                         parent_viewport=parent_viewport)
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        self.texture = get_full_map(map_id=self.map_id, tracks=unlocked_tracks)
        self.batch = BATCHES['mini_map_batch']
        self.group = GROUPS['mini_map']
        self.usage = 'static'

    def get_position(self):
        return (get_mini_map_position(self.screen_resolution)[0],
                get_mini_map_position(self.screen_resolution)[1]
                + int((MAP_HEIGHT - self.texture.height) // 2 * get_mini_map_width(self.screen_resolution) / MAP_WIDTH))

    def get_scale(self):
        return get_mini_map_width(self.screen_resolution) / MAP_WIDTH

    def on_unlock_track(self, track):
        self.on_update_texture(get_full_map(map_id=self.map_id, tracks=track))
        self.on_position_changed()
