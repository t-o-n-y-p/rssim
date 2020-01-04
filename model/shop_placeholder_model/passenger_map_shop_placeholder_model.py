from typing import final

from model.shop_placeholder_model import ShopPlaceholderModel
from database import PASSENGER_MAP


@final
class PassengerMapShopPlaceholderModel(ShopPlaceholderModel):
    def __init__(self, controller, view, shop_id):
        super().__init__(controller, view, map_id=PASSENGER_MAP, shop_id=shop_id)
