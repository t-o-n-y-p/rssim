from model.shop_placeholder_model import ShopPlaceholderModel


class PassengerMapShopPlaceholderModel(ShopPlaceholderModel):
    def __init__(self, controller, view, shop_id):
        super().__init__(controller, view, map_id=0, shop_id=shop_id)
