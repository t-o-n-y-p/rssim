import logging

import pygame

import config as c
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
        for i in range(c.NUMBER_OF_BACKGROUND_TILES[0]):
            for j in range(c.NUMBER_OF_BACKGROUND_TILES[1]):
                surface.blit(self.image, (base_offset[0] + i*c.BACKGROUND_TILE_RESOLUTION[0],
                                          base_offset[1] + j*c.BACKGROUND_TILE_RESOLUTION[1]))
                self.logger.debug('tile {} {} drawing completed'.format(i, j))

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('background image is in place')
