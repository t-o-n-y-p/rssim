from logging import getLogger

from ui import *
from ui.sprite import MapSprite
from textures import get_full_map


@final
class MainMapSprite(MapSprite):
    def __init__(self, map_id, parent_viewport):
        super().__init__(map_id, logger=getLogger(f'root.app.game.map.{map_id}.main_map_sprite'),
                         parent_viewport=parent_viewport)
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute('''SELECT unlocked_tracks_by_default FROM map_progress_config WHERE map_id = ?''',
                                 (self.map_id, ))
        self.unlocked_tracks_by_default = CONFIG_DB_CURSOR.fetchone()[0]
        self.texture = get_full_map(map_id=self.map_id, tracks=max(unlocked_tracks, self.unlocked_tracks_by_default))
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']

    def get_position(self):
        return 0, (MAP_HEIGHT - self.texture.height) // 2

    def on_unlock_track(self, track):
        self.on_update_texture(get_full_map(map_id=self.map_id, tracks=max(track, self.unlocked_tracks_by_default)))
        self.on_position_changed()
