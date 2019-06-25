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
            self.view.on_update_stage_state(stage_number)

        self.view.on_update_storage_money(self.shop_storage_money)
        self.view.on_update_money(self.money)

    def on_update_time(self, game_time):
        if self.current_stage > 0 \
                and self.shop_storage_money < self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]:
            self.internal_shop_time += 1
            if self.internal_shop_time % FRAMES_IN_ONE_HOUR == 0:
                self.shop_storage_money += min(self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT],
                                               self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]
                                               - self.shop_storage_money)
                self.view.on_update_storage_money(self.shop_storage_money)

        for stage in self.shop_stages_state_matrix:
            if self.shop_stages_state_matrix[stage][UNDER_CONSTRUCTION]:
                self.shop_stages_state_matrix[stage][CONSTRUCTION_TIME] -= 1
                if self.shop_stages_state_matrix[stage][CONSTRUCTION_TIME] == 0:
                    self.shop_stages_state_matrix[stage][UNDER_CONSTRUCTION] = False
                    self.shop_stages_state_matrix[stage][LOCKED] = False
                    self.current_stage = stage
                    self.view.on_unlock_stage(stage)
                    if stage == 1:
                        self.controller.parent_controller.parent_controller.parent_controller\
                            .on_add_exp_bonus(round(self.shop_stages_state_matrix[stage][EXP_BONUS], 2))
                    else:
                        self.controller.parent_controller.parent_controller.parent_controller\
                            .on_add_exp_bonus(round(self.shop_stages_state_matrix[stage][EXP_BONUS]
                                                    - self.shop_stages_state_matrix[stage - 1][EXP_BONUS], 2))

                    if stage < 4:
                        self.shop_stages_state_matrix[stage + 1][UNLOCK_CONDITION_FROM_PREVIOUS_STAGE] = True
                        self.on_check_shop_stage_unlock_conditions(stage + 1)
                        self.view.on_update_stage_state(self.shop_stages_state_matrix, stage + 1)

                self.view.on_update_stage_state(self.shop_stages_state_matrix, stage)

    def on_save_state(self):
        self.user_db_cursor.execute('''UPDATE shops SET current_stage = ?, shop_storage_money = ?, 
                                       internal_shop_time = ? WHERE map_id = ? AND shop_id = ?''',
                                    (self.current_stage, self.shop_storage_money, self.internal_shop_time,
                                     self.map_id, self.shop_id))
        for stage_number in self.shop_stages_state_matrix:
            self.user_db_cursor.execute('''UPDATE shop_stages SET locked = ?, under_construction = ?, 
                                           construction_time = ?, unlock_condition_from_level = ?, 
                                           unlock_condition_from_previous_stage = ?, unlock_available = ?
                                           WHERE map_id = ? AND shop_id = ? AND stage_number = ?''',
                                        tuple(map(int, (
                                            self.shop_stages_state_matrix[stage_number][LOCKED],
                                            self.shop_stages_state_matrix[stage_number][UNDER_CONSTRUCTION],
                                            self.shop_stages_state_matrix[stage_number][CONSTRUCTION_TIME],
                                            self.shop_stages_state_matrix[stage_number][UNLOCK_CONDITION_FROM_LEVEL],
                                            self.shop_stages_state_matrix[stage_number][
                                                                            UNLOCK_CONDITION_FROM_PREVIOUS_STAGE],
                                            self.shop_stages_state_matrix[stage_number][UNLOCK_AVAILABLE],
                                            self.map_id, self.shop_id, stage_number
                                        ))))

    def on_add_money(self, money):
        self.money += money
        self.view.on_update_money(self.money)

    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money)

    def on_level_up(self, level):
        for stage in self.shop_stages_state_matrix:
            if self.shop_stages_state_matrix[stage][LEVEL_REQUIRED] == level:
                self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL] = True
                self.on_check_shop_stage_unlock_conditions(stage)
                self.view.on_update_stage_state(self.shop_stages_state_matrix, stage)

    def on_check_shop_stage_unlock_conditions(self, stage):
        if self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_PREVIOUS_STAGE] \
                and self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL]:
            self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_PREVIOUS_STAGE] = False
            self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL] = False
            self.shop_stages_state_matrix[stage][UNLOCK_AVAILABLE] = True

    def on_put_stage_under_construction(self, stage_number):
        self.shop_stages_state_matrix[stage_number][UNLOCK_AVAILABLE] = False
        self.shop_stages_state_matrix[stage_number][UNDER_CONSTRUCTION] = True
        self.view.on_update_stage_state(self.shop_stages_state_matrix, stage_number)
        self.controller.parent_controller.parent_controller.parent_controller \
            .on_pay_money(self.shop_stages_state_matrix[stage_number][PRICE])
