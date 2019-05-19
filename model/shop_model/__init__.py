from logging import getLogger

from model import *


class ShopModel(Model):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.model'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.user_db_cursor.execute('''SELECT locked, under_construction, construction_time, current_stage, money, 
                                       next_stage_available, internal_shop_time FROM shops 
                                       WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.locked, self.under_construction, self.construction_time, self.current_stage, self.money, \
            self.next_stage_available, self.internal_shop_time = self.user_db_cursor.fetchone()
        self.locked, self.under_construction, self.next_stage_available \
            = bool(self.locked), bool(self.under_construction), bool(self.next_stage_available)
        self.config_db_cursor.execute('''SELECT track_required, first_available_shop_stage FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.track_required, self.first_available_shop_stage = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT level_required, price, initial_construction_time, hourly_profit, 
                                         storage_capacity, exp_bonus FROM shop_progress_config WHERE map_id = ?''',
                                      (self.map_id, ))
        self.shop_config = self.config_db_cursor.fetchall()

    def on_save_state(self):
        self.user_db_cursor.execute('''UPDATE shops SET locked = ?, under_construction = ?, construction_time = ?,
                                       current_stage = ?, money = ?, next_stage_available = ?, internal_shop_time = ?
                                       WHERE map_id = ? AND shop_id = ?''',
                                    (int(self.locked), int(self.under_construction), self.construction_time,
                                     self.current_stage, self.money, self.next_stage_available, self.internal_shop_time,
                                     self.map_id, self.shop_id))

    def on_activate_view(self):
        self.view.on_activate()

    def on_unlock(self):
        self.locked = False

    def on_put_under_construction(self):
        self.under_construction = True
        if self.current_stage == 0:
            next_stage = self.first_available_shop_stage
        else:
            next_stage = self.current_stage + 1

        self.construction_time = self.shop_config[next_stage][SHOP_INITIAL_CONSTRUCTION_TIME]
        self.view.on_put_under_construction()

    def on_update_time(self):
        if self.current_stage > 0 and not self.under_construction:
            self.internal_shop_time += 1
            if self.internal_shop_time % FRAMES_IN_ONE_HOUR == 0 \
                    and self.money < self.shop_config[self.current_stage][SHOP_STORAGE_CAPACITY]:
                self.money += min(self.shop_config[self.current_stage][SHOP_HOURLY_PROFIT],
                                  self.shop_config[self.current_stage][SHOP_STORAGE_CAPACITY] - self.money)
                self.view.on_update_storage()

        if self.under_construction:
            self.construction_time -= 1
            self.view.on_update_construction_time()
            if self.construction_time == 0:
                self.under_construction = False
                if self.current_stage == 0:
                    self.current_stage = self.first_available_shop_stage
                else:
                    self.current_stage += 1

                self.view.on_construction_completed()

    def on_clear_storage(self):
        self.controller.parent_controller.parent_controller.on_add_money(self.money)
        self.money = 0
        self.view.on_clear_storage()
