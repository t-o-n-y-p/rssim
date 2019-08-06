from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.button.close_shop_details_button import CloseShopDetailsButton
from ui.label.shop_title_label import ShopTitleLabel
from ui.shader_sprite.shop_view_shader_sprite import ShopViewShaderSprite


class ShopView(View):
    def __init__(self, map_id, shop_id):
        def on_close_shop_details(button):
            self.controller.parent_controller.on_close_shop_details(self.shop_id)

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        USER_DB_CURSOR.execute('''SELECT last_known_shop_window_position FROM graphics''')
        self.last_known_shop_window_position = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        self.shader_sprite = ShopViewShaderSprite(view=self)
        self.title_label = ShopTitleLabel(parent_viewport=self.viewport)
        self.title_label.on_update_args((self.shop_id + 1, ))
        self.close_shop_details_button = CloseShopDetailsButton(on_click_action=on_close_shop_details,
                                                                parent_viewport=self.viewport)
        self.buttons = [self.close_shop_details_button, ]

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
        self.is_activated = True
        self.shader_sprite.create()
        self.title_label.create()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = get_inner_area_rect(self.screen_resolution)[0]
        self.viewport.y1 = get_inner_area_rect(self.screen_resolution)[1]
        self.viewport.x2 = self.viewport.x1 + get_inner_area_rect(self.screen_resolution)[2]
        self.viewport.y2 = self.viewport.y1 + get_inner_area_rect(self.screen_resolution)[3]
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.title_label.on_update_current_locale(self.current_locale)
