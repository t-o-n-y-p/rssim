import logging

import pyglet

from game_object import GameObject


class TopAndBottomBar(GameObject):
    def __init__(self, batch, bar_group, border_group):
        super().__init__()
        self.logger = logging.getLogger('game.top_and_bottom_bar')
        self.logger.debug('------- START INIT -------')
        # create bottom bar for buttons
        batch.add(8, pyglet.gl.GL_QUADS, bar_group,
                  ('v2i/static', (0, 0, self.c['graphics']['bottom_bar_width'] - 1, 0,
                                  self.c['graphics']['bottom_bar_width'] - 1,
                                  self.c['graphics']['bottom_bar_height'] - 1,
                                  0, self.c['graphics']['bottom_bar_height'] - 1,
                                  0, self.c['graphics']['screen_resolution'][1] - 1,
                                  self.c['graphics']['screen_resolution'][0] - 1,
                                  self.c['graphics']['screen_resolution'][1] - 1,
                                  self.c['graphics']['screen_resolution'][0] - 1,
                                  self.c['graphics']['screen_resolution'][1] - 1 - self.c['graphics']['top_bar_height'],
                                  0, self.c['graphics']['screen_resolution'][1]
                                  - self.c['graphics']['top_bar_height'] - 1
                                  )),
                  ('c4B/static', (self.c['graphics']['bottom_bar_color'][0],
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
                                  self.c['graphics']['bottom_bar_color'][3],
                                  self.c['graphics']['bottom_bar_color'][0],
                                  self.c['graphics']['bottom_bar_color'][1],
                                  self.c['graphics']['bottom_bar_color'][2],
                                  self.c['graphics']['bottom_bar_color'][3]
                                  ))
                  )
        self.caption = pyglet.text.Label('Railway Station Simulator',
                                         font_name=self.c['graphics']['font_name'],
                                         font_size=self.c['graphics']['button_font_size'],
                                         x=10, y=self.c['graphics']['screen_resolution'][1]
                                         - self.c['graphics']['top_bar_height'] // 2,
                                         anchor_x='left', anchor_y='center',
                                         batch=batch, group=border_group)
        batch.add(28, pyglet.gl.GL_LINES, border_group,
                  ('v2i/static', (  # big generic border
                                  0, 0, self.c['graphics']['screen_resolution'][0] - 1, 0,
                                  self.c['graphics']['screen_resolution'][0] - 1, 0,
                                  self.c['graphics']['screen_resolution'][0] - 1,
                                  self.c['graphics']['screen_resolution'][1] - 1,
                                  self.c['graphics']['screen_resolution'][0] - 1,
                                  self.c['graphics']['screen_resolution'][1] - 1,
                                  0, self.c['graphics']['screen_resolution'][1] - 1,
                                  0, self.c['graphics']['screen_resolution'][1] - 1,
                                  0, 0,
                                  # big generic border layer 2
                                  1, 1, self.c['graphics']['screen_resolution'][0] - 2, 1,
                                  self.c['graphics']['screen_resolution'][0] - 2, 1,
                                  self.c['graphics']['screen_resolution'][0] - 2,
                                  self.c['graphics']['screen_resolution'][1] - 2,
                                  self.c['graphics']['screen_resolution'][0] - 2,
                                  self.c['graphics']['screen_resolution'][1] - 2,
                                  1, self.c['graphics']['screen_resolution'][1] - 2,
                                  1, self.c['graphics']['screen_resolution'][1] - 2,
                                  1, 1,
                                  # top bar border
                                  0, self.c['graphics']['screen_resolution'][1]
                                  - self.c['graphics']['top_bar_height'] - 1,
                                  self.c['graphics']['screen_resolution'][0] - 1,
                                  self.c['graphics']['screen_resolution'][1]
                                  - self.c['graphics']['top_bar_height'] - 1,
                                  0, self.c['graphics']['screen_resolution'][1]
                                  - self.c['graphics']['top_bar_height'],
                                  self.c['graphics']['screen_resolution'][0],
                                  self.c['graphics']['screen_resolution'][1]
                                  - self.c['graphics']['top_bar_height'],
                                  # bottom bar top border
                                  0, self.c['graphics']['bottom_bar_height'] - 1,
                                  self.c['graphics']['bottom_bar_width'] - 1,
                                  self.c['graphics']['bottom_bar_height'] - 1,
                                  0, self.c['graphics']['bottom_bar_height'] - 2,
                                  self.c['graphics']['bottom_bar_width'] - 2,
                                  self.c['graphics']['bottom_bar_height'] - 2,
                                  # bottom bar right border
                                  self.c['graphics']['bottom_bar_width'] - 1,
                                  self.c['graphics']['bottom_bar_height'] - 1,
                                  self.c['graphics']['bottom_bar_width'] - 1, 0,
                                  # bottom bar right border
                                  self.c['graphics']['bottom_bar_width'] - 2,
                                  self.c['graphics']['bottom_bar_height'] - 2,
                                  self.c['graphics']['bottom_bar_width'] - 2, 0
                                  )),
                  ('c4B/static', (255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
                                  255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
                                  255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
                                  255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
                                  255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
                                  255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255,
                                  255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255, 255, 0, 0, 255
                                  ))
                  )
        self.logger.debug('------- END INIT -------')
        self.logger.warning('top and bottom bar init completed')
