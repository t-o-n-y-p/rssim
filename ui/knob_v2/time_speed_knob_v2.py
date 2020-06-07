from math import log
from typing import final

from ui import YELLOW_RGB, YELLOW_GREY_RGB, window_size_has_changed, get_bottom_bar_height, localizable, default_object
from ui.knob_v2 import KnobV2, value_update_mode_enabled, next_knob_step_detected
from ui.label_v2.time_speed_value_label_v2 import TimeSpeedValueLabelV2


@final
class TimeSpeedKnobV2(KnobV2):
    @localizable
    @default_object(TimeSpeedValueLabelV2)
    def __init__(self, logger, parent_viewport, on_value_update_action):
        super().__init__(logger, parent_viewport, on_value_update_action)
        self.main_color = YELLOW_RGB
        self.background_color = YELLOW_GREY_RGB
        self.start_value = 1.0
        self.maximum_steps = 24
        self.value_step = pow(16.0, 1 / self.maximum_steps)
        self.on_init_state(self.start_value)

    def current_value_formula(self):
        return self.start_value * pow(self.value_step, self.current_step)

    def on_init_state(self, value):
        self.time_speed_value_label_v2.on_multiplier_update(value)                                              # noqa
        self.on_current_step_update(round(log(value, self.value_step)))

    @value_update_mode_enabled
    @next_knob_step_detected
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self.time_speed_value_label_v2.on_multiplier_update(self.current_value_formula())                       # noqa

    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport.x1 = self.parent_viewport.x2 - 2 * get_bottom_bar_height(self.screen_resolution)
        self.viewport.x2 = self.parent_viewport.x2 - get_bottom_bar_height(self.screen_resolution)
        self.viewport.y1 = self.parent_viewport.y1
        self.viewport.y2 = self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
        self.on_circle_resize()
