from logging import getLogger

from ui.settings.checkbox_group import *
from ui.settings.checkbox.level_up_notification_checkbox import LevelUpNotificationCheckbox
from ui.settings.checkbox.feature_unlocked_notification_checkbox import FeatureUnlockedNotificationCheckbox
from ui.settings.checkbox.construction_completed_notification_checkbox import ConstructionCompletedNotificationCheckbox
from ui.settings.checkbox.enough_money_notification_checkbox import EnoughMoneyNotificationCheckbox
from ui.settings.checkbox.bonus_expired_notification_checkbox import BonusExpiredNotificationCheckbox
from ui.settings.checkbox.shop_storage_notification_checkbox import ShopStorageNotificationCheckbox
from ui.label.notifications_checkbox_group_description_label import NotificationsCheckboxGroupDescriptionLabel


class NotificationsCheckboxGroup(CheckboxGroup):
    def __init__(self, column, row, on_update_state_actions, parent_viewport):
        super().__init__(column, row, parent_viewport,
                         logger=getLogger('root.app.settings.view.checkbox_group.notifications_checkbox_group'))
        self.description_label = NotificationsCheckboxGroupDescriptionLabel(parent_viewport=self.viewport)
        # passing parent viewport here, skipping self viewport because self viewport is calculated for description only
        # and checkbox viewports are calculated based on parent viewport
        self.checkboxes \
            = [LevelUpNotificationCheckbox(column, row - 2, on_update_state_actions[0], parent_viewport),
               FeatureUnlockedNotificationCheckbox(column, row - 4, on_update_state_actions[1], parent_viewport),
               ConstructionCompletedNotificationCheckbox(column, row - 6, on_update_state_actions[2], parent_viewport),
               EnoughMoneyNotificationCheckbox(column, row - 8, on_update_state_actions[3], parent_viewport),
               BonusExpiredNotificationCheckbox(column, row - 10, on_update_state_actions[4], parent_viewport),
               ShopStorageNotificationCheckbox(column, row - 12, on_update_state_actions[5], parent_viewport)]

        for checkbox in self.checkboxes:
            self.buttons.extend(checkbox.buttons)
