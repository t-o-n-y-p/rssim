from logging import getLogger

from ui.settings.checkbox import *


class EnoughMoneyNotificationCheckbox(Checkbox):
    """
    Implements checkbox for enough money notification state.
    For properties definition see base Checkbox class.
    """
    def __init__(self, column, row, on_update_state_action, current_locale):
        super().__init__(column, row, on_update_state_action, current_locale,
                         logger=getLogger(
                             'root.app.settings.view.checkbox.enough_money_notification_checkbox'))
        self.description_key = 'enough_money_notification_description_string'
