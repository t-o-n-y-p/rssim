from logging import getLogger

from ui.settings.checkbox import *


class Clock24HCheckbox(Checkbox):
    """
    Implements checkbox for 24-hour time format.
    For properties definition see base Checkbox class.
    """
    def __init__(self, column, row, on_update_state_action):
        super().__init__(column, row, on_update_state_action,
                         logger=getLogger(
                             'root.app.settings.view.checkbox.clock_24h_checkbox'))
        self.description_key = 'clock_24h_enabled_description_string'
