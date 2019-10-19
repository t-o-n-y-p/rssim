from logging import getLogger

from ui.label import InteractiveLabel
from ui import *
from i18n import I18N_RESOURCES


@final
class BonusCodeInteractiveLabel(InteractiveLabel):
    def __init__(self, parent_viewport):
        super().__init__(logger=getLogger('root.bonus_code_interactive_label'), parent_viewport=parent_viewport)
        self.placeholder_text_i18n_resources_key = 'bonus_code_placeholder_string'
        self.font_name = 'Arial'
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    def get_x(self):
        return (self.parent_viewport.x1 + self.parent_viewport.x2) // 2

    def get_y(self):
        return (self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)) // 2 \
               + 5 * get_bottom_bar_height(self.screen_resolution) // 8

    def get_font_size(self):
        return get_top_bar_height(self.screen_resolution)

    def get_width(self):
        return None

    def get_formatted_placeholder_text(self):
        return I18N_RESOURCES[self.placeholder_text_i18n_resources_key][self.current_locale]
