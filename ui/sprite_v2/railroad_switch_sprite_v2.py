from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR, USER_DB_CURSOR
from ui import GROUPS, BATCHES, SWITCHES_STRAIGHT, SWITCHES_DIVERGING

from ui.sprite_v2 import MapSpriteV2


@final
class RailroadSwitchSpriteV2(MapSpriteV2):
    def __init__(self, map_id, track_param_1, track_param_2, switch_type, parent_viewport):
        super().__init__(
            map_id, logger=getLogger(
                f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.railroad_switch_sprite'
            ), parent_viewport=parent_viewport)
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        CONFIG_DB_CURSOR.execute(
            '''SELECT offset_x, offset_y FROM switches_config
            WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?  AND map_id = ?''',
            (track_param_1, track_param_2, switch_type, map_id)
        )
        self.x, self.y = CONFIG_DB_CURSOR.fetchone()
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']
        CONFIG_DB_CURSOR.execute(
            '''SELECT region_x, region_y, region_w, region_h FROM switches_config
            WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? AND map_id = ?''',
            (self.track_param_1, self.track_param_2, switch_type, self.map_id)
        )
        self.switch_region = CONFIG_DB_CURSOR.fetchone()
        self.textures = [
            SWITCHES_STRAIGHT.get_region(*self.switch_region),
            SWITCHES_DIVERGING.get_region(*self.switch_region)
        ]
        USER_DB_CURSOR.execute(
            '''SELECT current_position FROM switches 
            WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? AND map_id = ?''',
            (self.track_param_1, self.track_param_2, switch_type, self.map_id)
        )
        self.texture = self.textures[int(USER_DB_CURSOR.fetchone()[0] == self.track_param_1)]

    def on_current_position_update(self, current_position):
        self.on_update_texture(self.textures[int(current_position == self.track_param_1)])
