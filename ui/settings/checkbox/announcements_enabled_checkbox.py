from logging import getLogger
from typing import final

from ui.label.announcements_enabled_checkbox_description_label import AnnouncementsEnabledCheckboxDescriptionLabel
from ui.settings.checkbox import Checkbox


@final
class AnnouncementsEnabledCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(
            column, row, on_update_state_action, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox.announcements_enabled_checkbox')
        )
        self.description_label = AnnouncementsEnabledCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
