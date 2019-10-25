from typing import final

from controller.shop_controller import ShopController
from model.shop_model.passenger_map_shop_model import PassengerMapShopModel
from view.shop_view.passenger_map_shop_view import PassengerMapShopView
from controller.shop_placeholder_controller.passenger_map_shop_placeholder_controller \
    import PassengerMapShopPlaceholderController
from controller.shop_constructor_controller.passenger_map_constructor_controller \
    import PassengerMapShopConstructorController


@final
class PassengerMapShopController(ShopController):
    def __init__(self, map_controller, shop_id):
        super().__init__(*self.create_shop_elements(shop_id), map_id=0,
                         parent_controller=map_controller, shop_id=shop_id)

    def create_shop_elements(self, shop_id):
        view = PassengerMapShopView(controller=self, shop_id=shop_id)
        model = PassengerMapShopModel(controller=self, view=view, shop_id=shop_id)
        placeholder = PassengerMapShopPlaceholderController(self, shop_id=shop_id)
        shop_constructor = PassengerMapShopConstructorController(self, shop_id=shop_id)
        return model, view, placeholder, shop_constructor
