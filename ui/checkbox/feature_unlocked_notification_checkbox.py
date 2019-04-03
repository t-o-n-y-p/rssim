from logging import getLogger

from ui.checkbox import *


class FeatureUnlockedNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, surface, batches, groups, current_locale):
        super().__init__(column, row, on_update_state_action, surface, batches, groups, current_locale,
                         logger=getLogger('root.app.settings.view.checkbox.feature_unlocked_notification_checkbox'))
        self.description_key = 'feature_unlocked_notification_description_string'
