from model.shop_model import ShopModel


class PassengerMapShopModel(ShopModel):
    def __init__(self, shop_id):
        super().__init__(map_id=0, shop_id=shop_id)
