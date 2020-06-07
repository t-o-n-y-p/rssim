from typing import final

from ui import GROUPS, BATCHES, CAR_MID_IMAGE
from ui.sprite_v2 import MapSpriteV2


@final
class MidCarSpriteV2(MapSpriteV2):
    def __init__(self, logger, parent_viewport, map_id, car_collection_id):
        super().__init__(logger, parent_viewport, map_id)
        self.texture = CAR_MID_IMAGE[self.map_id][car_collection_id]
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['train']
        self.usage = 'stream'
