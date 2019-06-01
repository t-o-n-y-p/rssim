from controller.shop_placeholder_controller import ShopPlaceholderController


class PassengerMapShopPlaceholderController(ShopPlaceholderController):
    def __init__(self, shop_controller, shop_id):
        super().__init__(map_id=0, parent_controller=shop_controller, shop_id=shop_id)
