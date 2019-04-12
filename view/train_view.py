from logging import getLogger

from pyglet.sprite import Sprite

from view import *
from textures import CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE


class TrainView(View):
    """
    Implements Train view.
    Train object is responsible for properties, UI and events related to the train.
    """
    def __init__(self, train_id):
        """
        Properties:
            car_position                        2D Cartesian positions for all cars plus rotation angle
            car_head_image                      texture for leading carriage
            car_mid_image                       texture for middle carriage
            car_tail_image                      texture for trailing carriage
            boarding_light_image                texture for middle carriage door status lights
            car_sprites                         list of sprites from car textures
            boarding_light_sprites              list of sprites from boarding lights textures
            direction                           current train direction
            car_image_collection                car image collection ID for this train
            state                               current train state

        :param train_id                         train identification number
        """
        self.map_id = None
        self.on_update_map_id()
        super().__init__(logger=getLogger(f'root.app.game.map.{self.map_id}.train.{train_id}.view'))
        self.car_position = []
        self.car_head_image = CAR_HEAD_IMAGE
        self.car_mid_image = CAR_MID_IMAGE
        self.car_tail_image = CAR_TAIL_IMAGE
        self.boarding_light_image = BOARDING_LIGHT_IMAGE
        self.car_sprites = []
        self.boarding_light_sprites = []
        self.direction = None
        self.car_image_collection = None
        self.state = None
        self.on_init_graphics()

    @view_is_active
    def on_update(self):
        """
        Updates fade-in/fade-out animations and creates or deletes car sprites
        depending on car position and train state.
        """
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
                                                     x=x, y=y, batch=self.batches['main_batch'],
                                                     group=self.groups['train'])
                    elif i == len(self.car_position) - 1:
                        self.car_sprites[i] = Sprite(self.car_tail_image[self.car_image_collection][self.direction],
                                                     x=x, y=y, batch=self.batches['main_batch'],
                                                     group=self.groups['train'])
                    else:
                        self.car_sprites[i] = Sprite(self.car_mid_image[self.car_image_collection][self.direction],
                                                     x=x, y=y, batch=self.batches['main_batch'],
                                                     group=self.groups['train'])

                    self.car_sprites[i].update(scale=self.zoom_factor, rotation=self.car_position[i][2])
                else:
                    self.car_sprites[i].update(x=x, y=y, rotation=self.car_position[i][2], scale=self.zoom_factor)

                if self.state == 'boarding_in_progress' and i in range(1, len(self.car_position) - 1):
                    if self.boarding_light_sprites[i] is None:
                        self.boarding_light_sprites[i] \
                            = Sprite(self.boarding_light_image[self.car_image_collection], x=x, y=y,
                                     batch=self.batches['main_batch'], group=self.groups['boarding_light'])
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

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates lists for car sprites.
        """
        self.on_init_graphics()
        self.is_activated = True
        for i in range(len(self.car_position)):
            self.car_sprites.append(None)
            self.boarding_light_sprites.append(None)

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
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
        """
        Updates base offset.

        :param new_base_offset:         new base offset
        """
        self.base_offset = new_base_offset

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites (nothing at the moment).
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated

    def on_update_direction(self, new_direction):
        """
        Updates current train direction value and car sprites.

        :param new_direction:                   new direction
        """
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
        """
        Updates car image collection value to assign car images correctly when direction is updated.

        :param car_image_collection:            image collection ID
        """
        self.car_image_collection = car_image_collection

    def on_update_state(self, state):
        """
        Updates train state.

        :param state:                           new train state
        """
        self.state = state

    def on_update_car_position(self, car_positions):
        """
        Updates car positions.

        :param car_positions:                   new car positions
        """
        self.car_position = car_positions

    def on_update_map_id(self):
        self.map_id = 0

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)