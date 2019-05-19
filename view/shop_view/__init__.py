from logging import getLogger

from view import *


class ShopView(View):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.shop_details_window_position = (0, 0)
        self.shop_details_window_size = (0, 0)
        self.config_db_cursor.execute('''SELECT level_required, price, initial_construction_time, hourly_profit, 
                                         storage_capacity, exp_bonus FROM shop_progress_config WHERE map_id = ?''',
                                      (self.map_id, ))
        self.shop_config = self.config_db_cursor.fetchall()
        self.config_db_cursor.execute('''SELECT first_available_shop_stage FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        first_available_shop_stage = self.config_db_cursor.fetchone()[0]
        self.shop_stage_cells = {}
        for i in range(first_available_shop_stage, 5):
            self.shop_stage_cells[i] = ShopStageCell(stage=i, number_of_stages=5-first_available_shop_stage)

        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.shop_details_window_size = (int(6.875 * bottom_bar_height) * 2 + bottom_bar_height // 4,
                                         19 * bottom_bar_height // 4)
        self.shop_details_window_position = ((self.screen_resolution[0] - self.shop_details_window_size[0]) // 2,
                                             (self.screen_resolution[1] - self.shop_details_window_size[1]
                                              - 3 * bottom_bar_height // 2) // 2 + bottom_bar_height)
