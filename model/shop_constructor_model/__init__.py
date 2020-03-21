from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class ShopConstructorModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, shop_id):
        super().__init__(controller, view, map_id,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.model'))
        self.shop_id = shop_id
        self.shop_stages_state_matrix = {}
        USER_DB_CURSOR.execute('''SELECT stage_number, locked, under_construction, construction_time,
                                  unlock_condition_from_level, unlock_condition_from_previous_stage,
                                  unlock_available FROM shop_stages WHERE map_id = ? AND shop_id = ?''',
                               (self.map_id, self.shop_id))
        for stage_info in USER_DB_CURSOR.fetchall():
            self.shop_stages_state_matrix[stage_info[0]] = [*stage_info[1:6], 1, stage_info[6]]
            CONFIG_DB_CURSOR.execute('''SELECT price, max_construction_time, level_required, hourly_profit,
                                        storage_capacity, exp_bonus FROM shop_progress_config
                                        WHERE map_id = ? AND stage_number = ?''',
                                     (self.map_id, stage_info[0]))
            stage_progress_config = CONFIG_DB_CURSOR.fetchone()
            self.shop_stages_state_matrix[stage_info[0]].extend([*stage_progress_config[:3],
                                                                 0, *stage_progress_config[3:]])

        USER_DB_CURSOR.execute('''SELECT current_stage, shop_storage_money, internal_shop_time
                                  FROM shops WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.current_stage, self.shop_storage_money, self.internal_shop_time = USER_DB_CURSOR.fetchone()

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE shops SET current_stage = ?, shop_storage_money = ?, 
                                  internal_shop_time = ? WHERE map_id = ? AND shop_id = ?''',
                               (self.current_stage, self.shop_storage_money, self.internal_shop_time,
                                self.map_id, self.shop_id))
        for stage_number in self.shop_stages_state_matrix:
            USER_DB_CURSOR.execute('''UPDATE shop_stages SET locked = ?, under_construction = ?, 
                                      construction_time = ?, unlock_condition_from_level = ?, 
                                      unlock_condition_from_previous_stage = ?, unlock_available = ?
                                      WHERE map_id = ? AND shop_id = ? AND stage_number = ?''',
                                   (
                                        self.shop_stages_state_matrix[stage_number][LOCKED],
                                        self.shop_stages_state_matrix[stage_number][UNDER_CONSTRUCTION],
                                        self.shop_stages_state_matrix[stage_number][CONSTRUCTION_TIME],
                                        self.shop_stages_state_matrix[stage_number][UNLOCK_CONDITION_FROM_LEVEL],
                                        self.shop_stages_state_matrix[stage_number][
                                                                                UNLOCK_CONDITION_FROM_PREVIOUS_STAGE],
                                        self.shop_stages_state_matrix[stage_number][UNLOCK_AVAILABLE],
                                        self.map_id, self.shop_id, stage_number
                                    )
                                   )

    @final
    def on_update_time(self, dt):
        if self.current_stage > 0 \
                and self.shop_storage_money < self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]:
            if self.internal_shop_time // SECONDS_IN_ONE_HOUR \
                    < (self.internal_shop_time + int(self.game_time_fraction + dt * self.dt_multiplier)) \
                    // SECONDS_IN_ONE_HOUR:
                if self.shop_storage_money \
                        < round(self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]
                                * SHOP_STORAGE_ALMOST_FULL_THRESHOLD) \
                        <= self.shop_storage_money + self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT]:
                    self.view.on_send_shop_storage_almost_full_notification()
                elif self.shop_storage_money \
                        < self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY] \
                        <= self.shop_storage_money + self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT]:
                    self.view.on_send_shop_storage_full_notification()

                self.shop_storage_money += min(self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT],
                                               self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]
                                               - self.shop_storage_money)
                self.view.on_update_storage_money(self.shop_storage_money)

            self.internal_shop_time += int(self.game_time_fraction + dt * self.dt_multiplier)

        for stage in self.shop_stages_state_matrix:
            if self.shop_stages_state_matrix[stage][UNDER_CONSTRUCTION]:
                self.shop_stages_state_matrix[stage][CONSTRUCTION_TIME] \
                    -= int(self.game_time_fraction + dt * self.dt_multiplier)
                if self.shop_stages_state_matrix[stage][CONSTRUCTION_TIME] <= 0:
                    self.shop_stages_state_matrix[stage][UNDER_CONSTRUCTION] = FALSE
                    self.shop_stages_state_matrix[stage][LOCKED] = FALSE
                    self.current_stage = stage
                    self.view.on_unlock_stage(stage)
                    if stage == 1:
                        self.controller.parent_controller.parent_controller.parent_controller\
                            .on_add_exp_bonus(round(self.shop_stages_state_matrix[stage][EXP_BONUS] / 100, 4))
                    else:
                        self.controller.parent_controller.parent_controller.parent_controller\
                            .on_add_exp_bonus(round((self.shop_stages_state_matrix[stage][EXP_BONUS]
                                                     - self.shop_stages_state_matrix[stage - 1][EXP_BONUS]) / 100, 4))

                    if stage < 4:
                        self.shop_stages_state_matrix[stage + 1][UNLOCK_CONDITION_FROM_PREVIOUS_STAGE] = TRUE
                        self.on_check_shop_stage_unlock_conditions(stage + 1)
                        self.view.on_update_stage_state(stage + 1)

                self.view.on_update_stage_state(stage)

        super().on_update_time(dt)

    @final
    def on_level_up(self):
        super().on_level_up()
        for stage in self.shop_stages_state_matrix:
            if self.shop_stages_state_matrix[stage][LEVEL_REQUIRED] == self.level:
                self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL] = TRUE
                self.on_check_shop_stage_unlock_conditions(stage)
                self.view.on_update_stage_state(stage)

    @final
    def on_check_shop_stage_unlock_conditions(self, stage):
        if self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_PREVIOUS_STAGE] \
                and self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL]:
            self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_PREVIOUS_STAGE] = FALSE
            self.shop_stages_state_matrix[stage][UNLOCK_CONDITION_FROM_LEVEL] = FALSE
            self.shop_stages_state_matrix[stage][UNLOCK_AVAILABLE] = TRUE

    @final
    def on_put_stage_under_construction(self, stage_number):
        self.shop_stages_state_matrix[stage_number][UNLOCK_AVAILABLE] = FALSE
        self.shop_stages_state_matrix[stage_number][UNDER_CONSTRUCTION] = TRUE
        self.shop_stages_state_matrix[stage_number][CONSTRUCTION_TIME] \
            = int(self.shop_stages_state_matrix[stage_number][MAX_CONSTRUCTION_TIME]
                  * self.construction_time_bonus_multiplier)
        self.view.on_update_stage_state(stage_number)
        self.controller.parent_controller.parent_controller.parent_controller \
            .on_pay_money(self.shop_stages_state_matrix[stage_number][PRICE])

    @final
    def on_clear_storage(self):
        self.controller.parent_controller.parent_controller.parent_controller\
            .on_add_money(self.shop_storage_money * self.money_bonus_multiplier)
        self.shop_storage_money = 0
        self.view.on_update_storage_money(0)
