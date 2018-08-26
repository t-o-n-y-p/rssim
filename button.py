import logging

import pyglet

from game_object import GameObject


class Button(GameObject):
    def __init__(self, position, button_size, text, on_click, draw_only_if_game_paused,
                 batch, button_group, text_group):
        super().__init__()
        self.logger = logging.getLogger('game.{} button'.format(text[0]))
        self.logger.debug('------- START INIT -------')
        self.draw_only_if_game_paused = draw_only_if_game_paused
        self.logger.debug('draw only if game paused set: {}'.format(self.draw_only_if_game_paused))
        self.allowed_to_be_drawn = False
        self.logger.debug('allowed_to_be_drawn set: {}'.format(self.allowed_to_be_drawn))
        self.state = 'normal'
        self.logger.debug('state set: {}'.format(self.state))
        self.position = position
        self.button_size = button_size
        self.batch = batch
        self.button_group = button_group
        self.text_group = text_group
        self.logger.debug('position set: {}'.format(self.position))
        self.text_objects = []
        self.on_click = on_click
        self.on_click_actual = self.on_click[0]
        self.logger.debug('on click action set: {}'.format(self.on_click_actual))
        self.image = {'normal': pyglet.image.load('img/button_{}_{}_normal.png'
                                                  .format(self.button_size[0], self.button_size[1])),
                      'hover': pyglet.image.load('img/button_{}_{}_hover.png'
                                                 .format(self.button_size[0], self.button_size[1])),
                      'pressed': pyglet.image.load('img/button_{}_{}_pressed.png'
                                                   .format(self.button_size[0], self.button_size[1]))}
        self.logger.debug('images set: {}'.format(self.image))
        self.sprite_actual = pyglet.sprite.Sprite(self.image['normal'],
                                                  x=self.position[0],
                                                  y=self.c['graphics']['screen_resolution'][1] - self.position[1]
                                                  - self.image['normal'].height,
                                                  batch=self.batch, group=self.button_group)
        self.text = text

        self.text_object_actual = pyglet.text.Label(text[0],
                                                    font_name=self.c['graphics']['font_name'],
                                                    font_size=self.c['graphics']['button_font_size'],
                                                    x=self.position[0] + self.button_size[0] // 2,
                                                    y=self.c['graphics']['screen_resolution'][1]
                                                    - (self.position[1] + self.button_size[1] // 2),
                                                    anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group)
        self.text_object_actual_text = self.text[0]
        self.logger.debug('text objects set: {}'.format(self.text))
        self.logger.debug('current text set: {}'.format(self.text[0]))
        self.logger.debug('------- END INIT -------')
        self.logger.warning('button init completed')

    def update(self, game_paused):
        self.logger.debug('------- START UPDATING -------')
        if not game_paused and self.draw_only_if_game_paused:
            self.allowed_to_be_drawn = False
            if self.sprite_actual is not None:
                self.sprite_actual.delete()
                self.sprite_actual = None

            if self.text_object_actual is not None:
                self.text_object_actual.delete()
                self.text_object_actual = None
            self.logger.debug('game is not paused and this button is drawn only if game paused')
            self.logger.debug('so hide the button')
        else:
            self.allowed_to_be_drawn = True
            if self.sprite_actual is not None:
                self.sprite_actual.delete()
                self.sprite_actual = None

            if self.text_object_actual is not None:
                self.text_object_actual.delete()
                self.text_object_actual = None

            self.sprite_actual = pyglet.sprite.Sprite(self.image['normal'],
                                                      x=self.position[0],
                                                      y=self.c['graphics']['screen_resolution'][1] - self.position[1]
                                                      - self.image['normal'].height,
                                                      batch=self.batch, group=self.button_group)
            self.text_object_actual = pyglet.text.Label(self.text[0],
                                                        font_name=self.c['graphics']['font_name'],
                                                        font_size=self.c['graphics']['button_font_size'],
                                                        x=self.position[0] + self.button_size[0] // 2,
                                                        y=self.c['graphics']['screen_resolution'][1]
                                                        - (self.position[1] + self.button_size[1] // 2),
                                                        anchor_x='center', anchor_y='center',
                                                        batch=self.batch, group=self.text_group)

            self.logger.info('button is always present on the screen')
            self.logger.info('so it is not hidden')

        self.logger.debug('------- END UPDATING -------')
        self.logger.info('button updated')

    def handle_mouse_motion(self, x, y, dx, dy):
        y = self.c['graphics']['screen_resolution'][1] - y
        if x in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and y in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            if self.state != 'pressed':
                self.state = 'hover'
                if self.sprite_actual is not None:
                    self.sprite_actual.delete()
                    self.sprite_actual = None

                self.sprite_actual = pyglet.sprite.Sprite(self.image['hover'],
                                                          x=self.position[0],
                                                          y=self.c['graphics']['screen_resolution'][1]
                                                          - self.position[1] - self.image['normal'].height,
                                                          batch=self.batch, group=self.button_group)
                self.logger.info('cursor is on the button')
        else:
            self.state = 'normal'
            if self.sprite_actual is not None:
                self.sprite_actual.delete()
                self.sprite_actual = None

            self.sprite_actual = pyglet.sprite.Sprite(self.image['normal'],
                                                      x=self.position[0],
                                                      y=self.c['graphics']['screen_resolution'][1]
                                                      - self.position[1] - self.image['normal'].height,
                                                      batch=self.batch, group=self.button_group)
            self.logger.debug('cursor is not on the button')

    def handle_mouse_press(self, x, y, button, modifiers):
        y = self.c['graphics']['screen_resolution'][1] - y
        if x in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and y in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2) \
                and button == pyglet.window.mouse.LEFT:
            self.state = 'pressed'
            self.sprite_actual.delete()
            self.sprite_actual = pyglet.sprite.Sprite(self.image['pressed'],
                                                      x=self.position[0],
                                                      y=self.c['graphics']['screen_resolution'][1]
                                                      - self.position[1] - self.image['normal'].height,
                                                      batch=self.batch, group=self.button_group)
            self.logger.info('cursor is on the button and user holds mouse button')

    def handle_mouse_release(self, x, y, button, modifiers):
        if self.state == 'pressed' and button == pyglet.window.mouse.LEFT:
            self.state = 'hover'
            self.sprite_actual.delete()
            self.sprite_actual = pyglet.sprite.Sprite(self.image['hover'],
                                                      x=self.position[0],
                                                      y=self.c['graphics']['screen_resolution'][1]
                                                      - self.position[1] - self.image['normal'].height,
                                                      batch=self.batch, group=self.button_group)
            self.logger.info('cursor is on the button and user released mouse button')
            self.logger.info('start onclick action')
            self.on_click_actual(self)
            if self.on_click_actual == self.on_click[0] and len(self.on_click) == 2:
                self.on_click_actual = self.on_click[1]
                self.logger.info('button is switched to second action')
            else:
                self.on_click_actual = self.on_click[0]
                self.logger.debug('button has only 1 action, so it remains the same')

            if self.text_object_actual_text == self.text[0] and len(self.text) == 2:
                self.text_object_actual_text = self.text[1]
                if self.text_object_actual is not None:
                    self.text_object_actual.delete()
                    self.text_object_actual = None

                self.text_object_actual = pyglet.text.Label(self.text[1],
                                                            font_name=self.c['graphics']['font_name'],
                                                            font_size=self.c['graphics']['button_font_size'],
                                                            x=self.position[0] + self.button_size[0] // 2,
                                                            y=self.c['graphics']['screen_resolution'][1]
                                                              - (self.position[1] + self.button_size[1] // 2),
                                                            anchor_x='center', anchor_y='center',
                                                            batch=self.batch, group=self.text_group)
                self.logger.info('button is switched to second text')
            else:
                self.text_object_actual_text = self.text[0]
                if self.text_object_actual is not None:
                    self.text_object_actual.delete()
                    self.text_object_actual = None
                self.text_object_actual = pyglet.text.Label(self.text[0],
                                                            font_name=self.c['graphics']['font_name'],
                                                            font_size=self.c['graphics']['button_font_size'],
                                                            x=self.position[0] + self.button_size[0] // 2,
                                                            y=self.c['graphics']['screen_resolution'][1]
                                                              - (self.position[1] + self.button_size[1] // 2),
                                                            anchor_x='center', anchor_y='center',
                                                            batch=self.batch, group=self.text_group)
                self.logger.debug('button has only 1 text, so it remains the same')
