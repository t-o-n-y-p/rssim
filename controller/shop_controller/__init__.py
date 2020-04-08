from abc import ABC, abstractmethod
from logging import getLogger
from typing import final

from controller import MapBaseController
from ui.transition_animation import TransitionAnimation
from ui.fade_animation.fade_in_animation.shop_fade_in_animation import ShopFadeInAnimation
from ui.fade_animation.fade_out_animation.shop_fade_out_animation import ShopFadeOutAnimation


class ShopController(MapBaseController, ABC):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(
            map_id, parent_controller, logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.controller')
        )
        self.view, self.model = self.create_view_and_model(shop_id)
        self.shop_id = shop_id
        self.fade_in_animation = ShopFadeInAnimation(self.view)
        self.fade_out_animation = ShopFadeOutAnimation(self.view)
        self.placeholder = self.create_placeholder(self.shop_id)
        self.shop_constructor = self.create_shop_constructor(self.shop_id)
        self.placeholder_to_shop_constructor_transition_animation = TransitionAnimation(
            fade_out_animation=self.placeholder.fade_out_animation,
            fade_in_animation=self.shop_constructor.fade_in_animation
        )
        self.fade_in_animation.shop_placeholder_fade_in_animation = self.placeholder.fade_in_animation
        self.fade_in_animation.shop_constructor_fade_in_animation = self.shop_constructor.fade_in_animation
        self.fade_out_animation.shop_placeholder_fade_out_animation = self.placeholder.fade_out_animation
        self.fade_out_animation.shop_constructor_fade_out_animation = self.shop_constructor.fade_out_animation
        self.child_controllers = [self.placeholder, self.shop_constructor]

    @abstractmethod
    def create_placeholder(self, shop_id):
        pass

    @abstractmethod
    def create_shop_constructor(self, shop_id):
        pass

    @final
    def on_level_up(self):
        super().on_level_up()
        if self.model.level >= self.model.level_required and self.placeholder.view.is_activated:
            self.placeholder_to_shop_constructor_transition_animation.on_activate()
