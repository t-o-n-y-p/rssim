from logging import getLogger

from controller import *
from ui.fade_animation.fade_in_animation.shop_constructor_fade_in_animation import ShopConstructorFadeInAnimation
from ui.fade_animation.fade_out_animation.shop_constructor_fade_out_animation import ShopConstructorFadeOutAnimation


class ShopConstructorController(MapBaseController, ABC):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(map_id, parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.controller'))
        self.view, self.model = self.create_view_and_model(shop_id)
        self.shop_id = shop_id
        self.fade_in_animation = ShopConstructorFadeInAnimation(self.view)
        self.fade_out_animation = ShopConstructorFadeOutAnimation(self.view)

    @final
    def on_clear_storage(self):
        self.model.on_clear_storage()

    @final
    def on_put_stage_under_construction(self, stage_number):
        self.model.on_put_stage_under_construction(stage_number)
