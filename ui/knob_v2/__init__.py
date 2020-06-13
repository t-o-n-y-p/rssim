from abc import ABC, abstractmethod
from math import cos, radians, sin
from typing import final

from pyglet.gl import GL_POINTS
from pyglet.window import mouse

from ui import BATCHES, GROUPS, WINDOW, HAND_CURSOR, DEFAULT_CURSOR, get_bottom_bar_height, UIObject, \
    is_not_active, is_active, HOVER, NORMAL


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


def next_knob_step_detected(fn):
    def _handle_if_next_knob_step_detected(*args, **kwargs):
        if (args[2] - args[4] - args[0].initial_cursor_y) // args[0].knob_sensitivity \
                != (args[2] - args[0].initial_cursor_y) // args[0].knob_sensitivity:
            fn(*args, **kwargs)

    return _handle_if_next_knob_step_detected


class KnobV2(UIObject, ABC):
    main_color: (int, int, int)
    background_color: (int, int, int)
    start_value: float
    value_step: float
    maximum_steps: int
    current_step: int

    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.knob_value_update_mode = False
        self.circle = None
        self.circle_vertices = []
        self.circle_colors = []
        self.circle_segments_per_step = None
        self.value_update_mode = False
        self.state = NORMAL
        self.initial_cursor_y = 0
        self.knob_sensitivity = 5
        self.on_mouse_press_handlers = [self.on_mouse_press]
        self.on_mouse_release_handlers = [self.on_mouse_release]
        self.on_mouse_motion_handlers = [self.on_mouse_motion]
        self.on_mouse_leave_handlers = [self.on_mouse_leave]
        self.on_mouse_drag_handlers = [self.on_mouse_drag]

    @abstractmethod
    def current_value_formula(self):
        pass

    @abstractmethod
    def on_init_state(self, value):
        pass

    @staticmethod
    def on_value_update():
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_current_step_update(
            self.current_step
            + (y - self.initial_cursor_y) // self.knob_sensitivity
            - (y - dy - self.initial_cursor_y) // self.knob_sensitivity
        )
        self.on_value_update()

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.circle:
            self.circle = BATCHES['ui_batch'].add(
                self.maximum_steps + 1, GL_POINTS, GROUPS['button_text'],
                ('v2f', self.circle_vertices), ('c4B', self.circle_colors)
            )

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.circle_colors[3::4] = (self.opacity, ) * (len(self.circle_colors) // 4)
        if self.circle:
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
        if self.circle:
            self.circle.colors = self.circle_colors

    @final
    @is_active
    def on_mouse_motion(self, x, y, dx, dy):
        if x in range(self.viewport.x1, self.viewport.x2) and y in range(self.viewport.y1, self.viewport.y2):
            if self.state != HOVER:
                self.state = HOVER
                WINDOW.set_mouse_cursor(HAND_CURSOR)

        elif self.state != NORMAL:
            self.state = NORMAL
            WINDOW.set_mouse_cursor(DEFAULT_CURSOR)

    @final
    @is_active
    @cursor_is_over_the_knob
    @left_mouse_button
    def on_mouse_press(self, x, y, button, modifiers):
        self.value_update_mode = True
        self.initial_cursor_y = y

    @final
    @is_active
    @left_mouse_button
    @value_update_mode_enabled
    def on_mouse_release(self, x, y, button, modifiers):
        self.value_update_mode = False
        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)

    @final
    @is_active
    def on_mouse_leave(self, x, y):
        self.state = NORMAL
        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)

    @final
    def on_circle_resize(self):
        circle_radius = 11 * get_bottom_bar_height(self.screen_resolution) / 32
        middle_point = (
            (self.viewport.x1 + self.viewport.x2) / 2,
            (self.viewport.y1 + self.viewport.y2) / 2 - circle_radius // 4
        )
        self.circle_vertices.clear()
        for i in range(self.maximum_steps):
            self.circle_vertices.append(
                middle_point[0] + circle_radius * cos(
                    radians(210 - i / self.maximum_steps * 240)
                )
            )
            self.circle_vertices.append(
                middle_point[1] + circle_radius * sin(
                    radians(210 - i / self.maximum_steps * 240)
                )
            )

        self.circle_vertices.append(middle_point[0] + circle_radius * cos(radians(-30)))
        self.circle_vertices.append(middle_point[1] + circle_radius * sin(radians(-30)))
        if self.circle:
            self.circle.vertices = self.circle_vertices
