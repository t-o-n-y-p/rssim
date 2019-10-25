from typing import final

from view.shop_placeholder_view import ShopPlaceholderView


@final
class PassengerMapShopPlaceholderView(ShopPlaceholderView):
    def __init__(self, controller, shop_id):
        super().__init__(controller, map_id=0, shop_id=shop_id)
