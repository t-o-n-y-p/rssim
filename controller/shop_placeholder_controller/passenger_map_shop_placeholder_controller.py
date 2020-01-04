from typing import final

from controller.shop_placeholder_controller import ShopPlaceholderController
from model.shop_placeholder_model.passenger_map_shop_placeholder_model import PassengerMapShopPlaceholderModel
from view.shop_placeholder_view.passenger_map_shop_placeholder_view import PassengerMapShopPlaceholderView
from database import PASSENGER_MAP


@final
class PassengerMapShopPlaceholderController(ShopPlaceholderController):
    def __init__(self, shop_controller, shop_id):
        super().__init__(*self.create_shop_placeholder_elements(shop_id), map_id=PASSENGER_MAP,
                         parent_controller=shop_controller, shop_id=shop_id)

    def create_shop_placeholder_elements(self, shop_id):
        view = PassengerMapShopPlaceholderView(controller=self, shop_id=shop_id)
        model = PassengerMapShopPlaceholderModel(controller=self, view=view, shop_id=shop_id)
        return model, view
