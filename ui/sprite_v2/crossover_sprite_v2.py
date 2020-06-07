from typing import final

from database import CONFIG_DB_CURSOR, USER_DB_CURSOR
from ui import GROUPS, BATCHES, SWITCHES_DIVERGING, SWITCHES_STRAIGHT

from ui.sprite_v2 import MapSpriteV2


@final
class CrossoverSpriteV2(MapSpriteV2):
    def __init__(self, logger, parent_viewport, map_id, track_param_1, track_param_2, crossover_type):
        super().__init__(logger, parent_viewport, map_id)
        CONFIG_DB_CURSOR.execute(
            '''SELECT offset_x, offset_y FROM crossovers_config
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (track_param_1, track_param_2, crossover_type, self.map_id)
        )
        self.x, self.y = CONFIG_DB_CURSOR.fetchone()
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']
        CONFIG_DB_CURSOR.execute(
            '''SELECT region_x, region_y, region_w, region_h FROM crossovers_config
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (track_param_1, track_param_2, crossover_type, self.map_id)
        )
        self.crossover_region = CONFIG_DB_CURSOR.fetchone()
        self.textures = [
            SWITCHES_STRAIGHT.get_region(*self.crossover_region),
            SWITCHES_DIVERGING.get_region(*self.crossover_region)
        ]
        USER_DB_CURSOR.execute(
            '''SELECT current_position_1, current_position_2 FROM crossovers 
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (track_param_1, track_param_2, crossover_type, self.map_id)
        )
        current_position_1, current_position_2 = USER_DB_CURSOR.fetchone()
        self.texture = self.textures[int(current_position_1 == current_position_2)]

    def on_current_position_update(self, current_position_1, current_position_2):
        self.on_update_texture(self.textures[int(current_position_1 == current_position_2)])
