from logging import getLogger
from typing import final

from ui import GROUPS, BATCHES, CAR_MID_IMAGE
from ui.sprite_v2 import MapSpriteV2


@final
class MidCarSpriteV2(MapSpriteV2):
    def __init__(self, map_id, train_id, car_collection_id, parent_viewport):
        super().__init__(
            map_id=map_id, logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.mid_car_sprite'),
            parent_viewport=parent_viewport
        )
        self.texture = CAR_MID_IMAGE[self.map_id][car_collection_id]
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['train']
        self.usage = 'stream'
