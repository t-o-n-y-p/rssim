import logging

import pyglet

from game_object import GameObject
from exceptions import VideoAdapterNotSupportedException


class MainMap(GameObject):
    def __init__(self, batch, group, game_config):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.main_map')
        self.logger.debug('------- START INIT -------')
        # load background texture tile
        self.sprite = None
        try:
            self.sprite = pyglet.sprite.Sprite(pyglet.image.load('img/map/4/full_map.png'),
                                               x=self.c.base_offset[0] + 120,
                                               y=self.c.base_offset[1],
                                               batch=batch, group=group)
        except pyglet.gl.lib.GLException:
            raise VideoAdapterNotSupportedException

        self.logger.debug('main map loaded')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('main map init completed')

    def update_sprite(self, base_offset):
        self.sprite.position = (base_offset[0] + 120, base_offset[1])
