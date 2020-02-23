from abc import ABC, abstractmethod

from pyglet.gl import GL_LINE_STRIP

from ui import *


class Knob(ABC):
    def __init__(self, parent_viewport, logger):
        self.main_color = None
        self.background_color = None
        self.parent_viewport = parent_viewport
        self.logger = logger
        self.viewport = Viewport()
        self.is_activated = False
        self.knob_value_update_mode = False
        self.circle = None
        self.circle_vertices = ()
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

    @abstractmethod
    def current_value_formula(self):
        pass

    def on_update_current_locale(self, new_locale):
        pass

    def on_activate(self):
        self.is_activated = True
        # self.value_label.create()
        self.circle = BATCHES['ui_batch'].add(self.maximum_steps * self.circle_segments_per_step + 3,
                                              GL_LINE_STRIP, GROUPS['button_text'],
                                              ('v2i', self.circle_vertices),
                                              ('c4B', self.circle_colors))

    def on_deactivate(self):
        self.is_activated = False

    @abstractmethod
    def on_window_resize(self, width, height):
        pass

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        # self.value_label.on_update_opacity(self.opacity)
        self.circle_colors[3::4] = (self.opacity, ) * (len(self.circle_colors) // 4)
        if self.circle is not None:
            if self.opacity > 0:
                self.circle.colors = self.circle_colors
            else:
                self.circle.delete()
                self.circle = None

    @final
    def on_current_step_update(self, step):
        self.current_step = step
        self.circle_colors = [
            *(*self.main_color, self.opacity) * (self.current_step * self.circle_segments_per_step),
            *(*self.background_color, self.opacity) * ((self.maximum_steps - self.current_step)
                                                       * self.circle_segments_per_step)
        ]
        if self.current_step == 0:
            self.circle_colors = [
                *(*self.background_color, self.opacity) * 2, *self.circle_colors, *self.background_color, self.opacity
            ]
        elif self.current_step == self.maximum_steps:
            self.circle_colors = [
                *(*self.main_color, self.opacity) * 2, *self.circle_colors, *self.main_color, self.opacity
            ]
        else:
            self.circle_colors = [
                *(*self.main_color, self.opacity) * 2, *self.circle_colors, *self.background_color, self.opacity
            ]
