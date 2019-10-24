from logging import getLogger

from view import *
from ui.label.shop_locked_label import ShopLockedLabel
from ui.label.shop_level_placeholder_label import ShopLevelPlaceholderLabel


class ShopPlaceholderView(GameBaseView):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.view'),
                         child_window=True)
        self.map_id = map_id
        self.shop_id = shop_id
        self.lock_label = ShopLockedLabel(parent_viewport=self.viewport)
        self.description_label = ShopLevelPlaceholderLabel(parent_viewport=self.viewport)
        CONFIG_DB_CURSOR.execute('''SELECT level_required FROM shops_config
                                    WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = CONFIG_DB_CURSOR.fetchone()[0]
        self.description_label.on_update_args((self.level_required, ))

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.lock_label.create()
        self.description_label.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.description_label.on_update_current_locale(self.current_locale)

    @final
    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.lock_label.on_change_screen_resolution(self.screen_resolution)
        self.description_label.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.lock_label.on_update_opacity(self.opacity)
        self.description_label.on_update_opacity(self.opacity)
