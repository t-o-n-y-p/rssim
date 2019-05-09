from logging import getLogger

from ui.button import Button


class CreateStationButton(Button):
    def __init__(self, on_click_action):
        """
        Implements Create station button on the main menu screen.
        For properties definition see base Button class.
        """
        super().__init__(logger=getLogger('root.button.create_station_button'))
        self.transparent = True
        self.to_activate_on_controller_init = False
        self.text = ' '
        self.font_name = 'Perfo'
        self.is_bold = True
        self.base_font_size_property = 30 / 80
        self.on_click_action = on_click_action
