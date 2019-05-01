from logging import getLogger

from ui.settings.checkbox import *


class DisplayFPSCheckbox(Checkbox):
    """
    Implements checkbox for FPS state.
    For properties definition see base Checkbox class.
    """
    def __init__(self, column, row, on_update_state_action):
        super().__init__(column, row, on_update_state_action,
                         logger=getLogger('root.app.settings.view.checkbox.display_fps_checkbox'))
        self.description_key = 'display_fps_description_string'
