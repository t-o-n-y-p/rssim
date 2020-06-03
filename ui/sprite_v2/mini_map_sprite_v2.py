from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR, USER_DB_CURSOR
from ui import get_map_tracks, MAP_WIDTH, get_mini_map_width, GROUPS, BATCHES, get_mini_map_y, get_mini_map_x

from ui.sprite_v2 import UISpriteV2


@final
class MiniMapSpriteV2(UISpriteV2):
    def __init__(self, map_id, parent_viewport):
        super().__init__(
            logger=getLogger(f'root.app.game.map.{map_id}.mini_map_sprite'), parent_viewport=parent_viewport
        )
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute(
            '''SELECT unlocked_tracks_by_default FROM map_progress_config WHERE map_id = ?''', (self.map_id, )
        )
        self.unlocked_tracks_by_default = CONFIG_DB_CURSOR.fetchone()[0]
        self.texture = get_map_tracks(
            map_id=self.map_id, tracks=max(self.unlocked_tracks, self.unlocked_tracks_by_default)
        )
        CONFIG_DB_CURSOR.execute(
            '''SELECT map_sprite_y FROM track_config WHERE map_id = ? AND track_number = ?''',
            (self.map_id, self.unlocked_tracks)
        )
        self.y_margin = CONFIG_DB_CURSOR.fetchone()[0]
        self.batch = BATCHES['mini_map_batch']
        self.group = GROUPS['mini_map']
        self.usage = 'static'

    def get_x(self):
        return self.parent_viewport.x1

    def get_y(self):
        return self.parent_viewport.y1 + self.y_margin * self.get_scale()

    def get_scale(self):
        return (self.parent_viewport.x2 - self.parent_viewport.x1) / MAP_WIDTH

    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        self.on_update_texture(get_map_tracks(map_id=self.map_id, tracks=max(track, self.unlocked_tracks_by_default)))
        CONFIG_DB_CURSOR.execute(
            '''SELECT map_sprite_y FROM track_config WHERE map_id = ? AND track_number = ?''',
            (self.map_id, self.unlocked_tracks)
        )
        if self.y_margin != (new_margin := CONFIG_DB_CURSOR.fetchone()[0]):
            self.y_margin = new_margin
            self.on_position_update()
