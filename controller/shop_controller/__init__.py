from logging import getLogger

from controller import *


class ShopController(Controller):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.controller'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.placeholder = None
        self.shop_constructor = None
        self.placeholder_to_shop_constructor_transition_animation = None

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()
        self.placeholder.on_update_view()
        self.shop_constructor.on_update_view()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        self.placeholder.on_change_screen_resolution(screen_resolution)
        self.shop_constructor.on_change_screen_resolution(screen_resolution)

    def on_save_state(self):
        self.shop_constructor.on_save_state()

    def on_update_time(self, game_time):
        self.shop_constructor.on_update_time(game_time)

    def on_level_up(self, level):
        self.model.on_level_up(level)
        if self.model.level >= self.model.level_required and self.placeholder.view.is_activated:
            self.placeholder_to_shop_constructor_transition_animation.on_activate()

        self.shop_constructor.on_level_up(level)

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.placeholder.on_deactivate_view()
        self.shop_constructor.on_deactivate_view()

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)
        self.placeholder.on_update_current_locale(new_locale)
        self.shop_constructor.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()
        self.placeholder.on_disable_notifications()
        self.shop_constructor.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()
        self.placeholder.on_enable_notifications()
        self.shop_constructor.on_enable_notifications()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        self.placeholder.on_update_fade_animation_state(new_state)
        self.shop_constructor.on_update_fade_animation_state(new_state)

    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()
        self.shop_constructor.on_apply_shaders_and_draw_vertices()

    def on_add_money(self, money):
        self.shop_constructor.on_add_money(money)

    def on_pay_money(self, money):
        self.shop_constructor.on_pay_money(money)
