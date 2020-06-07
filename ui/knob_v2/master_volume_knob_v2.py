from typing import final

from ui import RED_RGB, RED_GREY_RGB, window_size_has_changed, get_bottom_bar_height, default_object
from ui.knob_v2 import KnobV2, value_update_mode_enabled, next_knob_step_detected
from ui.label_v2.master_volume_value_label_v2 import MasterVolumeValueLabelV2


@final
class MasterVolumeKnobV2(KnobV2):
    @default_object(MasterVolumeValueLabelV2)
    def __init__(self, logger, parent_viewport, on_value_update_action):
        super().__init__(logger, parent_viewport, on_value_update_action)
        self.main_color = RED_RGB
        self.background_color = RED_GREY_RGB
        self.start_value = 0
        self.maximum_steps = 20
        self.value_step = 100 // self.maximum_steps
        self.on_init_state(self.start_value)

    def current_value_formula(self):
        return self.start_value + self.value_step * self.current_step

    def on_init_state(self, value):
        self.master_volume_value_label_v2.on_master_volume_update(value)                                        # noqa
        self.on_current_step_update(value // self.value_step)

    @value_update_mode_enabled
    @next_knob_step_detected
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        super().on_mouse_drag(x, y, dx, dy, buttons, modifiers)
        self.master_volume_value_label_v2.on_master_volume_update(self.current_value_formula())                 # noqa

    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport.x1 = self.parent_viewport.x2 - get_bottom_bar_height(self.screen_resolution)
        self.viewport.x2 = self.parent_viewport.x2
        self.viewport.y1 = self.parent_viewport.y1
        self.viewport.y2 = self.parent_viewport.y2
        self.on_circle_resize()
