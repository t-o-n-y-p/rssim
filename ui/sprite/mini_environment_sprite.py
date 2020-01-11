from logging import getLogger

from database import USER_DB_CURSOR
from ui import *
from ui.sprite import UISprite
from textures import get_full_map_e


@final
class MiniEnvironmentSprite(UISprite):
    def __init__(self, map_id, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.mini_environment_sprite'),
                         parent_viewport=parent_viewport)
        self.map_id = map_id
        USER_DB_CURSOR.execute('''SELECT unlocked_environment FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.texture = get_full_map_e(map_id=self.map_id, tiers=USER_DB_CURSOR.fetchone()[0])
        self.batch = BATCHES['mini_map_batch']
        self.group = GROUPS['mini_environment']
        self.usage = 'static'

    def get_position(self):
        return get_mini_map_position(self.screen_resolution)

    def get_scale(self):
        return get_mini_map_width(self.screen_resolution) / MAP_WIDTH

    def on_unlock_environment(self, tier):
        self.on_update_texture(get_full_map_e(map_id=self.map_id, tiers=tier))
