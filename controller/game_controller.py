from logging import getLogger

from controller import *
from model.game_model import GameModel
from view.game_view import GameView
from ui.fade_animation.fade_in_animation.game_fade_in_animation import GameFadeInAnimation
from ui.fade_animation.fade_out_animation.game_fade_out_animation import GameFadeOutAnimation
from controller.bonus_code_manager_controller import BonusCodeManagerController
from controller.map_switcher_controller import MapSwitcherController
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
        self.map_switcher = MapSwitcherController(self)
        self.maps = [PassengerMapController(self), ]
        self.fade_in_animation.bonus_code_manager_fade_in_animation = self.bonus_code_manager.fade_in_animation
        self.fade_out_animation.bonus_code_manager_fade_out_animation = self.bonus_code_manager.fade_out_animation
        self.fade_in_animation.map_switcher_fade_in_animation = self.map_switcher.fade_in_animation
        self.fade_out_animation.map_switcher_fade_out_animation = self.map_switcher.fade_out_animation
        for m in self.maps:
            self.fade_in_animation.map_fade_in_animations.append(m.fade_in_animation)
            self.fade_out_animation.map_fade_out_animations.append(m.fade_out_animation)

        self.child_controllers = [self.bonus_code_manager, self.map_switcher, *self.maps]

    @game_is_not_paused
    def on_update_time(self):
        super().on_update_time()
        if self.model.game_time % (FRAMES_IN_ONE_HOUR * 2) == 0:
            self.parent_controller.on_save_state()

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
        elif bonus_code_type == 'construction_time_bonus':
            self.on_activate_construction_time_bonus_code(
                self.bonus_code_manager.model.get_bonus_code_value(sha512_hash) - 1
            )

    def on_map_move_mode_available(self):
        self.maps[self.model.get_active_map()].on_map_move_mode_available()

    def on_map_move_mode_unavailable(self):
        self.maps[self.model.get_active_map()].on_map_move_mode_unavailable()

    def on_open_map_switcher(self):
        self.map_switcher.fade_in_animation.on_activate()
        self.maps[self.model.get_active_map()].on_open_map_switcher()

    def on_close_map_switcher(self):
        self.on_activate_map_switcher_button()
        self.maps[self.model.get_active_map()].on_close_map_switcher()

    @view_is_active
    def on_activate_map_switcher_button(self):
        self.view.open_map_switcher_button.on_activate(instant=True)

    def on_deactivate_map_switcher_button(self):
        self.view.open_map_switcher_button.on_deactivate(instant=True)
