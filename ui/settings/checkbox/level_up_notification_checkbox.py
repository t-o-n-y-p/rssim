from logging import getLogger

from ui.settings.checkbox import *


class LevelUpNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, surface, batches, groups, current_locale):
        super().__init__(column, row, on_update_state_action, surface, batches, groups, current_locale,
                         logger=getLogger('root.app.settings.view.checkbox.level_up_notification_checkbox'))
        self.description_key = 'level_up_notification_description_string'
