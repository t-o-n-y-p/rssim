from logging import getLogger

from ui.settings.checkbox_group import *
from ui.settings.checkbox.level_up_notification_checkbox import LevelUpNotificationCheckbox
from ui.settings.checkbox.feature_unlocked_notification_checkbox import FeatureUnlockedNotificationCheckbox
from ui.settings.checkbox.construction_completed_notification_checkbox import ConstructionCompletedNotificationCheckbox
from ui.settings.checkbox.enough_money_notification_checkbox import EnoughMoneyNotificationCheckbox


class NotificationsCheckboxGroup(CheckboxGroup):
    def __init__(self, column, row, surface, batches, groups, current_locale, on_update_state_actions):
        super().__init__(column, row, surface, batches, groups, current_locale,
                         logger=getLogger('root.app.settings.view.checkbox_group.notifications_checkbox_group'))
        self.description_key = 'notification_description_string'
        self.checkboxes \
            = [LevelUpNotificationCheckbox(column, row - 2, on_update_state_actions[0],
                                           surface, batches, groups, current_locale),
               FeatureUnlockedNotificationCheckbox(column, row - 4, on_update_state_actions[1],
                                                   surface, batches, groups, current_locale),
               ConstructionCompletedNotificationCheckbox(column, row - 6, on_update_state_actions[2],
                                                         surface, batches, groups, current_locale),
               EnoughMoneyNotificationCheckbox(column, row - 8, on_update_state_actions[3],
                                               surface, batches, groups, current_locale)]

        for checkbox in self.checkboxes:
            self.buttons.extend(checkbox.buttons)
