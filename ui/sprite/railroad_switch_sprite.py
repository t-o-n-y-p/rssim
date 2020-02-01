from logging import getLogger

from database import CONFIG_DB_CURSOR
from ui import *
from ui.sprite import MapSprite


@final
class RailroadSwitchSprite(MapSprite):
    def __init__(self, map_id, track_param_1, track_param_2, switch_type, parent_viewport):
        super().__init__(map_id,
                         logger=getLogger(f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.railroad_switch_sprite'),
                         parent_viewport=parent_viewport)
        CONFIG_DB_CURSOR.execute('''SELECT offset_x, offset_y FROM switches_config
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                    AND map_id = ?''',
                                 (track_param_1, track_param_2, switch_type, map_id))
        self.railroad_switch_offset = CONFIG_DB_CURSOR.fetchone()
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['main_map']
        self.on_position_changed()

    def get_position(self):
        return int(self.railroad_switch_offset[0] * self.scale), int(self.railroad_switch_offset[1] * self.scale)
