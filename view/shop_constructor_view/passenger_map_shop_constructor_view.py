from typing import final

from view.shop_constructor_view import ShopConstructorView


@final
class PassengerMapShopConstructorView(ShopConstructorView):
    def __init__(self, controller, shop_id):
        super().__init__(controller, map_id=0, shop_id=shop_id)
