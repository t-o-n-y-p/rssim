from logging import getLogger

from controller import *


class ShopConstructorController(AppBaseController, GameBaseController):
    def __init__(self, map_id, shop_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.controller'))
        self.map_id = map_id
        self.shop_id = shop_id

    @final
    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    @final
    def on_activate_view(self):
        self.model.on_activate_view()

    @final
    def on_deactivate_view(self):
        self.view.on_deactivate()

    @final
    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)

    @final
    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    @final
    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    @final
    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()

    @final
    def on_save_state(self):
        self.model.on_save_state()

    @final
    def on_clear_storage(self):
        self.parent_controller.parent_controller.parent_controller.on_add_money(self.model.shop_storage_money
                                                                                * self.model.money_bonus_multiplier)
        self.model.shop_storage_money = 0
        self.view.on_update_storage_money(0)

    @final
    def on_put_stage_under_construction(self, stage_number):
        self.model.on_put_stage_under_construction(stage_number)

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.view.on_change_shop_storage_notification_state(notification_state)
