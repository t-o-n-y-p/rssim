from typing import final

from database import USER_DB_CURSOR
from ui import get_map_environment_primary, MAP_WIDTH, GROUPS, BATCHES

from ui.sprite_v2 import UISpriteV2


@final
class MiniEnvironmentSpriteV2(UISpriteV2):
    def __init__(self, logger, parent_viewport, map_id):
        super().__init__(logger, parent_viewport)
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_environment FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_environment = USER_DB_CURSOR.fetchone()[0]
        self.texture = get_map_environment_primary(map_id=self.map_id, tiers=self.unlocked_environment)
        self.batch = BATCHES['mini_map_batch']
        self.group = GROUPS['mini_environment']
        self.usage = 'static'

    def get_x(self):
        return self.parent_viewport.x1

    def get_y(self):
        return self.parent_viewport.y1

    def get_scale(self):
        return (self.parent_viewport.x2 - self.parent_viewport.x1) / MAP_WIDTH

    def on_unlock_environment(self, tier):
        self.unlocked_environment = tier
        self.on_update_texture(get_map_environment_primary(map_id=self.map_id, tiers=self.unlocked_environment))
