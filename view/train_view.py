from logging import getLogger

from pyglet.sprite import Sprite

from view import *


class TrainView(View):
    """
    Implements Train view.
    Train object is responsible for properties, UI and events related to the train.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups, train_id,
                 car_head_image, car_mid_image, car_tail_image, boarding_light_image):
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

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        :param train_id                         train identification number
        :param car_head_image:                  texture for leading carriage
        :param car_mid_image:                   texture for middle carriage
        :param car_tail_image:                  texture for trailing carriage
        :param boarding_light_image:            texture for middle carriage door status lights
        """
        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger(f'root.app.game.map.train.{train_id}.view'))
        self.logger.info('START INIT')
        self.car_position = []
        self.car_head_image = car_head_image
        self.car_mid_image = car_mid_image
        self.car_tail_image = car_tail_image
        self.boarding_light_image = boarding_light_image
        self.logger.debug('textures set successfully')
        self.car_sprites = []
        self.boarding_light_sprites = []
        self.direction = None
        self.car_image_collection = None
        self.state = None
        self.logger.info('END INIT')

    @view_is_active
    def on_update(self):
        """
        Updates fade-in/fade-out animations and creates or deletes car sprites
        depending on car position and train state.
        """
        self.logger.info('START ON_UPDATE')
        self.logger.debug(f'cars: {len(self.car_position)}')
        for i in range(len(self.car_position)):
            self.logger.debug(f'zoom_out_activated: {self.zoom_out_activated}')
            if self.zoom_out_activated:
                x = self.base_offset[0] + self.car_position[i][0] // 2
                y = self.base_offset[1] + self.car_position[i][1] // 2
            else:
                x = self.base_offset[0] + self.car_position[i][0]
                y = self.base_offset[1] + self.car_position[i][1]

            self.logger.debug(f'new car sprite position: {(x, y)}')
            self.logger.debug(f'screen_resolution: {self.screen_resolution}')
            if x in range(-150, self.screen_resolution[0] + 150) \
                    and y in range(-100, self.screen_resolution[1] + 100):
                self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')
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

                    self.logger.debug(f'car {i} sprite position: {self.car_sprites[i].position}')
                    self.car_sprites[i].update(scale=self.zoom_factor, rotation=self.car_position[i][2])
                    self.logger.debug(f'car {i} sprite scale: {self.car_sprites[i].scale}')
                    self.logger.debug(f'car {i} sprite rotation: {self.car_sprites[i].rotation}')
                else:
                    self.car_sprites[i].update(x=x, y=y, rotation=self.car_position[i][2], scale=self.zoom_factor)
                    self.logger.debug(f'car {i} sprite position: {self.car_sprites[i].position}')
                    self.logger.debug(f'car {i} sprite scale: {self.car_sprites[i].scale}')
                    self.logger.debug(f'car {i} sprite rotation: {self.car_sprites[i].rotation}')

                self.logger.debug(f'state: {self.state}')
                if self.state == 'boarding_in_progress' and i in range(1, len(self.car_position) - 1):
                    self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')
                    if self.boarding_light_sprites[i] is None:
                        self.boarding_light_sprites[i] \
                            = Sprite(self.boarding_light_image[self.car_image_collection], x=x, y=y,
                                     batch=self.batches['main_batch'], group=self.groups['boarding_light'])
                        self.logger.debug('car {} boarding light sprite position: {}'
                                          .format(i, self.boarding_light_sprites[i].position))
                        self.boarding_light_sprites[i].scale = self.zoom_factor
                        self.logger.debug('car {} boarding light sprite scale: {}'
                                          .format(i, self.boarding_light_sprites[i].scale))
                    else:
                        self.boarding_light_sprites[i].update(x=x, y=y, scale=self.zoom_factor)
                        self.logger.debug('car {} boarding light sprite position: {}'
                                          .format(i, self.boarding_light_sprites[i].position))
                        self.logger.debug('car {} boarding light sprite scale: {}'
                                          .format(i, self.boarding_light_sprites[i].scale))

                else:
                    self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')
                    if self.boarding_light_sprites[i] is not None:
                        self.boarding_light_sprites[i].delete()
                        self.boarding_light_sprites[i] = None
                        self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')

            else:
                self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')
                if self.car_sprites[i] is not None:
                    self.car_sprites[i].delete()
                    self.car_sprites[i] = None
                    self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')

                self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')
                if self.boarding_light_sprites[i] is not None:
                    self.boarding_light_sprites[i].delete()
                    self.boarding_light_sprites[i] = None
                    self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')

        self.logger.info('END ON_UPDATE')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates lists for car sprites.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        for i in range(len(self.car_position)):
            self.car_sprites.append(None)
            self.boarding_light_sprites.append(None)

        self.logger.debug(f'car_sprites: {self.car_sprites}')
        self.logger.debug(f'boarding_light_sprites: {self.boarding_light_sprites}')
        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        for i in range(len(self.car_sprites)):
            self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')
            if self.car_sprites[i] is not None:
                self.car_sprites[i].delete()
                self.car_sprites[i] = None
                self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')

            self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')
            if self.boarding_light_sprites[i] is not None:
                self.boarding_light_sprites[i].delete()
                self.boarding_light_sprites[i] = None
                self.logger.debug(f'car {i} boarding light sprite: {self.boarding_light_sprites[i]}')

        self.car_sprites.clear()
        self.boarding_light_sprites.clear()
        self.logger.debug(f'car_sprites: {self.car_sprites}')
        self.logger.debug(f'boarding_light_sprites: {self.boarding_light_sprites}')
        self.logger.info('END ON_DEACTIVATE')

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset.

        :param new_base_offset:         new base offset
        """
        self.logger.info('START ON_CHANGE_BASE_OFFSET')
        self.base_offset = new_base_offset
        self.logger.info('END ON_CHANGE_BASE_OFFSET')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.on_recalculate_ui_properties(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites (nothing at the moment).
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.logger.info('START ON_CHANGE_ZOOM_FACTOR')
        self.zoom_factor = zoom_factor
        self.logger.debug(f'zoom_factor: {self.zoom_factor}')
        self.zoom_out_activated = zoom_out_activated
        self.logger.debug(f'zoom_out_activated: {self.zoom_out_activated}')
        self.logger.info('END ON_CHANGE_ZOOM_FACTOR')

    def on_update_direction(self, new_direction):
        """
        Updates current train direction value and car sprites.

        :param new_direction:                   new direction
        """
        self.logger.info('START ON_UPDATE_DIRECTION')
        self.direction = new_direction
        self.logger.debug(f'direction: {self.direction}')
        self.logger.debug(f'is_activated: {self.is_activated}')
        if self.is_activated:
            self.logger.debug(f'car 0 sprite: {self.car_sprites[0]}')
            if self.car_sprites[0] is not None:
                self.car_sprites[0].image = self.car_head_image[self.car_image_collection][self.direction]
                self.logger.debug(f'car 0 sprite: {self.car_sprites[0]}')

            self.logger.debug(f'last car sprite: {self.car_sprites[-1]}')
            if self.car_sprites[-1] is not None:
                self.car_sprites[-1].image = self.car_tail_image[self.car_image_collection][self.direction]
                self.logger.debug(f'last car sprite: {self.car_sprites[-1]}')

            for i in range(1, len(self.car_sprites) - 1):
                self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')
                if self.car_sprites[i] is not None:
                    self.car_sprites[i].image = self.car_mid_image[self.car_image_collection][self.direction]
                    self.logger.debug(f'car {i} sprite: {self.car_sprites[i]}')

        self.logger.info('END ON_UPDATE_DIRECTION')

    def on_update_car_image_collection(self, car_image_collection):
        """
        Updates car image collection value to assign car images correctly when direction is updated.

        :param car_image_collection:            image collection ID
        """
        self.logger.info('START ON_UPDATE_CAR_IMAGE_COLLECTION')
        self.car_image_collection = car_image_collection
        self.logger.debug(f'car_image_collection: {self.car_image_collection}')
        self.logger.info('END ON_UPDATE_CAR_IMAGE_COLLECTION')

    def on_update_state(self, state):
        """
        Updates train state.

        :param state:                           new train state
        """
        self.logger.info('START ON_UPDATE_STATE')
        self.state = state
        self.logger.debug(f'state: {self.state}')
        self.logger.info('END ON_UPDATE_STATE')

    def on_update_car_position(self, car_positions):
        """
        Updates car positions.

        :param car_positions:                   new car positions
        """
        self.logger.info('START ON_UPDATE_CAR_POSITION')
        self.car_position = car_positions
        self.logger.debug(f'car_position: {self.car_position}')
        self.logger.info('END ON_UPDATE_CAR_POSITION')
