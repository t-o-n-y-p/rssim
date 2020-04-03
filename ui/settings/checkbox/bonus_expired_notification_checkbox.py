from logging import getLogger

from ui.settings.checkbox import *
from ui.label.bonus_expired_notification_checkbox_description_label \
    import BonusExpiredNotificationCheckboxDescriptionLabel


@final
class BonusExpiredNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(
            column, row, on_update_state_action, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox.bonus_expired_notification_checkbox')
        )
        self.description_label = BonusExpiredNotificationCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
