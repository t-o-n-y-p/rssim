from pyglet import gl
from pyglet.text import Label
from pyglet.window import mouse
from pyglet.resource import add_font

from ui import *
from database import USER_DB_CURSOR


def button_is_not_activated(fn):
    def _handle_if_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_is_not_activated


def button_is_activated(fn):
    def _handle_if_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_is_activated


def button_is_activated_or_disabled(fn):
    def _handle_if_is_activated_or_disabled(*args, **kwargs):
        if args[0].is_activated or args[0].disabled_state:
            fn(*args, **kwargs)

    return _handle_if_is_activated_or_disabled


def left_mouse_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def cursor_is_over_the_button(fn):
    def _handle_if_cursor_is_over_the_button(*args, **kwargs):
        if args[1] in range(args[0].position[0] + 2, args[0].position[0] + args[0].button_size[0] - 2) \
                and args[2] in range(args[0].position[1] + 2, args[0].position[1] + args[0].button_size[1] - 2):
            fn(*args, **kwargs)

    return _handle_if_cursor_is_over_the_button


def button_is_pressed(fn):
    def _handle_if_button_is_pressed(*args, **kwargs):
        if args[0].state == 'pressed':
            fn(*args, **kwargs)

    return _handle_if_button_is_pressed


def create_two_state_button(first_button_object, second_button_object):
    first_button_object.paired_button = second_button_object
    second_button_object.paired_button = first_button_object
    return first_button_object, second_button_object


# button background RGB color for non-transparent and transparent button
BUTTON_BACKGROUND_RGB = {
    'normal': {False: (0.0, 0.0, 0.0), True: (0.0, 0.0, 0.0)},
    'hover': {False: (0.375, 0.0, 0.0), True: (0.5, 0.0, 0.0)},
    'pressed': {False: (0.5625, 0.0, 0.0), True: (0.75, 0.0, 0.0)}
}
# button background alpha for non-transparent and transparent button
BUTTON_BACKGROUND_ALPHA = {
    'normal': {False: 1.0, True: 0.0},
    'hover': {False: 1.0, True: 0.75},
    'pressed': {False: 1.0, True: 0.75}
}


class Button:
    def __init__(self, logger):
        self.logger = logger
        self.is_activated = False
        self.to_activate_on_controller_init = False
        self.state = 'normal'
        self.transparent = True
        self.invisible = False
        self.paired_button = None
        self.vertex_list = None
        self.text_label = None
        self.text = None
        add_font('perfo-bold.ttf')
        self.font_name = None
        self.is_bold = False
        self.base_font_size_property = 0.5
        self.font_size = 10
        self.position = (0, 0)
        self.button_size = (0, 0)
        self.x_margin = 0
        self.y_margin = 0
        self.on_click_action = None
        self.on_hover_action = None
        self.on_leave_action = None
        self.hand_cursor = SURFACE.get_system_mouse_cursor(SURFACE.CURSOR_HAND)
        self.default_cursor = SURFACE.get_system_mouse_cursor(SURFACE.CURSOR_DEFAULT)
        self.opacity = 0
        self.disabled_state = False
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]

    @button_is_not_activated
    def on_activate(self, instant=False):
        self.is_activated = True
        self.disabled_state = False
        if instant:
            self.opacity = 255

        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # 2 pixels are left for red button border,
        # that's why background position starts from (button_position + 2)
        if self.vertex_list is None and not self.invisible:
            self.vertex_list \
                = BATCHES['ui_batch'].add(4, gl.GL_QUADS, GROUPS['button_background'],
                                          ('v2i', (self.position[0] + 2, self.position[1] + 2,
                                                   self.position[0] + self.button_size[0] - 2, self.position[1] + 2,
                                                   self.position[0] + self.button_size[0] - 2,
                                                   self.position[1] + self.button_size[1] - 2,
                                                   self.position[0] + 2, self.position[1] + self.button_size[1] - 2)
                                           ),
                                          ('c4f', ((*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                                    BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                                    * float(self.opacity) / 255.0)
                                                   * 4)
                                           )
                                          )

        if self.text_label is None:
            if self.text not in (None, ''):
                self.text_label = Label(self.text, font_name=self.font_name, bold=self.is_bold,
                                        font_size=self.font_size, color=(*WHITE_RGB, self.opacity),
                                        x=self.position[0] + self.button_size[0] // 2,
                                        y=self.position[1] + self.button_size[1] // 2,
                                        anchor_x='center', anchor_y='center', batch=BATCHES['ui_batch'],
                                        group=GROUPS['button_text'])
        else:
            self.text_label.color = (*WHITE_RGB, self.opacity)

    @button_is_activated_or_disabled
    def on_deactivate(self, instant=False):
        self.is_activated = False
        self.disabled_state = False
        if instant:
            self.opacity = 0
            if self.vertex_list is not None:
                self.vertex_list.delete()
                self.vertex_list = None

            if self.text_label is not None:
                self.text_label.delete()
                self.text_label = None

    def on_disable(self, instant=False):
        self.on_deactivate()
        self.disabled_state = True
        if instant:
            self.opacity = 255

        if self.vertex_list is not None:
            self.vertex_list.delete()
            self.vertex_list = None

        if self.text_label is None:
            if self.text not in (None, ''):
                self.text_label = Label(self.text, font_name=self.font_name, bold=self.is_bold,
                                        font_size=self.font_size, color=(*GREY_RGB, self.opacity),
                                        x=self.position[0] + self.button_size[0] // 2,
                                        y=self.position[1] + self.button_size[1] // 2,
                                        anchor_x='center', anchor_y='center', batch=BATCHES['ui_batch'],
                                        group=GROUPS['button_text'])
        else:
            self.text_label.color = (*GREY_RGB, self.opacity)

    @button_is_activated_or_disabled
    def on_move(self):
        if self.vertex_list is not None:
            # move the button background to the new position
            # 2 pixels are left for red button border,
            # that's why background position starts from (button_position + 2)
            self.vertex_list.vertices = (self.position[0] + 2, self.position[1] + 2,
                                         self.position[0] + self.button_size[0] - 2, self.position[1] + 2,
                                         self.position[0] + self.button_size[0] - 2,
                                         self.position[1] + self.button_size[1] - 2,
                                         self.position[0] + 2, self.position[1] + self.button_size[1] - 2)
        # move the text label to the center of the button
        if self.text_label is not None:
            self.text_label.x = self.position[0] + self.button_size[0] // 2
            self.text_label.y = self.position[1] + self.button_size[1] // 2

    def on_resize(self):
        self.font_size = int(self.base_font_size_property * min(self.button_size))
        if self.text_label is not None:
            self.text_label.font_size = self.font_size

    @button_is_activated
    def handle_mouse_motion(self, x, y, dx, dy):
        # if cursor is on the button and button is not pressed, it means cursor was just moved over the button,
        # state and background color are changed to "hover" state
        if x in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and y in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            if self.state != 'pressed':
                self.state = 'hover'
                if self.vertex_list is not None:
                    self.vertex_list.colors = ((*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                               BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                               * float(self.opacity) / 255.0) * 4)

                SURFACE.set_mouse_cursor(self.hand_cursor)
                if self.on_hover_action is not None:
                    self.on_hover_action()
        # if cursor is not on the button and button is not normal, it means cursor has just left the button,
        # state and background color are changed to "normal" state
        else:
            if self.state != 'normal':
                self.state = 'normal'
                if self.vertex_list is not None:
                    self.vertex_list.colors = ((*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                               BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                               * float(self.opacity) / 255.0) * 4)

                SURFACE.set_mouse_cursor(self.default_cursor)
                if self.on_leave_action is not None:
                    self.on_leave_action()

    @button_is_activated
    @cursor_is_over_the_button
    @left_mouse_button
    def handle_mouse_press(self, x, y, button, modifiers):
        self.state = 'pressed'
        if self.vertex_list is not None:
            self.vertex_list.colors = ((*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                       * float(self.opacity) / 255.0) * 4)

    @button_is_activated
    @cursor_is_over_the_button
    @button_is_pressed
    @left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.state = 'hover'
        if self.vertex_list is not None:
            self.vertex_list.colors = ((*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                       * float(self.opacity) / 255.0) * 4)

        SURFACE.set_mouse_cursor(self.default_cursor)
        self.on_click_action(self)

    @button_is_activated
    def handle_mouse_leave(self, x, y):
        self.state = 'normal'
        if self.vertex_list is not None:
            self.vertex_list.colors = ((*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                       * float(self.opacity) / 255.0) * 4)

        SURFACE.set_mouse_cursor(self.default_cursor)
        if self.on_leave_action is not None:
            self.on_leave_action()

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity <= 0:
            if self.vertex_list is not None:
                self.vertex_list.delete()
                self.vertex_list = None

            if self.text_label is not None:
                self.text_label.delete()
                self.text_label = None

        else:
            if self.vertex_list is not None:
                self.vertex_list.colors[3::4] \
                    = ((BUTTON_BACKGROUND_ALPHA[self.state][self.transparent] * float(self.opacity) / 255.0, ) * 4)

            if self.text_label is not None:
                self.text_label.color = (*self.text_label.color[0:3], self.opacity)

    def on_update_current_locale(self, new_locale):
        pass


class UIButton(Button):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger=logger)
        self.parent_viewport = parent_viewport
        self.screen_resolution = (1280, 720)

    def get_position(self):
        pass

    def get_size(self):
        pass

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.position = self.get_position()
        self.button_size = self.get_size()
        self.on_move()
        self.on_resize()

    def on_position_changed(self):
        self.position = self.get_position()
        self.on_move()


class MapButton(Button):
    def __init__(self, logger):
        super().__init__(logger=logger)
        USER_DB_CURSOR.execute('SELECT last_known_base_offset FROM graphics')
        self.base_offset = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        USER_DB_CURSOR.execute('SELECT zoom_out_activated FROM graphics')
        self.zoom_out_activated = bool(USER_DB_CURSOR.fetchone()[0])
        if self.zoom_out_activated:
            self.scale = 0.5
        else:
            self.scale = 1.0

    def get_position(self):
        pass

    def get_size(self):
        pass

    def on_change_base_offset(self, base_offset):
        self.base_offset = base_offset
        self.position = self.get_position()
        self.on_move()

    def on_change_scale(self, new_scale):
        self.scale = new_scale
        self.button_size = self.get_size()
        self.on_resize()
