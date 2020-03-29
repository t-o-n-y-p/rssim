from logging import getLogger

from ui.knob.master_volume_knob import MasterVolumeKnob
from ui.label.master_volume_description_label import MasterVolumeDescriptionLabel
from ui.settings.knob import SettingsKnob


class MasterVolumeSettingsKnob(SettingsKnob):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(column, row, on_update_state_action, parent_viewport,
                         logger=getLogger('root.app.settings.view.settings_knob.master_volume_settings_knob'))
        self.description_label = MasterVolumeDescriptionLabel(parent_viewport=self.viewport)
        self.knob = MasterVolumeKnob(on_value_update_action=on_update_state_action, parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend(
            [self.description_label.on_window_resize, *self.knob.on_window_resize_handlers]
        )
        self.on_mouse_motion_handlers.append(self.knob.on_mouse_motion)
        self.on_mouse_press_handlers.append(self.knob.on_mouse_press)
        self.on_mouse_release_handlers.append(self.knob.on_mouse_release)
        self.on_mouse_drag_handlers.append(self.knob.on_mouse_drag)
