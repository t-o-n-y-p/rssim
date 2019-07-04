from logging import getLogger

from ui.settings.checkbox import *
from ui.label.fade_animations_enabled_checkbox_description_label import FadeAnimationsEnabledSCheckboxDescriptionLabel


class FadeAnimationsEnabledCheckbox(Checkbox):
    def __init__(self, column, row, on_update_state_action, parent_viewport):
        super().__init__(column, row, on_update_state_action, parent_viewport,
                         logger=getLogger('root.app.settings.view.checkbox.fade_animations_enabled_checkbox'))
        self.description_label = FadeAnimationsEnabledSCheckboxDescriptionLabel(parent_viewport=self.viewport)
