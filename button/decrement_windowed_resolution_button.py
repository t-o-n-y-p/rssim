from logging import getLogger

from button import Button


class DecrementWindowedResolutionButton(Button):
    """
    Implements "-" button for windowed resolution on settings screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.decrement_windowed_resolution_button'))
        self.to_activate_on_controller_init = False
        self.text = '–'
        self.font_name = 'Arial'
        self.font_size = 16
        self.x_margin = 100
        self.y_margin = 520
        self.button_size = (40, 40)
        self.on_click_action = on_click_action
