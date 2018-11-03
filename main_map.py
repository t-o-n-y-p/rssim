from logging import getLogger

from pyglet.image import load
from pyglet.sprite import Sprite

from game_object import GameObject


class MainMap(GameObject):
    def __init__(self, batch, group, game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.main_map')
        self.logger.debug('------- START INIT -------')
        # load background texture tile
        self.sprite_image = load('img/map/4/full_map.png')
        self.sprite = Sprite(self.sprite_image, x=self.c.base_offset[0] + 120, y=self.c.base_offset[1],
                             batch=batch, group=group)

        self.logger.debug('main map loaded')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('main map init completed')

    def update_sprite(self, base_offset):
        self.sprite.position = (base_offset[0] + 120, base_offset[1])

    def on_track_unlock(self, track):
        self.sprite.image = load('img/map/{}/full_map.png'.format(track))
