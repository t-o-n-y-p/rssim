from typing import final

from database import CONFIG_DB_CURSOR, USER_DB_CURSOR
from ui import get_map_tracks, GROUPS, BATCHES

from ui.sprite_v2 import MapSpriteV2


@final
class MainMapSpriteV2(MapSpriteV2):
    def __init__(self, logger, parent_viewport, map_id):
        super().__init__(logger, parent_viewport, map_id)
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute(
            '''SELECT unlocked_tracks_by_default FROM map_progress_config WHERE map_id = ?''', (self.map_id, )
        )
        self.unlocked_tracks_by_default = CONFIG_DB_CURSOR.fetchone()[0]
        self.texture = get_map_tracks(
            map_id=self.map_id, tracks=max(self.unlocked_tracks, self.unlocked_tracks_by_default)
        )
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']
        CONFIG_DB_CURSOR.execute(
            '''SELECT map_sprite_y FROM track_config WHERE map_id = ? AND track_number = ?''',
            (self.map_id, self.unlocked_tracks)
        )
        self.y = CONFIG_DB_CURSOR.fetchone()[0]

    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        CONFIG_DB_CURSOR.execute(
            '''SELECT map_sprite_y FROM track_config WHERE map_id = ? AND track_number = ?''',
            (self.map_id, self.unlocked_tracks)
        )
        self.on_position_update(y=CONFIG_DB_CURSOR.fetchone()[0])
        self.on_update_texture(
            get_map_tracks(map_id=self.map_id, tracks=max(self.unlocked_tracks, self.unlocked_tracks_by_default))
        )
