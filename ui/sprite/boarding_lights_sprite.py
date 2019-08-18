from logging import getLogger

from ui import *
from ui.sprite import MapSprite


class BoardingLightsSprite(MapSprite):
    def __init__(self, map_id, train_id, parent_viewport):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.boarding_lights_sprite'),
                         parent_viewport=parent_viewport)
        self.car_offset = (0, 0)
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['train']
        self.usage = 'stream'
        self.on_position_changed()

    def get_position(self):
        return (self.base_offset[0] + int(self.car_offset[0] * self.scale),
                self.base_offset[1] + int(self.car_offset[1] * self.scale))

    def on_update_car_position(self, car_position):
        self.car_offset = car_position[0:2]
        self.on_position_changed()
        self.on_rotate(car_position[2])
