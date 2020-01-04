from typing import final

from view.shop_placeholder_view import ShopPlaceholderView
from database import PASSENGER_MAP


@final
class PassengerMapShopPlaceholderView(ShopPlaceholderView):
    def __init__(self, controller, shop_id):
        super().__init__(controller, map_id=PASSENGER_MAP, shop_id=shop_id)
