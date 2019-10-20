from logging import getLogger

from controller import *


class ShopController(AppBaseController, GameBaseController):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.controller'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.placeholder = None
        self.shop_constructor = None
        self.placeholder_to_shop_constructor_transition_animation = None

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

    def on_activate_money_bonus_code(self, value):
        super().on_activate_money_bonus_code(value)
        self.shop_constructor.on_activate_money_bonus_code(value)

    def on_deactivate_money_bonus_code(self):
        super().on_deactivate_money_bonus_code()
        self.shop_constructor.on_deactivate_money_bonus_code()

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.shop_constructor.on_change_shop_storage_notification_state(notification_state)
