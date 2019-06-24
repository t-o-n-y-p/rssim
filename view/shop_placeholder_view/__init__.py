from logging import getLogger

from view import *
from ui.label.shop_locked_label import ShopLockedLabel
from ui.label.shop_level_placeholder_label import ShopLevelPlaceholderLabel


class ShopPlaceholderView(View):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.user_db_cursor.execute('''SELECT last_known_shop_window_position FROM graphics''')
        self.viewport.x1, self.viewport.y1 = tuple(map(int, self.user_db_cursor.fetchone()[0].split(',')))
        self.viewport.x2 = self.viewport.x1 + self.inner_area_size[0]
        self.viewport.y2 = self.viewport.y1 + self.inner_area_size[1]
        self.lock_label = ShopLockedLabel(parent_viewport=self.viewport)
        self.description_label = ShopLevelPlaceholderLabel(parent_viewport=self.viewport)
        self.config_db_cursor.execute('''SELECT level_required FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = self.config_db_cursor.fetchone()[0]
        self.description_label.on_update_args((self.level_required, ))
        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.lock_label.create()
        self.description_label.create()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.viewport.x1 = self.inner_area_position[0]
        self.viewport.y1 = self.inner_area_position[1]
        self.viewport.x2 = self.viewport.x1 + self.inner_area_size[0]
        self.viewport.y2 = self.viewport.y1 + self.inner_area_size[1]
        self.lock_label.on_change_screen_resolution(self.screen_resolution)
        self.description_label.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.lock_label.delete()
            self.description_label.delete()
        else:
            self.lock_label.on_update_opacity(self.opacity)
            self.description_label.on_update_opacity(self.opacity)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.description_label.on_update_current_locale(self.current_locale)
