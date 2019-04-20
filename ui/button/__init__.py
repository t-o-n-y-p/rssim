from pyglet import gl
from pyglet.text import Label
from pyglet.window import mouse
from pyglet.resource import add_font

from ui import SURFACE, BATCHES, GROUPS, WHITE_RGB


BUTTON_BACKGROUND_RGB = {
    'normal': {False: (0.0, 0.0, 0.0), True: (0.0, 0.0, 0.0)},
    'hover': {False: (0.375, 0.0, 0.0), True: (0.5, 0.0, 0.0)},
    'pressed': {False: (0.5625, 0.0, 0.0), True: (0.75, 0.0, 0.0)}
}
BUTTON_BACKGROUND_ALPHA = {
    'normal': {False: 0.97, True: 0.0},
    'hover': {False: 1.0, True: 0.75},
    'pressed': {False: 1.0, True: 0.75}
}


def button_is_not_activated(fn):
    """
    Use this decorator to execute function only if button is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_is_not_activated


def button_is_activated(fn):
    """
    Use this decorator to execute function only if button is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_is_activated


def left_mouse_button(fn):
    """
    Use this decorator to execute function only if left mouse button was pressed/released.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def cursor_is_over_the_button(fn):
    """
    Use this decorator to execute function only if mouse cursor is over the button.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_cursor_is_over_the_button(*args, **kwargs):
        if args[1] in range(args[0].position[0] + 2, args[0].position[0] + args[0].button_size[0] - 2) \
                and args[2] in range(args[0].position[1] + 2, args[0].position[1] + args[0].button_size[1] - 2):
            fn(*args, **kwargs)

    return _handle_if_cursor_is_over_the_button


def button_is_pressed(fn):
    """
    Use this decorator to execute function only if the button is in "pressed" state.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_button_is_pressed(*args, **kwargs):
        if args[0].state == 'pressed':
            fn(*args, **kwargs)

    return _handle_if_button_is_pressed


def create_two_state_button(first_button_object, second_button_object):
    """
    Makes button pair from 2 Button objects representing single button with 2 states.

    :param first_button_object:                 Button object for the first state
    :param second_button_object:                Button object for the second state
    :return:                                    two paired Button objects
    """
    first_button_object.paired_button = second_button_object
    second_button_object.paired_button = first_button_object
    return first_button_object, second_button_object


class Button:
    """
    Base class for all buttons in the app.
    """
    def __init__(self, logger):
        """
        Properties:
            is_activated                        indicates if the button is active
            to_activate_on_controller_init      indicates if the button should be activated
                                                when corresponding object controller is activated
            state                               visible state of the button: normal, hover or pressed
            surface                             surface to draw all UI objects on
            batch                               UI batch for the button
            groups                              defines drawing layers (some labels and sprites behind others)
            transparent                         indicates if button needs black background or not
            paired_button                       second button if action is back-and-forth
                                                (e.g. pause/resume, fullscreen/restore)
            vertex_list                         button background primitive
            text_object                         text label
            text                                string for text label
            font_name                           button label font
            is_bold                             indicates if button label is bold
            base_font_size_property             font size relative coefficient from button size
            font_size                           button label font size
            position                            left bottom corner position (including 2-pixel border)
            button_size                         button width and height (including 2-pixel borders)
            x_margin                            margin from left app window edge
            y_margin                            margin from bottom app window edge
            on_click_action                     function to execute if user clicks on the button
            on_hover_action                     function to execute if user moves cursor over the button
            on_leave_action                     function to execute if user removes cursor from the button
            hand_cursor                         system hand cursor icon
            default_cursor                      system default cursor icon (arrow)
            logger                              telemetry instance

        :param logger:                          telemetry instance
        """
        self.logger = logger
        self.is_activated = False
        self.to_activate_on_controller_init = False
        self.state = 'normal'
        self.surface = SURFACE
        self.batch = BATCHES['ui_batch']
        self.groups = GROUPS
        self.transparent = True
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
        self.hand_cursor = self.surface.get_system_mouse_cursor(SURFACE.CURSOR_HAND)
        self.default_cursor = self.surface.get_system_mouse_cursor(SURFACE.CURSOR_DEFAULT)
        self.opacity = 0

    @button_is_not_activated
    def on_activate(self):
        """
        Activates the button. Creates background and text label for the button.
        """
        self.is_activated = True
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # 2 pixels are left for red button border,
        # that's why background position starts from (button_position + 2)
        if self.vertex_list is None:
            self.vertex_list = self.batch.add(4, gl.GL_QUADS, self.groups['button_background'],
                                              ('v2i', (self.position[0] + 2, self.position[1] + 2,
                                                       self.position[0] + self.button_size[0] - 2, self.position[1] + 2,
                                                       self.position[0] + self.button_size[0] - 2,
                                                       self.position[1] + self.button_size[1] - 2,
                                                       self.position[0] + 2, self.position[1] + self.button_size[1] - 2)
                                               ),
                                              ('c4f', (*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                                       * float(self.opacity) / 255.0,
                                                       *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                                       * float(self.opacity) / 255.0,
                                                       *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                                       * float(self.opacity) / 255.0,
                                                       *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                                       BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                                       * float(self.opacity) / 255.0)
                                               )
                                              )

        if self.text_label is None:
            if self.text not in (None, ''):
                self.text_label = Label(self.text, font_name=self.font_name, bold=self.is_bold,
                                        font_size=self.font_size, color=(*WHITE_RGB, self.opacity),
                                        x=self.position[0] + self.button_size[0] // 2,
                                        y=self.position[1] + self.button_size[1] // 2,
                                        anchor_x='center', anchor_y='center', batch=self.batch,
                                        group=self.groups['button_text'])

    @button_is_activated
    def on_deactivate(self, instant=False):
        """
        Deactivates the button. Removes background and text label from the graphics memory.
        """
        self.is_activated = False
        if instant:
            self.opacity = 0
            self.vertex_list.delete()
            self.vertex_list = None
            if self.text_label is not None:
                self.text_label.delete()
                self.text_label = None

    def on_position_changed(self, position):
        """
        Applies new position for the button when notified about it.

        :param position:                        new button position (including 2-pixel borders)
        """
        self.position = position
        if self.is_activated:
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

    def on_size_changed(self, new_button_size):
        """
        Applies new size for the button when notified about it.

        :param new_button_size:                 new width and height (including 2-pixel borders)
        """
        self.button_size = new_button_size
        self.font_size = int(self.base_font_size_property * min(self.button_size))
        if self.is_activated:
            self.text_label.font_size = self.font_size

    @button_is_activated
    def handle_mouse_motion(self, x, y, dx, dy):
        """
        When mouse cursor is moved, checks if mouse is over the button or not, changes button state
        and calls handlers if cursor has just left the button or was just moved over it.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param dx:              relative X position from the previous mouse position
        :param dy:              relative Y position from the previous mouse position
        """
        # if cursor is on the button and button is not pressed, it means cursor was just moved over the button,
        # state and background color are changed to "hover" state
        if x in range(self.position[0] + 2, self.position[0] + self.button_size[0] - 2) \
                and y in range(self.position[1] + 2, self.position[1] + self.button_size[1] - 2):
            if self.state != 'pressed':
                self.state = 'hover'
                self.vertex_list.colors = (*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0,
                                           *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0,
                                           *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0,
                                           *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0)
                self.surface.set_mouse_cursor(self.hand_cursor)
                if self.on_hover_action is not None:
                    self.on_hover_action()
        # if cursor is not on the button and button is not normal, it means cursor has just left the button,
        # state and background color are changed to "normal" state
        else:
            if self.state != 'normal':
                self.state = 'normal'
                self.vertex_list.colors = (*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0,
                                           *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0,
                                           *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0,
                                           *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                           BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                           * float(self.opacity) / 255.0)
                self.surface.set_mouse_cursor(self.default_cursor)
                if self.on_leave_action is not None:
                    self.on_leave_action()

    @button_is_activated
    @cursor_is_over_the_button
    @left_mouse_button
    def handle_mouse_press(self, x, y, button, modifiers):
        """
        When mouse cursor is over the button and left button is pressed, changes button state.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param button:          determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.state = 'pressed'
        self.vertex_list.colors = (*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0)

    @button_is_activated
    @cursor_is_over_the_button
    @button_is_pressed
    @left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        """
        When mouse cursor is over the button and left button is released, changes button state
        and calls appropriate action assigned to the button.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param button:          determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.state = 'normal'
        self.vertex_list.colors = (*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0)
        self.surface.set_mouse_cursor(self.default_cursor)
        self.on_click_action(self)

    @button_is_activated
    def handle_mouse_leave(self, x, y):
        """
        When mouse cursor leaves the app window, changes button state because cursor is obviously not over the button.
        Without this handler, in some cases buttons stay in "hover" state when mouse cursor leaves the button placed
        near the app window edge.

        :param x:               mouse cursor X position
        :param y:               mouse cursor Y position
        """
        self.state = 'normal'
        self.vertex_list.colors = (*BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0,
                                   *BUTTON_BACKGROUND_RGB[self.state][self.transparent],
                                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent]
                                   * float(self.opacity) / 255.0)
        self.surface.set_mouse_cursor(self.default_cursor)
        if self.on_leave_action is not None:
            self.on_leave_action()

    def on_update_opacity(self):
        if self.is_activated and self.opacity < 255:
            self.opacity += 15
            self.on_update_sprite_opacity()

        if not self.is_activated and self.opacity > 0:
            self.opacity -= 15
            self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        if self.opacity <= 0:
            self.vertex_list.delete()
            self.vertex_list = None
            if self.text_label is not None:
                self.text_label.delete()
                self.text_label = None

        else:
            self.vertex_list.colors[3::4] \
                = (BUTTON_BACKGROUND_ALPHA[self.state][self.transparent] * float(self.opacity) / 255.0,
                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent] * float(self.opacity) / 255.0,
                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent] * float(self.opacity) / 255.0,
                   BUTTON_BACKGROUND_ALPHA[self.state][self.transparent] * float(self.opacity) / 255.0)
            if self.text_label is not None:
                self.text_label.color = (*WHITE_RGB, self.opacity)
