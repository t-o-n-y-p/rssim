"""
This module implements all buttons.
Buttons are used by object views to address player actions in the game.


__init__.py                                         implements decorators, constants and base Button class
accept_settings_button.py                           Accept button on settings screen
build_track_button.py                               Build track button on constructor screen
close_constructor_button.py                         Close constructor button on main game screen
close_game_button.py                                last button in the top right corner
close_schedule_button.py                            Close schedule button on main game screen
decrement_windowed_resolution_button.py             "-" button for windowed resolution on settings screen
fullscreen_button.py                                middle button in the top right corner (in windowed mode)
iconify_game_button.py                              first button in the top right corner
increment_windowed_resolution_button.py             "+" button for windowed resolution on settings screen
open_constructor_button.py                          Open constructor button on main game screen
open_schedule_button.py                             Open schedule button on main game screen
open_settings_button.py                             Open settings button in the bottom right corner
pause_game_button.py                                Pause button on main game screen
reject_settings_button.py                           Reject button on settings screen
reset_track_money_target_button.py                  Reset money target button inside track cell on constructor screen
restore_button.py                                   middle button in the top right corner (in fullscreen mode)
resume_game_button.py                               Resume button on main game screen
set_track_money_target_button.py                    Set money target button inside track cell on constructor screen
zoom_in_button.py                                   Zoom in button for game map on main game screen
zoom_out_button.py                                  Zoom out button for game map on main game screen
"""
from pyglet import gl
from pyglet.text import Label
from pyglet.window import mouse
from pyglet.resource import add_font


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


class Button:
    """
    Base class for all buttons in the app.
    """
    def __init__(self, surface, batch, groups, logger):
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

        :param surface:                         surface to draw all UI objects on
        :param batch:                           UI batch for the button
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        :param logger:                          telemetry instance
        """
        self.logger = logger
        self.is_activated = False
        self.to_activate_on_controller_init = None
        self.state = 'normal'
        self.surface = surface
        self.batch = batch
        self.groups = groups
        self.transparent = True
        self.paired_button = None
        self.vertex_list = None
        self.text_object = None
        self.text = None
        add_font('perfo-bold.ttf')
        self.font_name = None
        self.is_bold = False
        self.font_size = None
        self.position = (0, 0)
        self.button_size = ()
        self.x_margin = 0
        self.y_margin = 0
        self.on_click_action = None
        self.on_hover_action = None
        self.on_leave_action = None
        self.hand_cursor = self.surface.get_system_mouse_cursor(surface.CURSOR_HAND)
        self.default_cursor = self.surface.get_system_mouse_cursor(surface.CURSOR_DEFAULT)

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
        self.vertex_list = self.batch.add(4, gl.GL_QUADS, self.groups['button_background'],
                                          ('v2i', (self.position[0] + 2, self.position[1] + 2,
                                                   self.position[0] + self.button_size[0] - 2, self.position[1] + 2,
                                                   self.position[0] + self.button_size[0] - 2,
                                                   self.position[1] + self.button_size[1] - 2,
                                                   self.position[0] + 2, self.position[1] + self.button_size[1] - 2)
                                           ),
                                          ('c4B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
                                          )
        if not self.transparent:
            self.vertex_list.colors = (0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248)

        if self.text not in (None, ''):
            self.text_object = Label(self.text, font_name=self.font_name, bold=self.is_bold, font_size=self.font_size,
                                     x=self.position[0] + self.button_size[0] // 2,
                                     y=self.position[1] + self.button_size[1] // 2,
                                     anchor_x='center', anchor_y='center', batch=self.batch,
                                     group=self.groups['button_text'])

    @button_is_activated
    def on_deactivate(self):
        """
        Deactivates the button. Removes background and text label from the graphics memory.
        """
        self.is_activated = False
        self.vertex_list.delete()
        self.vertex_list = None
        if self.text_object is not None:
            self.text_object.delete()
            self.text_object = None

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
            if self.text_object is not None:
                self.text_object.x = self.position[0] + self.button_size[0] // 2
                self.text_object.y = self.position[1] + self.button_size[1] // 2

    def on_size_changed(self, new_button_size, new_font_size):
        """
        Applies new size for the button when notified about it.

        :param new_button_size:                 new width and height (including 2-pixel borders)
        :param new_font_size:                   new text label font size
        """
        self.button_size = new_button_size
        self.font_size = new_font_size
        if self.is_activated:
            self.text_object.font_size = self.font_size

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
                self.vertex_list.colors = (127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191)
                self.surface.set_mouse_cursor(self.hand_cursor)
                if self.on_hover_action is not None:
                    self.on_hover_action()
        # if cursor is not on the button and button is not normal, it means cursor has just left the button,
        # state and background color are changed to "normal" state
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
        self.vertex_list.colors = (191, 0, 0, 191, 191, 0, 0, 191, 191, 0, 0, 191, 191, 0, 0, 191)

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
        self.state = 'hover'
        self.vertex_list.colors = (127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191, 127, 0, 0, 191)
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
        if not self.transparent:
            self.vertex_list.colors = (0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248, 0, 0, 0, 248)
        else:
            self.vertex_list.colors = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.surface.set_mouse_cursor(self.default_cursor)
        if self.on_leave_action is not None:
            self.on_leave_action()
