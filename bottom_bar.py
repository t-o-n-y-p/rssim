import logging

import pygame

from game_object import GameObject


class BottomBar(GameObject):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('game.bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        self.bottom_bar_surface = pygame.Surface((self.c['graphics']['bottom_bar_width'],
                                                  self.c['graphics']['bottom_bar_height']), pygame.SRCALPHA)
        self.logger.debug('created surface for bottom bar {}x{}'.format(self.c['graphics']['bottom_bar_width'],
                                                                        self.c['graphics']['bottom_bar_height']))
        self.bottom_bar_surface.fill(self.c['graphics']['bottom_bar_color'])
        self.logger.debug('bottom bar color set: {}'.format(self.c['graphics']['bottom_bar_color']))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('bottom bar init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        # draw bottom bar for buttons
        surface.blit(self.bottom_bar_surface,
                     (0, self.c['graphics']['screen_resolution'][1] - self.c['graphics']['bottom_bar_height']))
        self.logger.debug('------- END DRAWING -------')
        self.logger.info('bottom bar is in place')
