import logging

import pyglet

from game_object import GameObject


def _button_is_visible(fn):
    def _handle_mouse_if_is_visible(*args, **kwargs):
        if args[0].is_visible:
            fn(*args, **kwargs)

    return _handle_mouse_if_is_visible


def _left_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == pyglet.window.mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def _cursor_is_over_the_button(fn):
    def _handle_if_cursor_is_over_the_button(*args, **kwargs):
        if args[1] in range(args[0].position[0] + 2, args[0].position[0] + args[0].button_size[0] - 2) \
                and args[2] in range(args[0].position[1] + 2, args[0].position[1] + args[0].button_size[1] - 2):
            fn(*args, **kwargs)

    return _handle_if_cursor_is_over_the_button


def _button_is_pressed(fn):
    def _handle_if_button_is_pressed(*args, **kwargs):
        if args[0].state == 'pressed':
            fn(*args, **kwargs)

    return _handle_if_button_is_pressed


class Button(GameObject):
    def __init__(self, position, button_size, text, font_size, on_click, is_visible,
                 batch, button_group, text_group, borders_group, game_config, logs_description):
        super().__init__(game_config)
        self.logger = logging.getLogger('game.{}_button'.format(logs_description))
        self.logger.debug('------- START INIT -------')
        self.is_visible = is_visible
        self.logger.debug('allowed_to_be_drawn set: {}'.format(self.is_visible))
        self.state = 'normal'
        self.logger.debug('state set: {}'.format(self.state))
        self.position = position
        self.button_size = button_size
        self.batch = batch
        self.button_group = button_group
        self.text_group = text_group
        self.borders_group = borders_group
        self.logger.debug('position set: {}'.format(self.position))
        self.text_objects = []
        self.on_click = on_click
        self.on_click_actual = self.on_click[0]
        self.logger.debug('on click action set: {}'.format(self.on_click_actual))
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.vertex_list \
            = batch.add(4, pyglet.gl.GL_QUADS, button_group,
                        ('v2i/static', (self.position[0],
                                        self.position[1],
                                        self.position[0] + self.button_size[0] - 1,
                                        self.position[1],
                                        self.position[0] + self.button_size[0] - 1,
                                        self.position[1] + self.button_size[1] - 1,
                                        self.position[0],
                                        self.position[1] + self.button_size[1] - 1)),
                        ('c4B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                        )
        self.border_sprite_image = pyglet.image.load('img/button_border_{}_{}.png'
                                                     .format(self.button_size[0], self.button_size[1]))
        self.border_sprite = pyglet.sprite.Sprite(self.border_sprite_image, x=self.position[0], y=self.position[1],
                                                  batch=self.batch, group=self.borders_group)
        self.text = text
        self.font_size = font_size
        self.text_object_actual = pyglet.text.Label(text[0],
                                                    font_name=self.c.font_name,
                                                    font_size=self.font_size,
                                                    x=self.position[0] + self.button_size[0] // 2,
                                                    y=self.position[1] + self.button_size[1] // 2,
                                                    anchor_x='center', anchor_y='center',
                                                    batch=self.batch, group=self.text_group)
        self.text_object_actual_text = self.text[0]
        self.logger.debug('text objects set: {}'.format(self.text))
        self.logger.debug('current text set: {}'.format(self.text[0]))
        if self.is_visible:
            self.on_button_is_visible()
        else:
            self.on_button_is_not_visible()

        self.logger.debug('------- END INIT -------')
        self.logger.warning('button init completed')

    def on_button_is_visible(self):
        self.is_visible = True
        if self.vertex_list is None:
            self.vertex_list = self.batch.add(4, pyglet.gl.GL_QUADS, self.button_group,
                                              ('v2i/static', (self.position[0],
                                                              self.position[1],
                                                              self.position[0] + self.button_size[0] - 1,
                                                              self.position[1],
                                                              self.position[0] + self.button_size[0] - 1,
                                                              self.position[1] + self.button_size[1] - 1,
                                                              self.position[0],
                                                              self.position[1] + self.button_size[1] - 1)),
                                              ('c4B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))

        self.border_sprite.visible = True

        if self.text_object_actual is None:
            self.text_object_actual = pyglet.text.Label(self.text_object_actual_text, font_name=self.c.font_name,
                                                        font_size=self.font_size,
                                                        x=self.position[0] + self.button_size[0] // 2,
                                                        y=self.position[1] + self.button_size[1] // 2,
                                                        anchor_x='center', anchor_y='center', batch=self.batch,
                                                        group=self.text_group)

    def on_button_is_not_visible(self):
        self.is_visible = False
        if self.vertex_list is not None:
            self.vertex_list.delete()
            self.vertex_list = None

        self.border_sprite.visible = False

        if self.text_object_actual is not None:
            self.text_object_actual.delete()
            self.text_object_actual = None

    def update(self, game_paused):
        pass

    @_button_is_visible
    def handle_mouse_motion(self, x, y, dx, dy):
        if x in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and y in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            if self.state != 'pressed':
                self.state = 'hover'
                self.vertex_list.colors = (127, 0, 0, 127, 127, 0, 0, 127, 127, 0, 0, 127, 127, 0, 0, 127)
                self.logger.info('cursor is on the button')
        else:
            if self.state != 'normal':
                self.state = 'normal'
                self.vertex_list.colors = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                self.logger.debug('cursor is not on the button')

    @_button_is_visible
    @_cursor_is_over_the_button
    @_left_button
    def handle_mouse_press(self, x, y, button, modifiers):
        self.state = 'pressed'
        self.vertex_list.colors = (191, 0, 0, 127, 191, 0, 0, 127, 191, 0, 0, 127, 191, 0, 0, 127)
        self.logger.info('cursor is on the button and user holds mouse button')

    @_button_is_visible
    @_button_is_pressed
    @_left_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.state = 'hover'
        self.vertex_list.colors = (127, 0, 0, 127, 127, 0, 0, 127, 127, 0, 0, 127, 127, 0, 0, 127)
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
            self.text_object_actual.text = self.text[1]
            self.logger.info('button is switched to second text')
        else:
            self.text_object_actual_text = self.text[0]
            self.text_object_actual.text = self.text[0]
            self.logger.debug('button has only 1 text, so it remains the same')

    @_button_is_visible
    def handle_mouse_leave(self, x, y):
        self.state = 'normal'
        self.vertex_list.colors = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.logger.debug('cursor is not on the button')
