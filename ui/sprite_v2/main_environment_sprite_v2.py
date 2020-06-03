from logging import getLogger
from typing import final

from database import USER_DB_CURSOR
from ui import get_map_environment_primary, GROUPS, BATCHES

from ui.sprite_v2 import MapSpriteV2


@final
class MainEnvironmentSpriteV2(MapSpriteV2):
    def __init__(self, map_id, parent_viewport):
        super().__init__(
            map_id=map_id, logger=getLogger(f'root.app.game.map.{map_id}.main_environment_sprite'),
            parent_viewport=parent_viewport
        )
        USER_DB_CURSOR.execute('''SELECT unlocked_environment FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_environment = USER_DB_CURSOR.fetchone()[0]
        self.texture = get_map_environment_primary(map_id=self.map_id, tiers=self.unlocked_environment)
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['environment']

    def on_unlock_environment(self, tier):
        self.unlocked_environment = tier
        self.on_update_texture(get_map_environment_primary(map_id=self.map_id, tiers=self.unlocked_environment))
