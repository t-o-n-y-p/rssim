import logging

import pygame

from game_object import GameObject
from text_object import TextObject


class TopAndBottomBar(GameObject):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('game.top_and_bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        self.top_bar_surface = pygame.Surface((self.c['graphics']['screen_resolution'][0],
                                               self.c['graphics']['top_bar_height']), pygame.SRCALPHA)
        self.bottom_bar_surface = pygame.Surface((self.c['graphics']['bottom_bar_width'],
                                                  self.c['graphics']['bottom_bar_height']), pygame.SRCALPHA)
        self.app_title_surface \
            = TextObject((100, self.c['graphics']['top_bar_height'] // 2),
                         'Railway Station Simulator', self.c['graphics']['button_text_color'],
                         self.c['graphics']['font_name'], self.c['graphics']['button_font_size'])
        self.logger.debug('created surface for bottom bar {}x{}'.format(self.c['graphics']['bottom_bar_width'],
                                                                        self.c['graphics']['bottom_bar_height']))
        self.top_bar_surface.fill(self.c['graphics']['bottom_bar_color'])
        pygame.draw.line(self.top_bar_surface, (255, 255, 255),
                         (0, 0), (self.c['graphics']['screen_resolution'][0] - 1, 0), 2)
        pygame.draw.line(self.top_bar_surface, (255, 255, 255),
                         (0, self.c['graphics']['top_bar_height'] - 2),
                         (self.c['graphics']['screen_resolution'][0] - 1, self.c['graphics']['top_bar_height'] - 2), 2)
        self.bottom_bar_surface.fill(self.c['graphics']['bottom_bar_color'])
        pygame.draw.line(self.bottom_bar_surface, (255, 255, 255),
                         (0, 0), (self.c['graphics']['bottom_bar_width'] - 1, 0), 2)
        pygame.draw.line(self.bottom_bar_surface, (255, 255, 255),
                         (0, self.c['graphics']['bottom_bar_height'] - 2),
                         (self.c['graphics']['bottom_bar_width'] - 1, self.c['graphics']['bottom_bar_height'] - 2), 2)
        pygame.draw.line(self.bottom_bar_surface, (255, 255, 255),
                         (self.c['graphics']['bottom_bar_width'] - 2, 0),
                         (self.c['graphics']['bottom_bar_width'] - 2, self.c['graphics']['bottom_bar_height'] - 2), 2)
        self.logger.debug('bottom bar color set: {}'.format(self.c['graphics']['bottom_bar_color']))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('top and bottom bar init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        # draw bottom bar for buttons
        surface.blit(self.top_bar_surface, (0, 0))
        self.app_title_surface.draw(surface)
        surface.blit(self.bottom_bar_surface,
                     (0, self.c['graphics']['screen_resolution'][1] - self.c['graphics']['bottom_bar_height']))
        pygame.draw.line(surface, (255, 255, 255), (0, 0), (self.c['graphics']['screen_resolution'][0] - 2, 0), 2)
        pygame.draw.line(surface, (255, 255, 255), (0, 0), (0, self.c['graphics']['screen_resolution'][1] - 2), 2)
        pygame.draw.line(surface, (255, 255, 255), (self.c['graphics']['screen_resolution'][0] - 2, 0),
                         (self.c['graphics']['screen_resolution'][0] - 2,
                          self.c['graphics']['screen_resolution'][1] - 2), 2)
        pygame.draw.line(surface, (255, 255, 255), (0, self.c['graphics']['screen_resolution'][1] - 2),
                         (self.c['graphics']['screen_resolution'][0] - 2,
                          self.c['graphics']['screen_resolution'][1] - 2), 2)
        self.logger.debug('------- END DRAWING -------')
        self.logger.info('bottom bar is in place')
