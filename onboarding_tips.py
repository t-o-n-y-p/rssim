import logging

import pygame

import config as c
from game_object import GameObject


class OnboardingTips(GameObject):
    def __init__(self, image, tip_type):
        super().__init__()
        self.logger = logging.getLogger('game.onboarding_tip_{}'.format(tip_type))
        self.logger.debug('------- START INIT -------')
        self.tip_type = tip_type
        self.image = pygame.image.load(image).convert_alpha()
        self.logger.debug('image loaded: {}'.format(image))
        self.condition_met = False
        self.logger.debug('condition_met: {}'.format(self.condition_met))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('tip init completed')

    def draw(self, surface, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.condition_met:
            self.logger.debug('condition met, we need to show tip')
            surface.blit(self.image, (c.screen_resolution[0] // 2 - self.image.get_width() // 2,
                                      c.screen_resolution[1] // 2 - self.image.get_height() // 2))
        else:
            self.logger.debug('condition not met, no need to show tip')

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('onboarding tip drawing processed')

    def update(self, game_paused):
        self.logger.debug('------- START UPDATING -------')
        if not game_paused:
            self.logger.debug('game was resumed, do not show tip anymore')
            self.condition_met = False
        else:
            self.logger.debug('game is still paused, show tip if game is saved')

        self.logger.debug('------- END UPDATING -------')
        self.logger.info('tip updated')

