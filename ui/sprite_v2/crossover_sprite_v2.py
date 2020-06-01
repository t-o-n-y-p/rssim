from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR
from ui import GROUPS, BATCHES

from ui.sprite_v2 import MapSpriteV2


@final
class CrossoverSpriteV2(MapSpriteV2):
    def __init__(self, map_id, track_param_1, track_param_2, crossover_type, parent_viewport):
        super().__init__(
            map_id=map_id, logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.crossover_sprite'
            ), parent_viewport=parent_viewport
        )
        CONFIG_DB_CURSOR.execute(
            '''SELECT offset_x, offset_y FROM crossovers_config
            WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? AND map_id = ?''',
            (track_param_1, track_param_2, crossover_type, self.map_id)
        )
        self.x, self.y = CONFIG_DB_CURSOR.fetchone()
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']
