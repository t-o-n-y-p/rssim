from pyglet import gl
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.window import mouse
from pyglet.resource import add_font


def _button_is_not_activated(fn):
    def _handle_if_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_is_not_activated


def _button_is_activated(fn):
    def _handle_if_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_is_activated


def _left_mouse_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
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


class Button:
    def __init__(self, surface, batch, groups):
        self.is_activated = False
        self.to_activate_on_controller_init = None
        self.state = 'normal'
        self.surface = surface
        self.batch = batch
        self.groups = groups
        self.transparent = True
        self.paired_button = None
        self.border_sprite_image = None
        self.border_sprite = None
        self.vertex_list = None
        self.text_object = None
        self.text = None
        add_font('perfo-bold.ttf')
        self.font_name = None
        self.is_bold = None
        self.font_size = None
        self.position = (0, 0)
        self.button_size = ()
        self.on_click_action = None
        self.on_hover_action = None
        self.on_leave_action = None
        self.hand_cursor = self.surface.get_system_mouse_cursor(surface.CURSOR_HAND)
        self.default_cursor = self.surface.get_system_mouse_cursor(surface.CURSOR_DEFAULT)

    @_button_is_not_activated
    def on_activate(self):
        self.is_activated = True
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.vertex_list = self.batch.add(4, gl.GL_QUADS, self.groups['button_background'],
                                          ('v2i', (self.position[0], self.position[1],
                                                   self.position[0] + self.button_size[0] - 1, self.position[1],
                                                   self.position[0] + self.button_size[0] - 1,
                                                   self.position[1] + self.button_size[1] - 1,
                                                   self.position[0], self.position[1] + self.button_size[1] - 1)
                                           ),
                                          ('c4B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                                          )
        if not self.transparent:
            self.vertex_list.colors = (0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248)

        self.border_sprite = Sprite(self.border_sprite_image, x=self.position[0], y=self.position[1], batch=self.batch,
                                    group=self.groups['button_border'])
        if self.text not in (None, ''):
            self.text_object = Label(self.text, font_name=self.font_name, bold=self.is_bold, font_size=self.font_size,
                                     x=self.position[0] + self.button_size[0] // 2,
                                     y=self.position[1] + self.button_size[1] // 2,
                                     anchor_x='center', anchor_y='center', batch=self.batch,
                                     group=self.groups['button_text'])

    @_button_is_activated
    def on_deactivate(self):
        self.is_activated = False
        self.vertex_list.delete()
        self.vertex_list = None
        self.border_sprite.delete()
        self.border_sprite = None
        if self.text_object is not None:
            self.text_object.delete()
            self.text_object = None

    def on_position_changed(self, position):
        self.position = position
        if self.is_activated:
            self.vertex_list.vertices = (self.position[0], self.position[1],
                                         self.position[0] + self.button_size[0] - 1, self.position[1],
                                         self.position[0] + self.button_size[0] - 1,
                                         self.position[1] + self.button_size[1] - 1,
                                         self.position[0], self.position[1] + self.button_size[1] - 1)
            self.border_sprite.position = position
            if self.text_object is not None:
                self.text_object.delete()
                self.text_object = Label(self.text, font_name=self.font_name, bold=self.is_bold,
                                         font_size=self.font_size,
                                         x=self.position[0] + self.button_size[0] // 2,
                                         y=self.position[1] + self.button_size[1] // 2,
                                         anchor_x='center', anchor_y='center', batch=self.batch,
                                         group=self.groups['button_text'])

    @_button_is_activated
    def handle_mouse_motion(self, x, y, dx, dy):
        if x in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and y in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            if self.state != 'pressed':
                self.state = 'hover'
                self.vertex_list.colors = (127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191)
                self.surface.set_mouse_cursor(self.hand_cursor)
                if self.on_hover_action is not None:
                    self.on_hover_action()
        else:
            if self.state != 'normal':
                self.state = 'normal'
                if not self.transparent:
                    self.vertex_list.colors = (0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248)
                else:
                    self.vertex_list.colors = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

                self.surface.set_mouse_cursor(self.default_cursor)
                if self.on_leave_action is not None:
                    self.on_leave_action()

    @_button_is_activated
    @_cursor_is_over_the_button
    @_left_mouse_button
    def handle_mouse_press(self, x, y, button, modifiers):
        self.state = 'pressed'
        self.vertex_list.colors = (191, 0, 0, 191, 191, 0, 0, 191, 191, 0, 0, 191, 191, 0, 0, 191)

    @_button_is_activated
    @_cursor_is_over_the_button
    @_button_is_pressed
    @_left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.state = 'hover'
        self.vertex_list.colors = (127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191)
        self.on_click_action(self)

    @_button_is_activated
    def handle_mouse_leave(self, x, y):
        self.state = 'normal'
        if not self.transparent:
            self.vertex_list.colors = (0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248)
        else:
            self.vertex_list.colors = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.surface.set_mouse_cursor(self.default_cursor)
