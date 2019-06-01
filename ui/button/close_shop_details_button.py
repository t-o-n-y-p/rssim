from logging import getLogger

from ui.button import Button


class CloseShopDetailsButton(Button):
    """
    Implements last button in the top right corner on shop details screen.
    For properties definition see base Button class.
    """
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.close_shop_details_button'))
        self.to_activate_on_controller_init = True
        self.text = ''
        self.font_name = 'Webdings'
        self.base_font_size_property = 38 / 80
        self.on_click_action = on_click_action
