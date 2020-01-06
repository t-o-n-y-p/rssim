from logging import getLogger

from controller import *
from model.shop_constructor_model import ShopConstructorModel
from view.shop_constructor_view import ShopConstructorView
from ui.fade_animation.fade_in_animation.shop_constructor_fade_in_animation import ShopConstructorFadeInAnimation
from ui.fade_animation.fade_out_animation.shop_constructor_fade_out_animation import ShopConstructorFadeOutAnimation


class ShopConstructorController(MapBaseController):
    def __init__(self, model: ShopConstructorModel, view: ShopConstructorView, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.controller'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.fade_in_animation = ShopConstructorFadeInAnimation(self)
        self.fade_out_animation = ShopConstructorFadeOutAnimation(self)
        self.view = view
        self.model = model
        self.view.on_init_content()

    def create_shop_constructor_elements(self, shop_id):
        pass

    @final
    def on_clear_storage(self):
        self.model.on_clear_storage()

    @final
    def on_put_stage_under_construction(self, stage_number):
        self.model.on_put_stage_under_construction(stage_number)

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.view.on_change_shop_storage_notification_state(notification_state)
