from logging import getLogger

from controller import *
from ui.transition_animation import TransitionAnimation
from model.shop_model import ShopModel
from view.shop_view import ShopView
from ui.fade_animation.fade_in_animation.shop_fade_in_animation import ShopFadeInAnimation
from ui.fade_animation.fade_out_animation.shop_fade_out_animation import ShopFadeOutAnimation
from controller.shop_placeholder_controller import ShopPlaceholderController
from controller.shop_constructor_controller import ShopConstructorController


class ShopController(GameBaseController):
    def __init__(self, model: ShopModel, view: ShopView, placeholder: ShopPlaceholderController,
                 shop_constructor: ShopConstructorController, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.controller'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.fade_in_animation = ShopFadeInAnimation(self)
        self.fade_out_animation = ShopFadeOutAnimation(self)
        self.view = view
        self.model = model
        self.view.on_init_content()
        self.placeholder = placeholder
        self.shop_constructor = shop_constructor
        self.placeholder_to_shop_constructor_transition_animation = \
            TransitionAnimation(fade_out_animation=self.placeholder.fade_out_animation,
                                fade_in_animation=self.shop_constructor.fade_in_animation)
        self.fade_in_animation.shop_placeholder_fade_in_animation = self.placeholder.fade_in_animation
        self.fade_in_animation.shop_constructor_fade_in_animation = self.shop_constructor.fade_in_animation
        self.fade_out_animation.shop_placeholder_fade_out_animation = self.placeholder.fade_out_animation
        self.fade_out_animation.shop_constructor_fade_out_animation = self.shop_constructor.fade_out_animation
        self.child_controllers = [self.placeholder, self.shop_constructor]

    def create_shop_elements(self, shop_id):
        pass

    @final
    def on_level_up(self):
        super().on_level_up()
        if self.model.level >= self.model.level_required and self.placeholder.view.is_activated:
            self.placeholder_to_shop_constructor_transition_animation.on_activate()

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.shop_constructor.on_change_shop_storage_notification_state(notification_state)
