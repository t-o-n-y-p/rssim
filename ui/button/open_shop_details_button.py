from logging import getLogger

from ui.button import Button


class OpenShopDetailsButton(Button):
    """
    Implements Open shop details button.
    For properties definition see base Button class.
    """
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.open_shop_details_button'))
        self.to_activate_on_controller_init = True
        self.invisible = True
        self.text = ' '
        self.font_name = 'Arial'
        self.base_font_size_property = 29 / 80
        self.on_click_action = on_click_action
