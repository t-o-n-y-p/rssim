import logging

import pyglet

from game_object import GameObject


class NotSupportedVideoAdapterException(Exception):
    def __init__(self):
        self.surface = None
        self.handler = None
        self.text = 'Your video adapter is not supported.'
        self.caption = 'Video Adapter Error'


class MainMap(GameObject):
    def __init__(self, batch, group):
        super().__init__()
        self.logger = logging.getLogger('game.main_map')
        self.logger.debug('------- START INIT -------')
        # load background texture tile
        self.sprite = None
        try:
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load('img/map/4/full_map.png'),
                                               x=self.c['graphics']['base_offset'][0],
                                               y=self.c['graphics']['base_offset'][1],
                                               batch=batch, group=group)
        except pyglet.gl.lib.GLException:
            raise NotSupportedVideoAdapterException

        self.logger.debug('main map loaded')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('main map init completed')

    def update_sprite(self, base_offset):
        self.sprite.position = base_offset
