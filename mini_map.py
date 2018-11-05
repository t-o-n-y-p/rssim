from logging import getLogger

from pyglet.image import load
from pyglet.sprite import Sprite

from game_object import GameObject


class MiniMap(GameObject):
    def __init__(self, image, x, y, batch, group, viewport_border_group, game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.mini_map')
        self.logger.debug('------- START INIT -------')
        self.image = image
        self.batch = batch
        self.group = group
        self.viewport_border_group = viewport_border_group
        self.x = x
        self.y = y
        self.sprite = None
        self.viewport_border = None
        self.viewport_border_image = load('img/viewport_border.png')
        self.logger.debug('image loaded: {}'.format(image))
        self.condition_met = False
        self.logger.debug('condition_met: {}'.format(self.condition_met))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('tip init completed')

    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.condition_met:
            if self.sprite is None:
                self.sprite = Sprite(self.image, x=self.x, y=self.y, batch=self.batch, group=self.group)
                self.sprite.opacity = 0
                self.logger.debug('condition met, we need to show tip')
            else:
                if self.sprite.opacity < 255:
                    self.sprite.opacity += 15

            if self.viewport_border is None:
                self.viewport_border = Sprite(self.viewport_border_image, batch=self.batch,
                                              group=self.viewport_border_group)
                self.viewport_border.opacity = 0
            else:
                self.viewport_border.position = (self.x + round((-1) * base_offset[0]
                                                                / self.c.map_resolution[0]
                                                                * self.sprite.width),
                                                 self.y + round((-1) * base_offset[1]
                                                                / self.c.map_resolution[1]
                                                                * self.sprite.height))
                if self.viewport_border.opacity < 255:
                    self.viewport_border.opacity += 15

        if not self.condition_met:
            if self.sprite is not None:
                self.sprite.opacity -= 15
                if self.sprite.opacity <= 0:
                    self.sprite.delete()
                    self.sprite = None

            if self.viewport_border is not None:
                self.viewport_border.opacity -= 15
                if self.viewport_border.opacity <= 0:
                    self.viewport_border.delete()
                    self.viewport_border = None

            self.logger.debug('condition not met, no need to show tip')

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('onboarding tip drawing processed')

    def on_track_unlock(self, track):
        self.image = load('img/mini_map/{}/mini_map.png'.format(track))
