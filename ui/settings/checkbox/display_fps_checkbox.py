from logging import getLogger

from ui.settings.checkbox import *
from ui.label.display_fps_checkbox_description_label import DisplayFPSCheckboxDescriptionLabel


class DisplayFPSCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(column, row, on_update_state_action, parent_viewport,
                         logger=getLogger('root.app.settings.view.checkbox.display_fps_checkbox'))
        self.description_label = DisplayFPSCheckboxDescriptionLabel(parent_viewport=self.viewport)
