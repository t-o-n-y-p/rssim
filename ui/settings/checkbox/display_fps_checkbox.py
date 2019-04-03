from logging import getLogger

from ui.settings.checkbox import *


class DisplayFPSCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, surface, batches, groups, current_locale):
        super().__init__(column, row, on_update_state_action, surface, batches, groups, current_locale,
                         logger=getLogger('root.app.settings.view.checkbox.display_fps_checkbox'))
        self.description_key = 'display_fps_description_string'
