from logging import getLogger

from button import Button


class CloseScheduleButton(Button):
    """
    Implements Close schedule button on main game screen.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.close_schedule_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 24 / 80
        self.on_click_action = on_click_action
