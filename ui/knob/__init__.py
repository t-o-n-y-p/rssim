from abc import ABC, abstractmethod

from pyglet.gl import GL_POINTS
from pyglet.window import mouse

from ui import *


def knob_is_active(fn):
    def _handle_if_knob_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_knob_is_activated


def knob_is_not_active(fn):
    def _handle_if_knob_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_knob_is_not_activated


def value_update_mode_enabled(fn):
    def _handle_if_value_update_mode_enabled(*args, **kwargs):
        if args[0].value_update_mode:
            fn(*args, **kwargs)

    return _handle_if_value_update_mode_enabled


def left_mouse_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def cursor_is_over_the_knob(fn):
    def _handle_if_cursor_is_over_the_knob(*args, **kwargs):
        if args[1] in range(args[0].viewport.x1, args[0].viewport.x2) \
                and args[2] in range(args[0].viewport.y1, args[0].viewport.y2):
            fn(*args, **kwargs)

    return _handle_if_cursor_is_over_the_knob


class Knob(ABC):
    def __init__(self, on_value_update_action, parent_viewport, logger):
        self.on_value_update_action = on_value_update_action
        self.main_color = None
        self.background_color = None
        self.parent_viewport = parent_viewport
        self.logger = logger
        self.viewport = Viewport()
        self.is_activated = False
        self.knob_value_update_mode = False
        self.circle = None
        self.circle_vertices = []
        self.circle_colors = []
        self.circle_segments_per_step = None
        self.value_label = None
        self.on_window_resize_handlers = [self.on_window_resize, ]
        self.screen_resolution = (0, 0)
        self.opacity = 0
        self.start_value = None
        self.value_step = None
        self.maximum_steps = None
        self.current_step = None
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.value_update_mode = False
        self.state = 'normal'
        self.initial_cursor_position = (0, 0)
        self.knob_sensitivity = 5

    @abstractmethod
    def current_value_formula(self):
        pass

    def on_update_current_locale(self, new_locale):
        pass

    @final
    @knob_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.value_label.create()
        self.circle = BATCHES['ui_batch'].add(self.maximum_steps + 1, GL_POINTS, GROUPS['button_text'],
                                              ('v2f', self.circle_vertices), ('c4B', self.circle_colors))

    @final
    @knob_is_active
    def on_deactivate(self):
        self.is_activated = False

    @abstractmethod
    def on_window_resize(self, width, height):
        pass

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.value_label.on_update_opacity(self.opacity)
        self.circle_colors[3::4] = (self.opacity, ) * (len(self.circle_colors) // 4)
        if self.circle is not None:
            if self.opacity > 0:
                self.circle.colors = self.circle_colors
            else:
                self.circle.delete()
                self.circle = None

    @final
    def on_current_step_update(self, step):
        self.current_step = max(min(self.maximum_steps, step), 0)
        self.circle_colors = [
            *(*self.main_color, self.opacity) * (self.current_step + 1),
            *(*self.background_color, self.opacity) * (self.maximum_steps - self.current_step)
        ]
        if self.circle is not None:
            self.circle.colors = self.circle_colors

    @final
    @knob_is_active
    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.viewport.x1, self.viewport.x2) and y in range(self.viewport.y1, self.viewport.y2):
            if self.state != 'hover':
                self.state = 'hover'
                WINDOW.set_mouse_cursor(HAND_CURSOR)

        elif self.state != 'normal':
            self.state = 'normal'
            WINDOW.set_mouse_cursor(DEFAULT_CURSOR)

    @final
    @knob_is_active
    @cursor_is_over_the_knob
    @left_mouse_button
    def on_mouse_press(self, x, y, button, modifiers):
        self.value_update_mode = True
        self.initial_cursor_position = x, y

    @final
    @knob_is_active
    @left_mouse_button
    @value_update_mode_enabled
    def on_mouse_release(self, x, y, button, modifiers):
        self.value_update_mode = False
        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
        # self.on_value_update_action(self.current_value_formula())

    @final
    @knob_is_active
    def on_mouse_leave(self, x, y):
        self.state = 'normal'
        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)

    @final
    @value_update_mode_enabled
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if (y - dy - self.initial_cursor_position[1]) // self.knob_sensitivity \
                != (y - self.initial_cursor_position[1]) // self.knob_sensitivity:
            self.on_current_step_update(
                self.current_step
                + (y - self.initial_cursor_position[1]) // self.knob_sensitivity
                - (y - dy - self.initial_cursor_position[1]) // self.knob_sensitivity
            )
            self.value_label.on_update_args((self.current_value_formula(), ))
