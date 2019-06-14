from logging import getLogger

from ui.button import Button


class ClearShopStorageButton(Button):
    def __init__(self, on_click_action):
        super().__init__(logger=getLogger('root.button.clear_shop_storage_button'))
        self.to_activate_on_controller_init = True
        self.text = 'Ò'
        self.font_name = 'Webdings'
        self.base_font_size_property = 38 / 80
        self.on_click_action = on_click_action
