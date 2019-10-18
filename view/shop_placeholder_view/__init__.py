from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.label.shop_locked_label import ShopLockedLabel
from ui.label.shop_level_placeholder_label import ShopLevelPlaceholderLabel


class ShopPlaceholderView(View):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.placeholder.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        USER_DB_CURSOR.execute('''SELECT last_known_shop_window_position FROM graphics''')
        self.last_known_shop_window_position = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        self.lock_label = ShopLockedLabel(parent_viewport=self.viewport)
        self.description_label = ShopLevelPlaceholderLabel(parent_viewport=self.viewport)
        CONFIG_DB_CURSOR.execute('''SELECT level_required FROM shops_config
                                    WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = CONFIG_DB_CURSOR.fetchone()[0]
        self.description_label.on_update_args((self.level_required, ))

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.lock_label.create()
        self.description_label.create()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = get_inner_area_rect(self.screen_resolution)[0]
        self.viewport.y1 = get_inner_area_rect(self.screen_resolution)[1]
        self.viewport.x2 = self.viewport.x1 + get_inner_area_rect(self.screen_resolution)[2]
        self.viewport.y2 = self.viewport.y1 + get_inner_area_rect(self.screen_resolution)[3]
        self.lock_label.on_change_screen_resolution(self.screen_resolution)
        self.description_label.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.lock_label.on_update_opacity(self.opacity)
        self.description_label.on_update_opacity(self.opacity)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.description_label.on_update_current_locale(self.current_locale)
