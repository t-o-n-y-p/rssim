from logging import getLogger

from view import *
from ui.button.close_shop_details_button import CloseShopDetailsButton
from ui.label.shop_title_label import ShopTitleLabel
from ui.shader_sprite.shop_view_shader_sprite import ShopViewShaderSprite


class ShopView(GameBaseView):
    def __init__(self, map_id, shop_id):
        def on_close_shop_details(button):
            self.controller.parent_controller.on_close_shop_details(self.shop_id)

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'), child_window=True)
        self.map_id = map_id
        self.shop_id = shop_id
        self.shader_sprite = ShopViewShaderSprite(view=self)
        self.title_label = ShopTitleLabel(parent_viewport=self.viewport)
        self.title_label.on_update_args((self.shop_id + 1, ))
        self.close_shop_details_button = CloseShopDetailsButton(on_click_action=on_close_shop_details,
                                                                parent_viewport=self.viewport)
        self.buttons = [self.close_shop_details_button, ]

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.title_label.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.title_label.on_update_current_locale(self.current_locale)
