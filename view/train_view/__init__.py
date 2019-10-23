from logging import getLogger
from random import seed, choice

from view import *
from ui.sprite.car_sprite import CarSprite
from ui.sprite.boarding_lights_sprite import BoardingLightsSprite


class TrainView(MapBaseView):
    def __init__(self, map_id, train_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.view'))
        self.map_id = map_id
        self.train_id = train_id
        self.car_position = []
        self.car_head_image = None
        self.car_mid_image = None
        self.car_tail_image = None
        self.boarding_light_image = None
        self.car_sprites = []
        self.boarding_light_sprites = []
        self.direction = None
        self.car_image_collection = None
        self.state = None

    @final
    def on_update(self):
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_update_car_position(self.car_position[i])
            self.boarding_light_sprites[i].on_update_car_position(self.car_position[i])
            if self.car_sprites[i].is_located_outside_viewport():
                self.car_sprites[i].delete()
                self.boarding_light_sprites[i].delete()
            else:
                if i not in (0, len(self.car_position) - 1) and self.state == 'boarding_in_progress':
                    self.car_sprites[i].delete()
                    self.boarding_light_sprites[i].create()
                else:
                    self.boarding_light_sprites[i].delete()
                    self.car_sprites[i].create()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_update_opacity(self.opacity)
            self.boarding_light_sprites[i].on_update_opacity(self.opacity)

        if self.opacity <= 0:
            self.car_sprites = []
            self.boarding_light_sprites = []

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        seed()
        for i in range(len(self.car_position)):
            self.car_sprites.append(CarSprite(self.map_id, self.train_id, parent_viewport=self.viewport))
            if i == 0:
                self.car_sprites[i].on_update_texture(self.car_head_image[self.car_image_collection][self.direction])
            elif i == len(self.car_position) - 1:
                self.car_sprites[i].on_update_texture(self.car_tail_image[self.car_image_collection][self.direction])
            else:
                self.car_sprites[i].on_update_texture(choice(self.car_mid_image[self.car_image_collection]))

            self.boarding_light_sprites.append(BoardingLightsSprite(self.map_id, self.train_id,
                                                                    parent_viewport=self.viewport))
            self.boarding_light_sprites[i].on_update_texture(self.boarding_light_image[self.car_image_collection])

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_change_base_offset(self, new_base_offset):
        super().on_change_base_offset(new_base_offset)
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_change_base_offset(self.base_offset)
            self.boarding_light_sprites[i].on_change_base_offset(self.base_offset)

    @final
    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        super().on_change_zoom_factor(zoom_factor, zoom_out_activated)
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_change_scale(self.zoom_factor)
            self.boarding_light_sprites[i].on_change_scale(self.zoom_factor)

    @final
    def on_update_direction(self, new_direction):
        self.direction = new_direction
        for i in range(len(self.car_sprites)):
            if i == 0:
                self.car_sprites[i].on_update_texture(self.car_head_image[self.car_image_collection][self.direction])
            elif i == len(self.car_sprites) - 1:
                self.car_sprites[i].on_update_texture(self.car_tail_image[self.car_image_collection][self.direction])
