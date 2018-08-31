import logging

import pyglet

from game_object import GameObject


class TopAndBottomBar(GameObject):
    def __init__(self, batch, group):
        super().__init__()
        self.logger = logging.getLogger('game.top_and_bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        # self.top_bar_surface = pyglet.image.load('img/top_bar.png')
        batch.add(4, pyglet.gl.GL_QUADS, group,
                  ('v2i/static', (0, 0, self.c['graphics']['bottom_bar_width'], 0,
                                  self.c['graphics']['bottom_bar_width'],
                                  self.c['graphics']['bottom_bar_height'],
                                  0, self.c['graphics']['bottom_bar_height'])
                   ),
                  ('c4B', (self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3],
                           self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3],
                           self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3],
                           self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3]))
                  )
        batch.add(4, pyglet.gl.GL_QUADS, group,
                  ('v2i/static', (0, self.c['graphics']['screen_resolution'][1],
                                  self.c['graphics']['screen_resolution'][0],
                                  self.c['graphics']['screen_resolution'][1],
                                  self.c['graphics']['screen_resolution'][0],
                                  self.c['graphics']['screen_resolution'][1] - self.c['graphics']['top_bar_height'],
                                  0, self.c['graphics']['screen_resolution'][1] - self.c['graphics']['top_bar_height'])
                   ),
                  ('c4B', (self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3],
                           self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3],
                           self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3],
                           self.c['graphics']['bottom_bar_color'][0],
                           self.c['graphics']['bottom_bar_color'][1],
                           self.c['graphics']['bottom_bar_color'][2],
                           self.c['graphics']['bottom_bar_color'][3]))
                  )
        # self.top_bar_sprite = pyglet.sprite.Sprite(self.top_bar_surface,
        #                                            x=0, y=self.c['graphics']['screen_resolution'][1]
        #                                            - self.c['graphics']['top_bar_height'],
        #                                            batch=batch, group=group)
        # self.bottom_bar_surface = pyglet.image.load('img/bottom_bar.png')
        # self.bottom_bar_sprite = pyglet.sprite.Sprite(self.bottom_bar_surface,
        #                                               x=0, y=0,
        #                                               batch=batch, group=group)
        self.logger.debug('------- END INIT -------')
        self.logger.warning('top and bottom bar init completed')
