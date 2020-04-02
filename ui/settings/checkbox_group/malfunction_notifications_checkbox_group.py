from logging import getLogger

from ui.label.malfunction_notifications_checkbox_group_description_label import \
    MalfunctionNotificationsCheckboxGroupDescriptionLabel
from ui.settings.checkbox.voice_not_found_notification_checkbox import VoiceNotFoundNotificationCheckbox
from ui.settings.checkbox_group import *


@final
class MalfunctionNotificationsCheckboxGroup(CheckboxGroup):
    def __init__(self, column, row, on_update_state_actions, parent_viewport):
        super().__init__(
            column, row, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox_group.malfunction_notifications_checkbox_group')
        )
        self.description_label = MalfunctionNotificationsCheckboxGroupDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
        # passing parent viewport here, skipping self viewport because self viewport is calculated for description only
        # and checkbox viewports are calculated based on parent viewport
        self.checkboxes = [
            VoiceNotFoundNotificationCheckbox(column, row - 2, on_update_state_actions[0], parent_viewport)
        ]

        for checkbox in self.checkboxes:
            self.buttons.extend(checkbox.buttons)
            self.on_window_resize_handlers.extend(checkbox.on_window_resize_handlers)
