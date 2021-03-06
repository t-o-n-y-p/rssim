from abc import ABC
from logging import getLogger
from typing import final

from database import USER_DB_CURSOR
from ui.sprite.car_sprite import CarSprite
from ui.sprite.boarding_lights_sprite import BoardingLightsSprite
from view import MapBaseView, view_is_not_active


class TrainView(MapBaseView, ABC):
    def __init__(self, controller, map_id, train_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.view'))
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
        self.cars = None
        self.on_append_window_handlers()

    def on_train_setup(self):
        USER_DB_CURSOR.execute(
            '''SELECT cars, state, direction, car_image_collection FROM trains WHERE train_id = ? AND map_id = ?''',
            (self.train_id, self.map_id)
        )
        self.cars, self.state, self.direction, self.car_image_collection = USER_DB_CURSOR.fetchone()

    def on_train_init(self, cars, state, direction, car_image_collection, game_time, game_time_fraction, dt_multiplier):
        self.cars, self.state, self.direction, self.car_image_collection, \
            self.game_time, self.game_time_fraction, self.dt_multiplier \
            = cars, state, direction, car_image_collection, game_time, game_time_fraction, dt_multiplier

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        for i in range(self.cars):
            self.car_sprites.append(CarSprite(self.map_id, self.train_id, parent_viewport=self.viewport))
            if i == 0:
                self.car_sprites[i].on_update_texture(self.car_head_image[self.car_image_collection][self.direction])
            elif i == self.cars - 1:
                self.car_sprites[i].on_update_texture(self.car_tail_image[self.car_image_collection][self.direction])
            else:
                self.car_sprites[i].on_update_texture(self.car_mid_image[self.car_image_collection])

            self.boarding_light_sprites.append(
                BoardingLightsSprite(self.map_id, self.train_id, parent_viewport=self.viewport)
            )
            self.boarding_light_sprites[i].on_update_texture(self.boarding_light_image[self.car_image_collection])

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
    def on_update_direction(self, new_direction):
        self.direction = new_direction
        for i in range(len(self.car_sprites)):
            if i == 0:
                self.car_sprites[i].on_update_texture(self.car_head_image[self.car_image_collection][self.direction])
            elif i == len(self.car_sprites) - 1:
                self.car_sprites[i].on_update_texture(self.car_tail_image[self.car_image_collection][self.direction])
