from typing import final

from model.shop_constructor_model import ShopConstructorModel
from database import PASSENGER_MAP


@final
class PassengerMapShopConstructorModel(ShopConstructorModel):
    def __init__(self, controller, view, shop_id):
        super().__init__(controller, view, map_id=PASSENGER_MAP, shop_id=shop_id)
