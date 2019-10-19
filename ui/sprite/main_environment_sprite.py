from logging import getLogger

from database import USER_DB_CURSOR
from ui import *
from ui.sprite import MapSprite
from textures import get_full_map_e


@final
class MainEnvironmentSprite(MapSprite):
    def __init__(self, map_id, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.main_environment_sprite'),
                         parent_viewport=parent_viewport)
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_environment FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        unlocked_environment = USER_DB_CURSOR.fetchone()[0]
        self.texture = get_full_map_e(map_id=self.map_id, tiers=unlocked_environment)
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['environment']

    def get_position(self):
        return self.base_offset

    def on_unlock_environment(self, tier):
        self.on_update_texture(get_full_map_e(map_id=self.map_id, tiers=tier))
