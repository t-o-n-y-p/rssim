from model.shop_constructor_model import ShopConstructorModel


class PassengerMapShopConstructorModel(ShopConstructorModel):
    def __init__(self, controller, view, shop_id):
        super().__init__(controller, view, map_id=0, shop_id=shop_id)
