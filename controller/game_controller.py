from logging import getLogger

from controller import *


@final
class GameController(AppBaseController, GameBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.game.controller'))
        self.bonus_code_manager = None
        self.maps = []
        self.map_transition_animations = []

    def on_activate_view(self):
        super().on_activate_view()
        self.bonus_code_manager.on_activate_view()
        self.maps[self.model.get_active_map()].on_activate_view()

    def on_deactivate_view(self):
        super().on_deactivate_view()
        self.bonus_code_manager.on_deactivate_view()
        for m in self.maps:
            m.on_deactivate_view()

    def on_update_view(self):
        super().on_update_view()
        self.bonus_code_manager.on_update_view()
        for m in self.maps:
            m.on_update_view()

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.bonus_code_manager.on_update_current_locale(new_locale)
        for m in self.maps:
            m.on_update_current_locale(new_locale)

    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.bonus_code_manager.on_change_screen_resolution(screen_resolution)
        for m in self.maps:
            m.on_change_screen_resolution(screen_resolution)

    def on_apply_shaders_and_draw_vertices(self):
        super().on_apply_shaders_and_draw_vertices()
        self.bonus_code_manager.on_apply_shaders_and_draw_vertices()
        for m in self.maps:
            m.on_apply_shaders_and_draw_vertices()

    def on_disable_notifications(self):
        super().on_disable_notifications()
        self.bonus_code_manager.on_disable_notifications()
        for m in self.maps:
            m.on_disable_notifications()

    def on_enable_notifications(self):
        super().on_enable_notifications()
        self.bonus_code_manager.on_enable_notifications()
        for m in self.maps:
            m.on_enable_notifications()

    def on_update_fade_animation_state(self, new_state):
        super().on_update_fade_animation_state(new_state)
        self.bonus_code_manager.on_update_fade_animation_state(new_state)
        for m in self.maps:
            m.on_update_fade_animation_state(new_state)

    def on_save_state(self):
        super().on_save_state()
        self.bonus_code_manager.on_save_state()
        for m in self.maps:
            m.on_save_state()

    @game_is_not_paused
    def on_update_time(self):
        super().on_update_time()
        self.bonus_code_manager.on_update_time()
        for m in self.maps:
            m.on_update_time()

        if self.model.game_time % (FRAMES_IN_ONE_HOUR * 2) == 0:
            self.parent_controller.on_save_state()

    def on_pause_game(self):
        self.model.on_pause_game()

    def on_resume_game(self):
        self.model.on_resume_game()

    def on_level_up(self):
        self.model.on_level_up()
        for m in self.maps:
            m.on_level_up(self.model.level)

    def on_update_money_target(self, money_target):
        self.model.on_update_money_target(money_target)

    def on_add_exp(self, exp):
        self.model.on_add_exp(exp)

    def on_add_money(self, money):
        profit = self.model.on_add_money(money)
        for m in self.maps:
            m.on_add_money(profit)

    def on_pay_money(self, money):
        self.model.on_pay_money(money)
        for m in self.maps:
            m.on_pay_money(money)

    def on_change_level_up_notification_state(self, notification_state):
        self.view.on_change_level_up_notification_state(notification_state)

    def on_change_feature_unlocked_notification_state(self, notification_state):
        for m in self.maps:
            m.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        for m in self.maps:
            m.on_change_construction_completed_notification_state(notification_state)

    def on_change_enough_money_notification_state(self, notification_state):
        self.view.on_change_enough_money_notification_state(notification_state)

    def on_change_bonus_expired_notification_state(self, notification_state):
        self.bonus_code_manager.on_change_bonus_expired_notification_state(notification_state)

    def on_change_shop_storage_notification_state(self, notification_state):
        for map_ in self.maps:
            map_.on_change_shop_storage_notification_state(notification_state)

    def on_deactivate_money_target_for_inactive_maps(self, active_map_id):
        for i in range(len(self.maps)):
            if i != active_map_id:
                self.maps[i].constructor.on_deactivate_money_target()

    def on_update_clock_state(self, clock_24h_enabled):
        self.view.on_update_clock_state(clock_24h_enabled)
        for m in self.maps:
            m.on_update_clock_state(clock_24h_enabled)

    def on_add_exp_bonus(self, exp_bonus):
        self.model.on_add_exp_bonus(exp_bonus)

    def on_activate_new_bonus_code(self, sha512_hash):
        self.bonus_code_manager.on_activate_new_bonus_code(sha512_hash)
        if (bonus_code_type := self.bonus_code_manager.model.get_bonus_code_type(sha512_hash)) == 'exp_bonus':
            self.model.on_activate_exp_bonus_code(self.bonus_code_manager.model.get_bonus_code_value(sha512_hash) - 1)
        elif bonus_code_type == 'money_bonus':
            self.model.on_activate_money_bonus_code(self.bonus_code_manager.model.get_bonus_code_value(sha512_hash) - 1)

    def on_deactivate_exp_bonus_code(self):
        self.model.on_deactivate_exp_bonus_code()
        self.bonus_code_manager.on_deactivate_exp_bonus_code()

    def on_deactivate_money_bonus_code(self):
        self.model.on_deactivate_money_bonus_code()
        self.bonus_code_manager.on_deactivate_money_bonus_code()
