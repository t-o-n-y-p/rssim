from logging import getLogger
from typing import final

from ui.label.clock_24h_checkbox_description_label import Clock24HCheckboxDescriptionLabel
from ui.settings.checkbox import Checkbox


@final
class Clock24HCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(
            column, row, on_update_state_action, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox.clock_24h_checkbox')
        )
        self.description_label = Clock24HCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
