from logging import getLogger

from ui.button import Button


class CreateStationButton(Button):
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.create_station_button'))
        self.transparent = True
        self.to_activate_on_controller_init = True
        self.text = ' '
        self.font_name = 'Perfo'
        self.is_bold = True
        self.base_font_size_property = 30 / 80
        self.on_click_action = on_click_action
