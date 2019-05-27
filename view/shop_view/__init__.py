from logging import getLogger

from pyglet.image import load

from view import *


class ShopView(View):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.shop_details_window_position = (0, 0)
        self.shop_details_window_size = (0, 0)
        self.shop_icon_size = (0, 0)
        self.shop_icon_position = (0, 0)
        self.config_db_cursor.execute('''SELECT level_required, price, initial_construction_time, hourly_profit, 
                                         storage_capacity, exp_bonus FROM shop_progress_config WHERE map_id = ?''',
                                      (self.map_id, ))
        self.shop_config = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT first_available_shop_stage FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        first_available_shop_stage = self.config_db_cursor.fetchone()[0]
        self.storage_progress_inactive_image = load('img/game_progress_bars/shop_storage_inactive.png')
        self.storage_progress_active_image = load('img/game_progress_bars/shop_storage_active.png')
        self.shop_stage_cells = {}
        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.shop_details_window_size = (int(6.875 * self.bottom_bar_height) * 2 + self.bottom_bar_height // 4,
                                         19 * self.bottom_bar_height // 4)
        self.shop_details_window_position = ((self.screen_resolution[0] - self.shop_details_window_size[0]) // 2,
                                             (self.screen_resolution[1] - self.shop_details_window_size[1]
                                              - 3 * self.bottom_bar_height // 2) // 2 + self.bottom_bar_height)
        self.shop_icon_size = (int(6.25 * self.bottom_bar_height), self.bottom_bar_height * 2)
        self.shop_icon_position = (self.shop_details_window_position[0]
                                   + (self.shop_details_window_size[0] - self.shop_icon_size[0]) // 2,
                                   self.shop_details_window_position[1]
                                   + (self.shop_details_window_size[1] - self.top_bar_height - self.bottom_bar_height
                                      - self.shop_icon_size[1]) // 2)
