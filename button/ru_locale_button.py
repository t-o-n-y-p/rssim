from logging import getLogger

from button import Button


class RULocaleButton(Button):
    """
    Implements RU locale button in the top bar.
    For properties definition see base Button class.
    """
    def __init__(self, surface, batch, groups, on_click_action):
        super().__init__(surface, batch, groups, logger=getLogger('root.button.ru_locale_button'))
        self.to_activate_on_controller_init = True
        self.text = ' '
        self.font_name = 'Arial'
        self.font_size = 48
        self.x_margin = 34
        self.y_margin = 684
        self.button_size = (36, 36)
        self.on_click_action = on_click_action
