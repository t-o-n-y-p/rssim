from logging import getLogger

from controller import *
from model.game_model import GameModel
from view.game_view import GameView
from ui.fade_animation.fade_in_animation.game_fade_in_animation import GameFadeInAnimation
from ui.fade_animation.fade_out_animation.game_fade_out_animation import GameFadeOutAnimation
from controller.bonus_code_manager_controller import BonusCodeManagerController
from controller.map_controller.passenger_map_controller import PassengerMapController


@final
class GameController(GameBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.game.controller'))
        self.fade_in_animation = GameFadeInAnimation(self)
        self.fade_out_animation = GameFadeOutAnimation(self)
        self.view = GameView(controller=self)
        self.model = GameModel(controller=self, view=self.view)
        self.view.on_init_content()
        self.bonus_code_manager = BonusCodeManagerController(self)
        self.maps = [PassengerMapController(self), ]
        self.fade_in_animation.bonus_code_manager_fade_in_animation = self.bonus_code_manager.fade_in_animation
        self.fade_out_animation.bonus_code_manager_fade_out_animation = self.bonus_code_manager.fade_out_animation
        for m in self.maps:
            self.fade_in_animation.map_fade_in_animations.append(m.fade_in_animation)
            self.fade_out_animation.map_fade_out_animations.append(m.fade_out_animation)

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

    def on_update_clock_state(self, clock_24h_enabled):
        super().on_update_clock_state(clock_24h_enabled)
        for m in self.maps:
            m.on_update_clock_state(clock_24h_enabled)

    @game_is_not_paused
    def on_update_time(self):
        super().on_update_time()
        self.bonus_code_manager.on_update_time()
        for m in self.maps:
            m.on_update_time()

        if self.model.game_time % (FRAMES_IN_ONE_HOUR * 2) == 0:
            self.parent_controller.on_save_state()

    def on_level_up(self):
        super().on_level_up()
        for m in self.maps:
            m.on_level_up()

    def on_add_money(self, money):
        super().on_add_money(money)
        for m in self.maps:
            m.on_add_money(money)

    def on_pay_money(self, money):
        super().on_pay_money(money)
        for m in self.maps:
            m.on_pay_money(money)

    def on_activate_exp_bonus_code(self, value):
        super().on_activate_exp_bonus_code(value)
        for m in self.maps:
            m.on_activate_exp_bonus_code(value)

    def on_activate_money_bonus_code(self, value):
        super().on_activate_money_bonus_code(value)
        for m in self.maps:
            m.on_activate_money_bonus_code(value)

    def on_deactivate_exp_bonus_code(self):
        super().on_deactivate_exp_bonus_code()
        self.bonus_code_manager.on_deactivate_exp_bonus_code()
        for m in self.maps:
            m.on_deactivate_exp_bonus_code()

    def on_deactivate_money_bonus_code(self):
        super().on_deactivate_money_bonus_code()
        self.bonus_code_manager.on_deactivate_money_bonus_code()
        for m in self.maps:
            m.on_deactivate_money_bonus_code()

    def on_pause_game(self):
        self.model.on_pause_game()

    def on_resume_game(self):
        self.model.on_resume_game()

    def on_update_money_target(self, money_target):
        self.model.on_update_money_target(money_target)

    def on_add_exp(self, exp):
        self.model.on_add_exp(exp)

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

    def on_add_exp_bonus(self, exp_bonus):
        self.model.on_add_exp_bonus(exp_bonus)

    def on_activate_new_bonus_code(self, sha512_hash):
        self.bonus_code_manager.on_activate_new_bonus_code(sha512_hash)
        if (bonus_code_type := self.bonus_code_manager.model.get_bonus_code_type(sha512_hash)) == 'exp_bonus':
            self.on_activate_exp_bonus_code(self.bonus_code_manager.model.get_bonus_code_value(sha512_hash) - 1)
        elif bonus_code_type == 'money_bonus':
            self.on_activate_money_bonus_code(self.bonus_code_manager.model.get_bonus_code_value(sha512_hash) - 1)
