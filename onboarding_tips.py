import logging

import pygame

from game_object import GameObject


class OnboardingTips(GameObject):
    def __init__(self, image, x, y, tip_type):
        super().__init__()
        self.logger = logging.getLogger('game.onboarding_tip_{}'.format(tip_type))
        self.logger.debug('------- START INIT -------')
        self.tip_type = tip_type
        self.image = image
        self.logger.debug('image loaded: {}'.format(image))
        self.condition_met = False
        self.logger.debug('condition_met: {}'.format(self.condition_met))
        self.rect_area = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.return_rect_area = False
        self.logger.debug('------- END INIT -------')
        self.logger.warning('tip init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.condition_met:
            self.logger.debug('condition met, we need to show tip')
            if self.tip_type == 'mini_map':
                new_image = self.image.copy()
                position_rect = new_image.get_rect()
                position_rect.x = (-1) * base_offset[0] * new_image.get_width() \
                    // self.c['graphics']['map_resolution'][0]
                position_rect.y = (-1) * base_offset[1] * new_image.get_height() \
                    // self.c['graphics']['map_resolution'][1]
                position_rect.w = self.c['graphics']['screen_resolution'][0] * new_image.get_width() \
                    // self.c['graphics']['map_resolution'][0]
                position_rect.h = self.c['graphics']['screen_resolution'][1] * new_image.get_height() \
                    // self.c['graphics']['map_resolution'][1]
                pygame.draw.rect(new_image, (255, 127, 0), position_rect, 1)
                surface.blit(new_image, (self.rect_area.x, self.rect_area.y))
            else:
                surface.blit(self.image, (self.rect_area.x, self.rect_area.y))
        else:
            self.logger.debug('condition not met, no need to show tip')

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('onboarding tip drawing processed')
        if self.return_rect_area:
            self.return_rect_area = False
            return [self.rect_area, ]
        else:
            return []

    def update_image(self, new_base_image):
        self.image = new_base_image


