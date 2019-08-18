from logging import getLogger

from ui import *
from ui.button import UIButton
from i18n import I18N_RESOURCES


class OpenSettingsMainMenuViewButton(UIButton):
    def __init__(self, on_click_action, parent_viewport):
        super().__init__(logger=getLogger('root.open_settings_main_menu_view_button'),
                         parent_viewport=parent_viewport)
        self.transparent = True
        self.to_activate_on_controller_init = True
        self.text = I18N_RESOURCES['settings_label_string'][self.current_locale]
        self.font_name = 'Perfo'
        self.is_bold = True
        self.base_font_size_property = 30 / 80
        self.on_click_action = on_click_action

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.text = I18N_RESOURCES['settings_label_string'][self.current_locale]
        if self.text_label is not None:
            self.text_label.text = I18N_RESOURCES['settings_label_string'][self.current_locale]

    def get_position(self):
        return ((self.parent_viewport.x1 + self.parent_viewport.x2) // 2
                - 7 * get_bottom_bar_height(self.screen_resolution) // 2,
                (self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                 + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)) // 2
                - get_bottom_bar_height(self.screen_resolution) // 2)

    def get_size(self):
        return (get_bottom_bar_height(self.screen_resolution) * 7,
                get_bottom_bar_height(self.screen_resolution))