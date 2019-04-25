from logging import getLogger

from ui.settings.checkbox import *


class FadeAnimationsEnabledCheckbox(Checkbox):
    """
    Implements checkbox for fade animations state.
    For properties definition see base Checkbox class.
    """
    def __init__(self, column, row, current_locale, on_update_state_action):
        super().__init__(column, row, on_update_state_action, current_locale,
                         logger=getLogger('root.app.settings.view.checkbox.fade_animations_enabled_checkbox'))
        self.description_key = 'fade_animations_enabled_description_string'
