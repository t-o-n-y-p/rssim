from logging import getLogger
from typing import final

from database import USER_DB_CURSOR
from ui import get_map_environment_primary, MAP_WIDTH, get_mini_map_width, GROUPS, BATCHES, \
    get_mini_map_x, get_mini_map_y

from ui.sprite_v2 import UISpriteV2


@final
class MiniEnvironmentSpriteV2(UISpriteV2):
    def __init__(self, map_id, parent_viewport):
        super().__init__(
            logger=getLogger(f'root.app.game.map.{map_id}.mini_environment_sprite'),
            parent_viewport=parent_viewport
        )
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_environment FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_environment = USER_DB_CURSOR.fetchone()[0]
        self.texture = get_map_environment_primary(map_id=self.map_id, tiers=self.unlocked_environment)
        self.batch = BATCHES['mini_map_batch']
        self.group = GROUPS['mini_environment']
        self.usage = 'static'

    def get_x(self):
        return get_mini_map_x(self.screen_resolution)

    def get_y(self):
        return get_mini_map_y(self.screen_resolution)

    def get_scale(self):
        return get_mini_map_width(self.screen_resolution) / MAP_WIDTH

    def on_unlock_environment(self, tier):
        self.unlocked_environment = tier
        if self.texture:
            self.on_update_texture(get_map_environment_primary(map_id=self.map_id, tiers=self.unlocked_environment))
