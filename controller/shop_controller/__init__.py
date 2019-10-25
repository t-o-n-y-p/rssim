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

    def create_shop_elements(self, shop_id):
        pass

    @final
    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.placeholder.on_deactivate_view()
        self.shop_constructor.on_deactivate_view()

    @final
    def on_update_view(self):
        super().on_update_view()
        self.placeholder.on_update_view()
        self.shop_constructor.on_update_view()

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.placeholder.on_update_current_locale(new_locale)
        self.shop_constructor.on_update_current_locale(new_locale)

    @final
    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.placeholder.on_change_screen_resolution(screen_resolution)
        self.shop_constructor.on_change_screen_resolution(screen_resolution)

    @final
    def on_apply_shaders_and_draw_vertices(self):
        super().on_apply_shaders_and_draw_vertices()
        self.shop_constructor.on_apply_shaders_and_draw_vertices()

    @final
    def on_disable_notifications(self):
        super().on_disable_notifications()
        self.placeholder.on_disable_notifications()
        self.shop_constructor.on_disable_notifications()

    @final
    def on_enable_notifications(self):
        super().on_enable_notifications()
        self.placeholder.on_enable_notifications()
        self.shop_constructor.on_enable_notifications()

    @final
    def on_update_fade_animation_state(self, new_state):
        super().on_update_fade_animation_state(new_state)
        self.placeholder.on_update_fade_animation_state(new_state)
        self.shop_constructor.on_update_fade_animation_state(new_state)

    @final
    def on_save_state(self):
        self.shop_constructor.on_save_state()

    @final
    def on_update_time(self):
        super().on_update_time()
        self.shop_constructor.on_update_time()

    @final
    def on_level_up(self):
        super().on_level_up()
        if self.model.level >= self.model.level_required and self.placeholder.view.is_activated:
            self.placeholder_to_shop_constructor_transition_animation.on_activate()

        self.shop_constructor.on_level_up()

    @final
    def on_add_money(self, money):
        super().on_add_money(money)
        self.shop_constructor.on_add_money(money)

    @final
    def on_pay_money(self, money):
        super().on_pay_money(money)
        self.shop_constructor.on_pay_money(money)

    @final
    def on_activate_money_bonus_code(self, value):
        super().on_activate_money_bonus_code(value)
        self.shop_constructor.on_activate_money_bonus_code(value)

    @final
    def on_deactivate_money_bonus_code(self):
        super().on_deactivate_money_bonus_code()
        self.shop_constructor.on_deactivate_money_bonus_code()

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.shop_constructor.on_change_shop_storage_notification_state(notification_state)
