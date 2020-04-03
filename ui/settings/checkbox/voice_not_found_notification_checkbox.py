from logging import getLogger

from ui.label.voice_not_found_notification_ckeckbox_description_label import \
    VoiceNotFoundNotificationCheckboxDescriptionLabel
from ui.settings.checkbox import *


@final
class VoiceNotFoundNotificationCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(
            column, row, on_update_state_action, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox.voice_not_found_notification_checkbox')
        )
        self.description_label = VoiceNotFoundNotificationCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
