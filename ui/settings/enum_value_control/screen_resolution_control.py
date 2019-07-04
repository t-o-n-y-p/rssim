from logging import getLogger

from ui.settings.enum_value_control import *
from ui.label.screen_resolution_control_description_label import ScreenResolutionControlDescriptionLabel
from ui.label.temp_screen_resolution_value_label import TempScreenResolutionValueLabel


class ScreenResolutionControl(EnumValueControl):
    def __init__(self, column, row, possible_values_list, on_update_state_action, parent_viewport):
        super().__init__(column, row, possible_values_list, on_update_state_action, parent_viewport,
                         logger=getLogger('root.app.settings.view.enum_value_control.screen_resolution_control'))
        self.description_label = ScreenResolutionControlDescriptionLabel(parent_viewport=self.viewport)
        self.temp_value_label = TempScreenResolutionValueLabel(parent_viewport=self.viewport)
