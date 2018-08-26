import logging

import pyglet

from game_object import GameObject


class BgImg(GameObject):
    def __init__(self, image, batch, group):
        super().__init__()
        self.logger = logging.getLogger('game.background_image')
        self.logger.debug('------- START INIT -------')
        # load background texture tile
        self.image = pyglet.image.load(image)
        self.sprite = {}
        for i in range(self.c['graphics']['number_of_background_tiles'][0]):
            self.sprite[i] = {}
            for j in range(self.c['graphics']['number_of_background_tiles'][1]):
                self.sprite[i][j] = pyglet.sprite.Sprite(self.image,
                                                         x=i*self.c['graphics']['background_tile_resolution'][0],
                                                         y=j*self.c['graphics']['background_tile_resolution'][1],
                                                         batch=batch, group=group)
        self.logger.debug('background image loaded')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('background image init completed')

    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        # fill map with background texture tile
        for i in range(self.c['graphics']['number_of_background_tiles'][0]):
            for j in range(self.c['graphics']['number_of_background_tiles'][1]):
                x = base_offset[0] + i*self.c['graphics']['background_tile_resolution'][0]
                y = self.c['graphics']['screen_resolution'][1] \
                    - (base_offset[1] + j*self.c['graphics']['background_tile_resolution'][1])
                self.sprite[i][j].position = (x, y)
                self.logger.debug('tile {} {} drawing completed'.format(i, j))

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('background image is in place')
