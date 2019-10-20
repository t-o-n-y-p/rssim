from logging import getLogger

from controller import *


class ConstructorController(AppBaseController, GameBaseController):
    def __init__(self, map_id, parent_controller):
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.constructor.controller'))
        self.map_id = map_id

    @final
    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    @final
    def on_save_state(self):
        self.model.on_save_state()

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    @final
    def on_activate_view(self):
        self.model.on_activate_view()

    @final
    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.parent_controller.on_close_constructor()

    @final
    def on_put_under_construction(self, construction_type, entity_number):
        self.model.on_put_under_construction(construction_type, entity_number)

    @final
    def on_add_money(self, money):
        self.model.on_add_money(money)

    @final
    def on_pay_money(self, money):
        self.model.on_pay_money(money)

    @final
    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    @final
    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    @final
    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    @final
    def on_activate_money_target(self, construction_type, row):
        self.model.on_activate_money_target(construction_type, row)
        self.parent_controller.parent_controller.on_deactivate_money_target_for_inactive_maps(self.map_id)

    @final
    def on_deactivate_money_target(self):
        self.model.on_deactivate_money_target()

    @final
    def on_change_feature_unlocked_notification_state(self, notification_state):
        self.view.on_change_feature_unlocked_notification_state(notification_state)

    @final
    def on_change_construction_completed_notification_state(self, notification_state):
        self.view.on_change_construction_completed_notification_state(notification_state)

    @final
    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
