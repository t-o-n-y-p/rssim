from typing import final

from controller.shop_constructor_controller import ShopConstructorController


@final
class PassengerMapShopConstructorController(ShopConstructorController):
    def __init__(self, shop_controller, shop_id):
        super().__init__(map_id=0, parent_controller=shop_controller, shop_id=shop_id)
