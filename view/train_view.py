from pyglet.sprite import Sprite

from .view_base import View


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


class TrainView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.base_offset = (-3440, -1440)
        self.screen_resolution = (1280, 720)
        self.zoom_out_activated = False
        self.zoom_factor = 1.0
        self.car_position = []
        self.car_head_image = []
        self.car_mid_image = []
        self.car_tail_image = []
        self.boarding_light_image = []
        self.car_sprites = None
        self.boarding_light_sprites = None
        self.direction = None
        self.car_image_collection = None
        self.state = None

    def on_update(self):
        pass

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        for i in range(len(self.car_position)):
            if self.zoom_out_activated:
                x = self.base_offset[0] + self.car_position[i][0] // 2
                y = self.base_offset[1] + self.car_position[i][1] // 2
            else:
                x = self.base_offset[0] + self.car_position[i][0]
                y = self.base_offset[1] + self.car_position[i][1]

            if x in range(-150, self.screen_resolution[0] + 150) and y in range(-100, self.screen_resolution[1] + 100):
                if i == 0:
                    sprite = Sprite(self.car_head_image[self.car_image_collection][self.direction], x=x, y=y)
                    self.boarding_light_sprites.append(None)
                elif i == len(self.car_position) - 1:
                    sprite = Sprite(self.car_tail_image[self.car_image_collection][self.direction], x=x, y=y)
                    self.boarding_light_sprites.append(None)
                else:
                    sprite = Sprite(self.car_mid_image[self.car_image_collection][self.direction], x=x, y=y)
                    if self.state == 'boarding_in_progress':
                        self.boarding_light_sprites.append(Sprite(self.boarding_light_image[self.car_image_collection],
                                                                  x=x, y=y))

                sprite.update(scale=self.zoom_factor, rotation=self.car_position[i][2])
                self.car_sprites.append(sprite)
            else:
                self.car_sprites.append(None)
                self.boarding_light_sprites.append(None)

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for i in range(len(self.car_sprites)):
            if self.car_sprites[i] is not None:
                self.car_sprites[i].delete()
                self.car_sprites[i] = None

            if self.boarding_light_sprites[i] is not None:
                self.boarding_light_sprites[i].delete()
                self.boarding_light_sprites[i] = None

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        self.on_update_car_position(self.car_position)

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.on_update_car_position(self.car_position)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        for i in self.car_sprites:
            if i is not None:
                i.scale = self.zoom_factor

        for i in self.boarding_light_sprites:
            if i is not None:
                i.scale = self.zoom_factor

    def on_update_direction(self, new_direction):
        self.direction = new_direction
        if self.car_sprites[0] is not None:
            self.car_sprites[0].image = self.car_head_image[self.car_image_collection][self.direction]

        if self.car_sprites[-1] is not None:
            self.car_sprites[-1].image = self.car_tail_image[self.car_image_collection][self.direction]

        for i in range(1, len(self.car_sprites) - 1):
            if self.car_sprites[i] is not None:
                self.car_sprites[i].image = self.car_mid_image[self.car_image_collection][self.direction]

    def on_update_car_image_collection(self, car_image_collection):
        self.car_image_collection = car_image_collection

    def on_update_state(self, state):
        self.state = state
        if self.state == 'boarding_in_progress':
            for i in range(1, len(self.car_sprites) - 1):
                if self.zoom_out_activated:
                    x = self.base_offset[0] + self.car_position[i][0] // 2
                    y = self.base_offset[1] + self.car_position[i][1] // 2
                else:
                    x = self.base_offset[0] + self.car_position[i][0]
                    y = self.base_offset[1] + self.car_position[i][1]

                if x in range(-150, self.screen_resolution[0] + 150) \
                        and y in range(-100, self.screen_resolution[1] + 100) \
                        and self.boarding_light_sprites[i] is None:
                    self.boarding_light_sprites[i] = Sprite(self.boarding_light_image[self.car_image_collection],
                                                            x=x, y=y)

        else:
            for i in range(1, len(self.car_sprites) - 1):
                if self.boarding_light_sprites[i] is not None:
                    self.boarding_light_sprites[i].delete()
                    self.boarding_light_sprites[i] = None

    def on_update_car_position(self, car_positions):
        self.car_position = car_positions
        for i in range(len(self.car_sprites)):
            if self.zoom_out_activated:
                x = self.base_offset[0] + self.car_position[i][0] // 2
                y = self.base_offset[1] + self.car_position[i][1] // 2
            else:
                x = self.base_offset[0] + self.car_position[i][0]
                y = self.base_offset[1] + self.car_position[i][1]

            if x in range(-150, self.screen_resolution[0] + 150) and y in range(-100, self.screen_resolution[1] + 100):
                if self.car_sprites[i] is None:
                    if i == 0:
                        self.car_sprites[i] = Sprite(self.car_head_image[self.car_image_collection][self.direction],
                                                     x=x, y=y)
                    elif i == len(self.car_position) - 1:
                        self.car_sprites[i] = Sprite(self.car_tail_image[self.car_image_collection][self.direction],
                                                     x=x, y=y)
                    else:
                        self.car_sprites[i] = Sprite(self.car_mid_image[self.car_image_collection][self.direction],
                                                     x=x, y=y)
                        if self.state == 'boarding_in_progress':
                            self.boarding_light_sprites[i] \
                                = Sprite(self.boarding_light_image[self.car_image_collection], x=x, y=y)

                    self.car_sprites[i].update(scale=self.zoom_factor, rotation=self.car_position[i][2])
                else:
                    self.car_sprites[i].update(x=x, y=y, rotation=self.car_position[i][2])
                    if self.state == 'boarding_in_progress' and i in range(1, len(self.car_sprites) - 1):
                        self.boarding_light_sprites[i].position = (x, y)

            else:
                if self.car_sprites[i] is not None:
                    self.car_sprites[i].delete()
                    self.car_sprites[i] = None

                if self.boarding_light_sprites[i] is not None:
                    self.boarding_light_sprites[i].delete()
                    self.boarding_light_sprites[i] = None