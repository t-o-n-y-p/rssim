from logging import getLogger

from database import CONFIG_DB_CURSOR
from ui import *
from ui.sprite import MapSprite


class CrossoverSprite(MapSprite):
    def __init__(self, map_id, track_param_1, track_param_2, crossover_type, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.crossover_sprite'),
                         parent_viewport=parent_viewport)
        CONFIG_DB_CURSOR.execute('''SELECT offset_x, offset_y FROM crossovers_config
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                    AND map_id = ?''',
                                 (track_param_1, track_param_2, crossover_type, map_id))
        self.crossover_offset = CONFIG_DB_CURSOR.fetchone()
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']

    def get_position(self):
        return (self.base_offset[0] + int(self.crossover_offset[0] * self.scale),
                self.base_offset[1] + int(self.crossover_offset[1] * self.scale))