from logging import getLogger

from ui.settings.checkbox import *
from ui.label.fade_animations_enabled_checkbox_description_label import FadeAnimationsEnabledCheckboxDescriptionLabel


@final
class FadeAnimationsEnabledCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(
            column, row, on_update_state_action, parent_viewport,
            logger=getLogger('root.app.settings.view.checkbox.fade_animations_enabled_checkbox')
        )
        self.description_label = FadeAnimationsEnabledCheckboxDescriptionLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.description_label.on_window_resize)
