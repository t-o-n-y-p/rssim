from typing import final

from view.shop_view import ShopView


@final
class PassengerMapShopView(ShopView):
    def __init__(self, controller, shop_id):
        super().__init__(controller, map_id=0, shop_id=shop_id)
