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
        self.base_font_size_property = 32 / 80
        self.on_click_action = on_click_action
