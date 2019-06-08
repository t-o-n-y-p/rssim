from logging import getLogger

from model import *


class ShopModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.model'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.user_db_cursor.execute('SELECT level FROM game_progress')
        self.level = self.user_db_cursor.fetchone()[0]
        self.config_db_cursor.execute('''SELECT level_required FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = self.config_db_cursor.fetchone()[0]
        # self.shop_stages_state_matrix = {}
        # self.user_db_cursor.execute('''SELECT stage_number, locked, under_construction, construction_time,
        #                                unlock_condition_from_level, unlock_condition_from_previous_stage,
        #                                unlock_available FROM shop_stages WHERE map_id = ? AND shop_id = ?''',
        #                             (self.map_id, self.shop_id))
        # fetched_data = self.user_db_cursor.fetchall()
        # for stage_info in fetched_data:
        #     self.shop_stages_state_matrix[stage_info[0]] = [bool(stage_info[1]), bool(stage_info[2]), stage_info[3],
        #                                                     bool(stage_info[4]), bool(stage_info[5]), 1,
        #                                                     bool(stage_info[6])]
        #     self.config_db_cursor.execute('''SELECT price, level_required, hourly_profit,
        #                                      storage_capacity, exp_bonus FROM shop_progress_config
        #                                      WHERE map_id = ? AND stage_number = ?''',
        #                                   (self.map_id, stage_info[0]))
        #     stage_progress_config = self.config_db_cursor.fetchone()
        #     self.shop_stages_state_matrix[stage_info[0]].extend([stage_progress_config[0], stage_progress_config[1],
        #                                                          0, *stage_progress_config[2::]])
        #
        # self.user_db_cursor.execute('SELECT money FROM game_progress')
        # self.money = self.user_db_cursor.fetchone()[0]

    def on_activate_view(self):
        self.view.on_activate()

    def on_level_up(self, level):
        self.level = level
