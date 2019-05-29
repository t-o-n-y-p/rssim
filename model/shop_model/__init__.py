from logging import getLogger

from model import *


class ShopModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.model'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.user_db_cursor.execute('''SELECT locked, current_stage, money, internal_shop_time FROM shops 
                                       WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.locked, self.current_stage, self.money, self.internal_shop_time = self.user_db_cursor.fetchone()
        self.locked = bool(self.locked)
        self.config_db_cursor.execute('''SELECT track_required, first_available_shop_stage FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.track_required, self.first_available_shop_stage = self.config_db_cursor.fetchone()
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

    def on_save_state(self):
        self.user_db_cursor.execute('''UPDATE shops SET locked = ?, current_stage = ?, money = ?, internal_shop_time = ?
                                       WHERE map_id = ? AND shop_id = ?''',
                                    (int(self.locked), self.current_stage, self.money, self.internal_shop_time,
                                     self.map_id, self.shop_id))
        for stage in self.shop_stages_state_matrix:
            self.user_db_cursor.execute('''UPDATE shop_stages SET locked = ?, under_construction = ?, 
                                           construction_time = ?, unlock_condition_from_level = ?, 
                                           unlock_condition_from_previous_stage = ?, unlock_available = ? 
                                           WHERE map_id = ? AND shop_id = ? AND stage_number = ?''',
                                        tuple(
                                            map(int,
                                                (self.shop_stages_state_matrix[stage][LOCKED],
                                                 self.shop_stages_state_matrix[stage][UNDER_CONSTRUCTION],
                                                 self.shop_stages_state_matrix[stage][CONSTRUCTION_TIME],
                                                 self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL],
                                                 self.shop_stages_state_matrix[stage][
                                                     UNLOCK_CONDITION_FROM_PREVIOUS_STAGE],
                                                 self.shop_stages_state_matrix[stage][UNLOCK_AVAILABLE],
                                                 self.map_id, self.shop_id, stage)
                                                )
                                            )
                                        )

    def on_activate_view(self):
        self.view.on_activate()

    def on_unlock(self):
        self.locked = False

    def on_put_under_construction(self, stage_number):
        self.shop_stages_state_matrix[stage_number][UNLOCK_AVAILABLE] = False
        self.shop_stages_state_matrix[stage_number][UNDER_CONSTRUCTION] = True
        self.controller.parent_controller.parent_controller\
            .on_pay_money(self.shop_stages_state_matrix[stage_number][PRICE])

    def on_update_time(self):
        if self.current_stage > 0:
            self.internal_shop_time += 1
            if self.internal_shop_time % FRAMES_IN_ONE_HOUR == 0 \
                    and self.money < self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]:
                self.money += min(self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT],
                                  self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY] - self.money)
                self.view.on_update_storage()

    def on_clear_storage(self):
        self.controller.parent_controller.parent_controller.on_add_money(self.money)
        self.money = 0
        self.view.on_clear_storage()
