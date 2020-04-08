from logging import getLogger
from typing import final

from ui.label.shop_storage_notification_checkbox_description_label \
    import ShopStorageNotificationCheckboxDescriptionLabel
from ui.settings.checkbox import Checkbox


@final
class ShopStorageNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(
            column, row, on_update_state_action, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox.shop_storage_notification_checkbox')
        )
        self.description_label = ShopStorageNotificationCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
