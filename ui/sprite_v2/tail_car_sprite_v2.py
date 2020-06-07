from typing import final

from ui import GROUPS, BATCHES, CAR_TAIL_IMAGE
from ui.sprite_v2 import MapSpriteV2


@final
class TailCarSpriteV2(MapSpriteV2):
    def __init__(self, logger, parent_viewport, map_id, car_collection_id, current_direction, new_direction):
        super().__init__(logger, parent_viewport, map_id)
        self.car_collection_id = car_collection_id
        self.new_direction = new_direction
        self.texture = CAR_TAIL_IMAGE[self.map_id][self.car_collection_id][current_direction]
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['train']
        self.usage = 'stream'

    def on_switch_direction(self):
        self.on_update_texture(CAR_TAIL_IMAGE[self.map_id][self.car_collection_id][self.new_direction])
