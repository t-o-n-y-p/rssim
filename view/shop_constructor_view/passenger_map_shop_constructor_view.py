from typing import final

from view.shop_constructor_view import ShopConstructorView


@final
class PassengerMapShopConstructorView(ShopConstructorView):
    def __init__(self, shop_id):
        super().__init__(map_id=0, shop_id=shop_id)
