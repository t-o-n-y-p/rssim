from typing import final

from view.shop_constructor_view import ShopConstructorView
from database import PASSENGER_MAP


@final
class PassengerMapShopConstructorView(ShopConstructorView):
    def __init__(self, controller, shop_id):
        super().__init__(controller, map_id=PASSENGER_MAP, shop_id=shop_id)
