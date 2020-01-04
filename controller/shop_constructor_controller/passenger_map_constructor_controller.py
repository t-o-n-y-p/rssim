from typing import final

from controller.shop_constructor_controller import ShopConstructorController
from model.shop_constructor_model.passenger_map_shop_constructor_model import PassengerMapShopConstructorModel
from view.shop_constructor_view.passenger_map_shop_constructor_view import PassengerMapShopConstructorView
from database import PASSENGER_MAP


@final
class PassengerMapShopConstructorController(ShopConstructorController):
    def __init__(self, shop_controller, shop_id):
        super().__init__(*self.create_shop_constructor_elements(shop_id), map_id=PASSENGER_MAP,
                         parent_controller=shop_controller, shop_id=shop_id)

    def create_shop_constructor_elements(self, shop_id):
        view = PassengerMapShopConstructorView(controller=self, shop_id=shop_id)
        model = PassengerMapShopConstructorModel(controller=self, view=view, shop_id=shop_id)
        view.shop_stages_state_matrix = model.shop_stages_state_matrix
        for i in range(1, 5):
            view.shop_stage_cells[i].data = view.shop_stages_state_matrix[i]

        return model, view
