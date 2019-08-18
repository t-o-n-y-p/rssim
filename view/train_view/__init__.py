from logging import getLogger
from ctypes import windll
from random import seed, choice

from view import *
from database import CONFIG_DB_CURSOR
from ui.sprite.car_sprite import CarSprite
from ui.sprite.boarding_lights_sprite import BoardingLightsSprite


class TrainView(View):
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

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

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

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_update_opacity(self.opacity)
            self.boarding_light_sprites[i].on_update_opacity(self.opacity)

        if self.opacity <= 0:
            for i in range(len(self.car_sprites)):
                self.car_sprites[i] = None
                self.boarding_light_sprites[i] = None

            self.car_sprites = []
            self.boarding_light_sprites = []

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
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

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_change_base_offset(self.base_offset)
            self.boarding_light_sprites[i].on_change_base_offset(self.base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        for i in range(len(self.car_sprites)):
            self.car_sprites[i].on_change_scale(self.zoom_factor)
            self.boarding_light_sprites[i].on_change_scale(self.zoom_factor)

    def on_update_direction(self, new_direction):
        self.direction = new_direction
        for i in range(len(self.car_sprites)):
            if i == 0:
                self.car_sprites[i].on_update_texture(self.car_head_image[self.car_image_collection][self.direction])
            elif i == len(self.car_sprites) - 1:
                self.car_sprites[i].on_update_texture(self.car_tail_image[self.car_image_collection][self.direction])

    def on_update_car_image_collection(self, car_image_collection):
        self.car_image_collection = car_image_collection

    def on_update_state(self, state):
        self.state = state

    def on_update_car_position(self, car_positions):
        self.car_position = car_positions
