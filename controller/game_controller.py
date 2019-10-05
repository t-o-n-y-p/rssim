from logging import getLogger

from controller import *
from database import on_commit


class GameController(Controller):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.game.controller'))
        self.maps = []
        self.map_transition_animations = []

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()
        for map_ in self.maps:
            map_.on_update_view()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        for map_ in self.maps:
            map_.on_change_screen_resolution(screen_resolution)

    def on_pause_game(self):
        self.model.on_pause_game()

    def on_resume_game(self):
        self.model.on_resume_game()

    def on_activate_view(self):
        self.model.on_activate_view()
        self.maps[self.model.get_active_map()].on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        for map_ in self.maps:
            map_.on_deactivate_view()

    @game_is_not_paused
    def on_update_time(self):
        self.parent_controller.bonus_code.on_update_time(self.model.game_time)
        for map_ in self.maps:
            map_.on_update_time(self.model.game_time)

        self.model.on_update_time()
        if self.model.game_time % (FRAMES_IN_ONE_HOUR * 2) == 0:
            self.on_save_and_commit_state()

    def on_save_and_commit_state(self):
        self.model.on_save_state()
        self.parent_controller.bonus_code.on_save_state()
        for map_ in self.maps:
            map_.on_save_state()

        on_commit()

    def on_level_up(self):
        self.model.on_level_up()
        self.parent_controller.bonus_code.on_level_up(self.model.level)
        for map_ in self.maps:
            map_.on_level_up(self.model.level)

    def on_update_money_target(self, money_target):
        self.model.on_update_money_target(money_target)

    def on_add_exp(self, exp):
        self.model.on_add_exp(exp)

    def on_add_money(self, money):
        profit = self.model.on_add_money(money)
        for map_ in self.maps:
            map_.on_add_money(profit)

    def on_pay_money(self, money):
        self.model.on_pay_money(money)
        for map_ in self.maps:
            map_.on_pay_money(money)

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)
        for map_ in self.maps:
            map_.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()
        for map_ in self.maps:
            map_.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()
        for map_ in self.maps:
            map_.on_enable_notifications()

    def on_change_level_up_notification_state(self, notification_state):
        self.view.on_change_level_up_notification_state(notification_state)

    def on_change_feature_unlocked_notification_state(self, notification_state):
        for map_ in self.maps:
            map_.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        for map_ in self.maps:
            map_.on_change_construction_completed_notification_state(notification_state)

    def on_change_enough_money_notification_state(self, notification_state):
        self.view.on_change_enough_money_notification_state(notification_state)

    def on_change_bonus_expired_notification_state(self, notification_state):
        self.view.on_change_bonus_expired_notification_state(notification_state)

    def on_change_shop_storage_notification_state(self, notification_state):
        for map_ in self.maps:
            map_.on_change_shop_storage_notification_state(notification_state)

    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()
        for map_ in self.maps:
            map_.on_apply_shaders_and_draw_vertices()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        for map_ in self.maps:
            map_.on_update_fade_animation_state(new_state)

    def on_deactivate_money_target_for_inactive_maps(self, active_map_id):
        for i in range(len(self.maps)):
            if i != active_map_id:
                self.maps[i].constructor.on_deactivate_money_target()

    def on_update_clock_state(self, clock_24h_enabled):
        self.view.on_update_clock_state(clock_24h_enabled)
        for map_ in self.maps:
            map_.on_update_clock_state(clock_24h_enabled)

    def on_add_exp_bonus(self, exp_bonus):
        self.model.on_add_exp_bonus(exp_bonus)

    def on_activate_exp_bonus_code(self, value):
        self.model.on_activate_exp_bonus_code(value)

    def on_deactivate_exp_bonus_code(self):
        self.model.on_deactivate_exp_bonus_code()

    def on_activate_money_bonus_code(self, value):
        self.model.on_activate_money_bonus_code(value)

    def on_deactivate_money_bonus_code(self):
        self.model.on_deactivate_money_bonus_code()
