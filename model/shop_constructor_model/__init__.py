from logging import getLogger

from model import *


class ShopConstructorModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.model'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.shop_stages_state_matrix = {}
        self.user_db_cursor.execute('''SELECT stage_number, locked, under_construction, construction_time,
                                       unlock_condition_from_level, unlock_condition_from_previous_stage,
                                       unlock_available FROM shop_stages WHERE map_id = ? AND shop_id = ?''',
                                    (self.map_id, self.shop_id))
        fetched_data = self.user_db_cursor.fetchall()
        for stage_info in fetched_data:
            self.shop_stages_state_matrix[stage_info[0]] = [bool(stage_info[1]), bool(stage_info[2]), stage_info[3],
                                                            bool(stage_info[4]), bool(stage_info[5]), 1,
                                                            bool(stage_info[6])]
            self.config_db_cursor.execute('''SELECT price, level_required, hourly_profit,
                                             storage_capacity, exp_bonus FROM shop_progress_config
                                             WHERE map_id = ? AND stage_number = ?''',
                                          (self.map_id, stage_info[0]))
            stage_progress_config = self.config_db_cursor.fetchone()
            self.shop_stages_state_matrix[stage_info[0]].extend([stage_progress_config[0], stage_progress_config[1],
                                                                 0, *stage_progress_config[2::]])

        self.user_db_cursor.execute('SELECT money FROM game_progress')
        self.money = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('''SELECT current_stage, shop_storage_money, internal_shop_time
                                       FROM shops WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.current_stage, self.shop_storage_money, self.internal_shop_time = self.user_db_cursor.fetchone()

    def on_activate_view(self):
        self.view.current_stage = self.current_stage
        self.view.on_activate()
        for stage_number in range(1, 5):
            self.view.on_update_stage_state(self.shop_stages_state_matrix, stage_number)

        self.view.on_update_storage_money(self.shop_storage_money)
        self.view.on_update_money(self.money)

    def on_save_state(self):
        self.user_db_cursor.execute('''UPDATE shops SET current_stage = ?, shop_storage_money = ?, 
                                       internal_shop_time = ? WHERE map_id = ? AND shop_id = ?''',
                                    (self.current_stage, self.shop_storage_money, self.internal_shop_time,
                                     self.map_id, self.shop_id))
        for stage_number in self.shop_stages_state_matrix:
            self.user_db_cursor.execute('''UPDATE shop_stages SET locked = ?, under_construction = ?, 
                                           construction_time = ?, unlock_condition_from_level = ?, 
                                           unlock_condition_from_previous_stage = ?, unlock_available = ?
                                           WHERE map_id = ? AND shop_id = ?''',
                                        tuple(map(int, (
                                            self.shop_stages_state_matrix[stage_number][LOCKED],
                                            self.shop_stages_state_matrix[stage_number][UNDER_CONSTRUCTION],
                                            self.shop_stages_state_matrix[stage_number][CONSTRUCTION_TIME],
                                            self.shop_stages_state_matrix[stage_number][UNLOCK_CONDITION_FROM_LEVEL],
                                            self.shop_stages_state_matrix[stage_number][
                                                                            UNLOCK_CONDITION_FROM_PREVIOUS_STAGE],
                                            self.shop_stages_state_matrix[stage_number][UNLOCK_AVAILABLE],
                                            self.map_id, self.shop_id
                                        ))))
