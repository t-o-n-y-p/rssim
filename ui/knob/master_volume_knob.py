from logging import getLogger

from ui import *
from ui.knob import Knob
from ui.label.master_volume_value_label import MasterVolumeValueLabel


@final
class MasterVolumeKnob(Knob):
    def __init__(self, on_value_update_action, parent_viewport):
        super().__init__(on_value_update_action=on_value_update_action, parent_viewport=parent_viewport,
                         logger=getLogger('root.app.game.view.master_volume_knob'))
        self.main_color = RED_RGB
        self.background_color = RED_GREY_RGB
        self.value_label = MasterVolumeValueLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.value_label.on_window_resize)
        self.start_value = 0
        self.maximum_steps = 25
        self.value_step = 100 // self.maximum_steps
        self.on_init_state(self.start_value)

    def current_value_formula(self):
        return self.start_value + self.value_step * self.current_step

    def on_init_state(self, value):
        self.value_label.on_update_args((value, ))
        self.on_current_step_update(value // self.value_step)

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 = self.parent_viewport.x2 - get_bottom_bar_height(self.screen_resolution)
        self.viewport.x2 = self.parent_viewport.x2
        self.viewport.y1 = self.parent_viewport.y1
        self.viewport.y2 = self.parent_viewport.y2
        self.on_circle_resize()
