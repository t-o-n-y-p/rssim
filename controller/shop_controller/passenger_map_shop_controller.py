from typing import final

from controller.shop_controller import ShopController


@final
class PassengerMapShopController(ShopController):
    def __init__(self, map_controller, shop_id):
        super().__init__(map_id=0, parent_controller=map_controller, shop_id=shop_id)
