from typing import final

from controller.shop_controller import ShopController
from model.shop_model.passenger_map_shop_model import PassengerMapShopModel
from view.shop_view.passenger_map_shop_view import PassengerMapShopView
from controller.shop_placeholder_controller.passenger_map_shop_placeholder_controller \
    import PassengerMapShopPlaceholderController
from controller.shop_constructor_controller.passenger_map_constructor_controller \
    import PassengerMapShopConstructorController
from database import PASSENGER_MAP


@final
class PassengerMapShopController(ShopController):
    def __init__(self, map_controller, shop_id):
        super().__init__(map_id=PASSENGER_MAP, parent_controller=map_controller, shop_id=shop_id)

    def create_view_and_model(self, shop_id):
        view = PassengerMapShopView(controller=self, shop_id=shop_id)
        model = PassengerMapShopModel(controller=self, view=view, shop_id=shop_id)
        return view, model

    def create_placeholder(self, shop_id):
        return PassengerMapShopPlaceholderController(self, shop_id=shop_id)

    def create_shop_constructor(self, shop_id):
        return PassengerMapShopConstructorController(self, shop_id=shop_id)
