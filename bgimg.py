import logging

import pygame

from game_object import GameObject


class BgImg(GameObject):
    def __init__(self, image):
        super().__init__()
        self.logger = logging.getLogger('game.background_image')
        self.logger.debug('------- START INIT -------')
        # load background texture tile
        self.image = pygame.image.load(image).convert_alpha()
        self.logger.debug('background image loaded: {}'.format(image))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('background image init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        # fill map with background texture tile
        for i in range(self.c['graphics']['number_of_background_tiles'][0]):
            for j in range(self.c['graphics']['number_of_background_tiles'][1]):
                if (base_offset[0] + i*self.c['graphics']['background_tile_resolution'][0]) \
                        in range((-1)*self.c['graphics']['background_tile_resolution'][0],
                                 self.c['graphics']['screen_resolution'][0]) \
                        and (base_offset[1] + j*self.c['graphics']['background_tile_resolution'][1]) \
                        in range((-1)*self.c['graphics']['background_tile_resolution'][1],
                                 self.c['graphics']['screen_resolution'][1]):
                    surface.blit(self.image, (base_offset[0] + i*self.c['graphics']['background_tile_resolution'][0],
                                              base_offset[1] + j*self.c['graphics']['background_tile_resolution'][1]))
                    self.logger.debug('tile {} {} drawing completed'.format(i, j))

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('background image is in place')
