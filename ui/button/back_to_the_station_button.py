from logging import getLogger

from ui.button import Button
from i18n import I18N_RESOURCES


class BackToTheStationButton(Button):
    def __init__(self, on_click_action):
        """
        Implements Back to the station button on the main menu screen.
        For properties definition see base Button class.
        """
        super().__init__(logger=getLogger('root.button.back_to_the_station_button'))
        self.transparent = True
        self.to_activate_on_controller_init = False
        self.text = I18N_RESOURCES['back_to_the_station_label_string'][self.current_locale]
        self.font_name = 'Perfo'
        self.is_bold = True
        self.base_font_size_property = 30 / 80
        self.on_click_action = on_click_action

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.text = I18N_RESOURCES['back_to_the_station_label_string'][self.current_locale]
        if self.text_label is not None:
            self.text_label.text = I18N_RESOURCES['back_to_the_station_label_string'][self.current_locale]
