from logging import getLogger

from ui import *
from ui.sprite import MapSprite


@final
class CarSprite(MapSprite):
    def __init__(self, map_id, train_id, parent_viewport):
        super().__init__(map_id, logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.car_sprite'),
                         parent_viewport=parent_viewport)
        self.car_offset = (0, 0)
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['train']
        self.usage = 'stream'
        self.subpixel = True
        self.on_position_changed()

    def get_position(self):
        return self.car_offset

    def on_update_car_position(self, car_position):
        self.car_offset = car_position[0:2]
        self.on_position_changed()
        self.on_rotate(car_position[2])
