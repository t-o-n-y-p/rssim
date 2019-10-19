from logging import getLogger

from ui.settings.checkbox import *
from ui.label.shop_storage_notification_checkbox_description_label \
    import ShopStorageNotificationCheckboxDescriptionLabel


@final
class ShopStorageNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(column, row, on_update_state_action, parent_viewport,
                         logger=getLogger('root.app.settings.view.checkbox.shop_storage_notification_checkbox'))
        self.description_label = ShopStorageNotificationCheckboxDescriptionLabel(parent_viewport=self.viewport)
