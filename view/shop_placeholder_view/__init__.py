from abc import ABC
from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR
from ui.label.shop_locked_label import ShopLockedLabel
from ui.label.shop_level_placeholder_label import ShopLevelPlaceholderLabel
from view import MapBaseView, view_is_not_active


class ShopPlaceholderView(MapBaseView, ABC):
    def __init__(self, controller, map_id, shop_id):
        super().__init__(
            controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.view'),
            child_window=True
        )
        self.shop_id = shop_id
        self.lock_label = ShopLockedLabel(parent_viewport=self.viewport)
        self.description_label = ShopLevelPlaceholderLabel(parent_viewport=self.viewport)
        CONFIG_DB_CURSOR.execute(
            '''SELECT level_required FROM shops_config WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id)
        )
        self.level_required = CONFIG_DB_CURSOR.fetchone()[0]
        self.description_label.on_update_args((self.level_required, ))
        self.on_window_resize_handlers.extend(
            [
                self.lock_label.on_window_resize, self.description_label.on_window_resize
            ]
        )
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.lock_label.create()
        self.description_label.create()

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.description_label.on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.lock_label.on_update_opacity(self.opacity)
        self.description_label.on_update_opacity(self.opacity)
