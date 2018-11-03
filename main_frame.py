from logging import getLogger

from pyglet.image import load
from pyglet.sprite import Sprite

from game_object import GameObject


class MainFrame(GameObject):
    def __init__(self, batch, main_frame_group, game_config):
        super().__init__(game_config)
        self.logger = getLogger('game.top_and_bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        self.main_frame = load('img/main_frame/main_frame_{}_{}.png'.format(self.c.screen_resolution[0],
                                                                            self.c.screen_resolution[1]))
        self.main_frame_sprite = Sprite(self.main_frame, x=0, y=0, batch=batch, group=main_frame_group)
        self.logger.debug('------- END INIT -------')
        self.logger.warning('top and bottom bar init completed')
