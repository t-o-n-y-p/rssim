from logging import getLogger
from typing import final

from ui import GROUPS, BATCHES, CAR_TAIL_IMAGE
from ui.sprite_v2 import MapSpriteV2


@final
class TailCarSpriteV2(MapSpriteV2):
    def __init__(self, map_id, train_id, car_collection_id, current_direction, new_direction, parent_viewport):
        super().__init__(
            map_id=map_id, logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.tail_car_sprite'),
            parent_viewport=parent_viewport
        )
        self.car_collection_id = car_collection_id
        self.new_direction = new_direction
        self.texture = CAR_TAIL_IMAGE[self.map_id][self.car_collection_id][current_direction]
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['train']
        self.usage = 'stream'

    def on_switch_direction(self):
        self.on_update_texture(CAR_TAIL_IMAGE[self.map_id][self.car_collection_id][self.new_direction])
