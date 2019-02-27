from logging import getLogger

from button import Button


class BuyTrackButton(Button):
    """
    Implements Buy track button on constructor screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.buy_track_button'))
        self.to_activate_on_controller_init = False
        self.text = ''
        self.font_name = 'Webdings'
        self.font_size = 40
        self.x_margin = 0
        self.y_margin = 0
        self.button_size = (80, 80)
        self.on_click_action = on_click_action
