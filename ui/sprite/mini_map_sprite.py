from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR, USER_DB_CURSOR
from ui import get_map_tracks, MAP_WIDTH, get_mini_map_width, MAP_HEIGHT, get_mini_map_position, GROUPS, BATCHES

from ui.sprite import UISprite


@final
class MiniMapSprite(UISprite):
    def __init__(self, map_id, parent_viewport):
        super().__init__(
            logger=getLogger(f'root.app.game.map.{map_id}.mini_map_sprite'), parent_viewport=parent_viewport
        )
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute(
            '''SELECT unlocked_tracks_by_default FROM map_progress_config WHERE map_id = ?''', (self.map_id, )
        )
        self.unlocked_tracks_by_default = CONFIG_DB_CURSOR.fetchone()[0]
        self.texture = get_map_tracks(map_id=self.map_id, tracks=max(unlocked_tracks, self.unlocked_tracks_by_default))
        self.batch = BATCHES['mini_map_batch']
        self.group = GROUPS['mini_map']
        self.usage = 'static'

    def get_position(self):
        return (
            get_mini_map_position(self.screen_resolution)[0],
            get_mini_map_position(self.screen_resolution)[1]
            + int((MAP_HEIGHT - self.texture.height) // 2 * get_mini_map_width(self.screen_resolution) / MAP_WIDTH)
        )

    def get_scale(self):
        return get_mini_map_width(self.screen_resolution) / MAP_WIDTH

    def on_unlock_track(self, track):
        self.on_update_texture(get_map_tracks(map_id=self.map_id, tracks=max(track, self.unlocked_tracks_by_default)))
        self.on_position_changed()
