import logging

import pygame

import config as c
from game_object import GameObject


class BottomBar(GameObject):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('game.bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        self.bottom_bar_surface = pygame.Surface((c.BOTTOM_BAR_WIDTH, c.BOTTOM_BAR_HEIGHT), pygame.SRCALPHA)
        self.logger.debug('created surface for bottom bar {}x{}'.format(c.BOTTOM_BAR_WIDTH, c.BOTTOM_BAR_HEIGHT))
        self.bottom_bar_surface.fill(c.BOTTOM_BAR_COLOR)
        self.logger.debug('bottom bar color set: {}'.format(c.BOTTOM_BAR_COLOR))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('bottom bar init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        # draw bottom bar for buttons
        surface.blit(self.bottom_bar_surface, (0, c.SCREEN_RESOLUTION[1] - c.BOTTOM_BAR_HEIGHT))
        self.logger.debug('------- END DRAWING -------')
        self.logger.info('bottom bar is in place')
