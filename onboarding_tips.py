import logging

import pyglet

from game_object import GameObject


class OnboardingTips(GameObject):
    def __init__(self, image, x, y, tip_type, batch, group):
        super().__init__()
        self.logger = logging.getLogger('game.onboarding_tip_{}'.format(tip_type))
        self.logger.debug('------- START INIT -------')
        self.tip_type = tip_type
        self.image = image
        self.batch = batch
        self.group = group
        self.x = x
        self.y = y
        self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                           y=self.c['graphics']['screen_resolution'][1] - self.y,
                                           batch=self.batch, group=self.group)
        self.logger.debug('image loaded: {}'.format(image))
        self.condition_met = False
        self.logger.debug('condition_met: {}'.format(self.condition_met))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('tip init completed')

    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.condition_met:
            if self.sprite is not None:
                self.sprite.delete()
                self.sprite = None

            self.sprite = pyglet.sprite.Sprite(self.image, x=self.x,
                                               y=self.c['graphics']['screen_resolution'][1]
                                               - self.y - self.image.height,
                                               batch=self.batch, group=self.group)
            self.logger.debug('condition met, we need to show tip')
        else:
            if self.sprite is not None:
                self.sprite.delete()
                self.sprite = None

            self.logger.debug('condition not met, no need to show tip')

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('onboarding tip drawing processed')

    def update_image(self, new_base_image):
        self.image = new_base_image


