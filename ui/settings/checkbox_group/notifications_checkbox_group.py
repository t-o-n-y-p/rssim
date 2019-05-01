from logging import getLogger

from ui.settings.checkbox_group import *
from ui.settings.checkbox.level_up_notification_checkbox import LevelUpNotificationCheckbox
from ui.settings.checkbox.feature_unlocked_notification_checkbox import FeatureUnlockedNotificationCheckbox
from ui.settings.checkbox.construction_completed_notification_checkbox import ConstructionCompletedNotificationCheckbox
from ui.settings.checkbox.enough_money_notification_checkbox import EnoughMoneyNotificationCheckbox


class NotificationsCheckboxGroup(CheckboxGroup):
    """
    Implements checkbox group for notifications state.
    For properties definition see base CheckboxGroup class.
    """
    def __init__(self, column, row, on_update_state_actions):
        super().__init__(column, row,
                         logger=getLogger('root.app.settings.view.checkbox_group.notifications_checkbox_group'))
        self.description_key = 'notification_description_string'
        self.checkboxes \
            = [LevelUpNotificationCheckbox(column, row - 2, on_update_state_actions[0]),
               FeatureUnlockedNotificationCheckbox(column, row - 4, on_update_state_actions[1]),
               ConstructionCompletedNotificationCheckbox(column, row - 6, on_update_state_actions[2]),
               EnoughMoneyNotificationCheckbox(column, row - 8, on_update_state_actions[3])]

        for checkbox in self.checkboxes:
            self.buttons.extend(checkbox.buttons)
