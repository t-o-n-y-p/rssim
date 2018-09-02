import logging

import pyglet

from game_object import GameObject


class OnboardingTips(GameObject):
    def __init__(self, image, x, y, tip_type, batch, group, viewport_border_group):
        super().__init__()
        self.logger = logging.getLogger('game.onboarding_tip_{}'.format(tip_type))
        self.logger.debug('------- START INIT -------')
        self.tip_type = tip_type
        self.image = image
        self.batch = batch
        self.group = group
        self.viewport_border_group = viewport_border_group
        self.x = x
        self.y = self.c['graphics']['screen_resolution'][1] - y - self.image.height
        self.sprite = None
        self.viewport_border = None
        self.viewport_border_opacity = 0
        self.logger.debug('image loaded: {}'.format(image))
        self.condition_met = False
        self.logger.debug('condition_met: {}'.format(self.condition_met))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('tip init completed')

    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.condition_met:
            if self.sprite is None:
                self.sprite = pyglet.sprite.Sprite(self.image, x=self.x, y=self.y,
                                                   batch=self.batch, group=self.group)
                self.sprite.opacity = 0
                self.logger.debug('condition met, we need to show tip')
            else:
                if self.sprite.opacity < 255:
                    self.sprite.opacity += 15

            if self.tip_type == 'mini_map':
                if self.viewport_border is None:
                    self.viewport_border \
                        = self.batch.add(8, pyglet.gl.GL_LINES, self.viewport_border_group,
                                         ('v2i',
                                          (self.x + round((-1) * base_offset[0]
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width) + 1,
                                           self.y + round((-1) * base_offset[1]
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height) + 1,
                                           self.x + round(((-1) * base_offset[0]
                                                           + self.c['graphics']['screen_resolution'][0])
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width),
                                           self.y + round((-1) * base_offset[1]
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height) + 1,
                                           self.x + round(((-1) * base_offset[0]
                                                           + self.c['graphics']['screen_resolution'][0])
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width),
                                           self.y + round((-1) * base_offset[1]
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height) + 1,
                                           self.x + round(((-1) * base_offset[0]
                                                           + self.c['graphics']['screen_resolution'][0])
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width),
                                           self.y + round(((-1) * base_offset[1]
                                                           + self.c['graphics']['screen_resolution'][1])
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height),
                                           self.x + round(((-1) * base_offset[0]
                                                           + self.c['graphics']['screen_resolution'][0])
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width),
                                           self.y + round(((-1) * base_offset[1]
                                                           + self.c['graphics']['screen_resolution'][1])
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height),
                                           self.x + round((-1) * base_offset[0]
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width) + 1,
                                           self.y + round(((-1) * base_offset[1]
                                                           + self.c['graphics']['screen_resolution'][1])
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height),
                                           self.x + round((-1) * base_offset[0]
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width) + 1,
                                           self.y + round(((-1) * base_offset[1]
                                                           + self.c['graphics']['screen_resolution'][1])
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height),
                                           self.x + round((-1) * base_offset[0]
                                                          / self.c['graphics']['map_resolution'][0]
                                                          * self.sprite.width) + 1,
                                           self.y + round((-1) * base_offset[1]
                                                          / self.c['graphics']['map_resolution'][1]
                                                          * self.sprite.height)
                                           )),
                                         ('c4B/static', (255, 127, 0, 0, 255, 127, 0, 0, 255, 127, 0, 0, 255, 127, 0, 0,
                                                         255, 127, 0, 0, 255, 127, 0, 0, 255, 127, 0, 0, 255, 127, 0, 0
                                                         ))
                                         )
                else:
                    self.viewport_border.vertices \
                        = (self.x + round((-1) * base_offset[0]
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width) + 1,
                           self.y + round((-1) * base_offset[1]
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height) + 1,
                           self.x + round(((-1) * base_offset[0]
                                           + self.c['graphics']['screen_resolution'][0])
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width),
                           self.y + round((-1) * base_offset[1]
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height) + 1,
                           self.x + round(((-1) * base_offset[0]
                                           + self.c['graphics']['screen_resolution'][0])
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width),
                           self.y + round((-1) * base_offset[1]
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height) + 1,
                           self.x + round(((-1) * base_offset[0]
                                           + self.c['graphics']['screen_resolution'][0])
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width),
                           self.y + round(((-1) * base_offset[1]
                                           + self.c['graphics']['screen_resolution'][1])
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height),
                           self.x + round(((-1) * base_offset[0]
                                           + self.c['graphics']['screen_resolution'][0])
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width),
                           self.y + round(((-1) * base_offset[1]
                                           + self.c['graphics']['screen_resolution'][1])
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height),
                           self.x + round((-1) * base_offset[0]
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width) + 1,
                           self.y + round(((-1) * base_offset[1]
                                           + self.c['graphics']['screen_resolution'][1])
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height),
                           self.x + round((-1) * base_offset[0]
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width) + 1,
                           self.y + round(((-1) * base_offset[1]
                                           + self.c['graphics']['screen_resolution'][1])
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height),
                           self.x + round((-1) * base_offset[0]
                                          / self.c['graphics']['map_resolution'][0]
                                          * self.sprite.width) + 1,
                           self.y + round((-1) * base_offset[1]
                                          / self.c['graphics']['map_resolution'][1]
                                          * self.sprite.height)
                           )
                    if self.viewport_border_opacity < 255:
                        self.viewport_border_opacity += 15
                        self.viewport_border.colors = (255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity,
                                                       255, 127, 0, self.viewport_border_opacity)
        else:
            if self.sprite is not None:
                self.sprite.opacity -= 15
                if self.sprite.opacity <= 0:
                    self.sprite.delete()
                    self.sprite = None

            if self.viewport_border is not None:
                self.viewport_border_opacity -= 15
                self.viewport_border.colors = (255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity,
                                               255, 127, 0, self.viewport_border_opacity)
                if self.viewport_border_opacity <= 0:
                    self.viewport_border.delete()
                    self.viewport_border = None

            self.logger.debug('condition not met, no need to show tip')

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('onboarding tip drawing processed')

    def update_image(self, new_base_image):
        self.image = new_base_image
