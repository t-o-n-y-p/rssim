from logging import getLogger

from controller import *


class ShopConstructorController(AppBaseController, GameBaseController):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.controller'))
        self.map_id = map_id
        self.shop_id = shop_id

    @final
    def on_clear_storage(self):
        self.parent_controller.parent_controller.parent_controller.on_add_money(self.model.shop_storage_money
                                                                                * self.model.money_bonus_multiplier)
        self.model.shop_storage_money = 0
        self.view.on_update_storage_money(0)

    @final
    def on_put_stage_under_construction(self, stage_number):
        self.model.on_put_stage_under_construction(stage_number)

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.view.on_change_shop_storage_notification_state(notification_state)
