import logging

import pyglet

from game_object import GameObject


class TopAndBottomBar(GameObject):
    def __init__(self, batch, bar_group):
        super().__init__()
        self.logger = logging.getLogger('game.top_and_bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        self.main_frame = pyglet.image.load('img/main_frame_{}_{}.png'
                                            .format(self.c['graphics']['screen_resolution'][0],
                                                    self.c['graphics']['screen_resolution'][1]))
        self.main_frame_sprite = pyglet.sprite.Sprite(self.main_frame, x=0, y=0, batch=batch, group=bar_group)
        self.logger.debug('------- END INIT -------')
        self.logger.warning('top and bottom bar init completed')
