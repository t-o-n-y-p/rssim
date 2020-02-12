from logging import getLogger

from ui.settings.checkbox import *
from ui.label.level_up_notification_checkbox_description_label import LevelUpNotificationCheckboxDescriptionLabel


@final
class LevelUpNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(column, row, on_update_state_action, parent_viewport,
                         logger=getLogger('root.app.settings.view.checkbox.level_up_notification_checkbox'))
        self.description_label = LevelUpNotificationCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_resize_handlers.append(self.description_label.on_resize)
