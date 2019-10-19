from typing import final

from view.shop_view import ShopView


@final
class PassengerMapShopView(ShopView):
    def __init__(self, shop_id):
        super().__init__(map_id=0, shop_id=shop_id)
