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
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups):
        super().__init__(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
        self.base_offset = (-3456, -1688)
        self.screen_resolution = (1280, 720)
        self.zoom_out_activated = False
        self.zoom_factor = 1.0
        self.car_position = []
        self.car_head_image = []
        self.car_mid_image = []
        self.car_tail_image = []
        self.boarding_light_image = []
        self.car_sprites = []
        self.boarding_light_sprites = []
        self.direction = None
        self.car_image_collection = None
        self.state = None

    @_view_is_active
    def on_update(self):
        for i in range(len(self.car_position)):
            if self.zoom_out_activated:
                x = self.base_offset[0] + self.car_position[i][0] // 2
                y = self.base_offset[1] + self.car_position[i][1] // 2
            else:
                x = self.base_offset[0] + self.car_position[i][0]
                y = self.base_offset[1] + self.car_position[i][1]

            if x in range(-150, self.screen_resolution[0] + 150) \
                    and y in range(-100, self.screen_resolution[1] + 100):
                if self.car_sprites[i] is None:
                    if i == 0:
                        self.car_sprites[i] = Sprite(self.car_head_image[self.car_image_collection][self.direction],
                                                     x=x, y=y, batch=self.batch, group=self.groups['train'])
                    elif i == len(self.car_position) - 1:
                        self.car_sprites[i] = Sprite(self.car_tail_image[self.car_image_collection][self.direction],
                                                     x=x, y=y, batch=self.batch, group=self.groups['train'])
                    else:
                        self.car_sprites[i] = Sprite(self.car_mid_image[self.car_image_collection][self.direction],
                                                     x=x, y=y, batch=self.batch, group=self.groups['train'])

                    self.car_sprites[i].update(scale=self.zoom_factor, rotation=self.car_position[i][2])
                else:
                    self.car_sprites[i].update(x=x, y=y, rotation=self.car_position[i][2], scale=self.zoom_factor)

                if self.state == 'boarding_in_progress' and i in range(1, len(self.car_position) - 1):
                    if self.boarding_light_sprites[i] is None:
                        self.boarding_light_sprites[i] \
                            = Sprite(self.boarding_light_image[self.car_image_collection], x=x, y=y,
                                     batch=self.batch, group=self.groups['boarding_light'])
                        self.boarding_light_sprites[i].scale = self.zoom_factor
                    else:
                        self.boarding_light_sprites[i].update(x=x, y=y, scale=self.zoom_factor)

                else:
                    if self.boarding_light_sprites[i] is not None:
                        self.boarding_light_sprites[i].delete()
                        self.boarding_light_sprites[i] = None

            else:
                if self.car_sprites[i] is not None:
                    self.car_sprites[i].delete()
                    self.car_sprites[i] = None

                if self.boarding_light_sprites[i] is not None:
                    self.boarding_light_sprites[i].delete()
                    self.boarding_light_sprites[i] = None

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        for i in range(len(self.car_position)):
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

        self.car_sprites.clear()
        self.boarding_light_sprites.clear()

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated

    def on_update_direction(self, new_direction):
        self.direction = new_direction
        if self.is_activated:
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

    def on_update_car_position(self, car_positions):
        self.car_position = car_positions
