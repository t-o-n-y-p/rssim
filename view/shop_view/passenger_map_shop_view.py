from typing import final

from view.shop_view import ShopView
from database import PASSENGER_MAP


@final
class PassengerMapShopView(ShopView):
    def __init__(self, controller, shop_id):
        super().__init__(controller, map_id=PASSENGER_MAP, shop_id=shop_id)
