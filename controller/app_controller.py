from logging import getLogger
from typing import final

from controller import AppBaseController
from database import on_commit, PASSENGER_MAP
from ui import WINDOW
from model.app_model import AppModel
from view.app_view import AppView
from ui.fade_animation.fade_in_animation.app_fade_in_animation import AppFadeInAnimation
from ui.fade_animation.fade_out_animation.app_fade_out_animation import AppFadeOutAnimation
from ui.transition_animation import TransitionAnimation
from controller.main_menu_controller import MainMenuController
from controller.license_controller import LicenseController
from controller.onboarding_controller import OnboardingController
from controller.bonus_code_activation_controller import BonusCodeActivationController
from controller.settings_controller import SettingsController
from controller.game_controller import GameController


@final
class AppController(AppBaseController):
    def __init__(self, loader):
        super().__init__(logger=getLogger('root.app.controller'))
        self.loader = loader
        self.view = AppView(controller=self)
        self.model = AppModel(controller=self, view=self.view)
        self.fade_in_animation = AppFadeInAnimation(self.view)
        self.fade_out_animation = AppFadeOutAnimation(self.view)
        self.main_menu = MainMenuController(self)
        self.onboarding = OnboardingController(self)
        self.license = LicenseController(self)
        self.game = GameController(self)
        self.settings = SettingsController(self)
        self.bonus_code_activation = BonusCodeActivationController(self)
        self.main_menu_to_game_transition_animation = TransitionAnimation(
            fade_out_animation=self.main_menu.fade_out_animation, fade_in_animation=self.game.fade_in_animation
        )
        self.main_menu_to_onboarding_transition_animation = TransitionAnimation(
            fade_out_animation=self.main_menu.fade_out_animation, fade_in_animation=self.onboarding.fade_in_animation
        )
        self.game_to_main_menu_transition_animation = TransitionAnimation(
            fade_out_animation=self.game.fade_out_animation, fade_in_animation=self.main_menu.fade_in_animation
        )
        self.main_menu_to_license_transition_animation = TransitionAnimation(
            fade_out_animation=self.main_menu.fade_out_animation, fade_in_animation=self.license.fade_in_animation
        )
        self.license_to_main_menu_transition_animation = TransitionAnimation(
            fade_out_animation=self.license.fade_out_animation, fade_in_animation=self.main_menu.fade_in_animation
        )
        self.game_to_settings_transition_animation = TransitionAnimation(
            fade_out_animation=self.game.fade_out_animation, fade_in_animation=self.settings.fade_in_animation
        )
        self.settings_to_game_transition_animation = TransitionAnimation(
            fade_out_animation=self.settings.fade_out_animation, fade_in_animation=self.game.fade_in_animation
        )
        self.onboarding_to_game_transition_animation = TransitionAnimation(
            fade_out_animation=self.onboarding.fade_out_animation, fade_in_animation=self.game.fade_in_animation
        )
        self.main_menu_to_settings_transition_animation = TransitionAnimation(
            fade_out_animation=self.main_menu.fade_out_animation, fade_in_animation=self.settings.fade_in_animation
        )
        self.settings_to_main_menu_transition_animation = TransitionAnimation(
            fade_out_animation=self.settings.fade_out_animation, fade_in_animation=self.main_menu.fade_in_animation
        )
        self.main_menu_to_bonus_code_activation_transition_animation = TransitionAnimation(
            fade_out_animation=self.main_menu.fade_out_animation,
            fade_in_animation=self.bonus_code_activation.fade_in_animation
        )
        self.bonus_code_activation_to_main_menu_transition_animation = TransitionAnimation(
            fade_out_animation=self.bonus_code_activation.fade_out_animation,
            fade_in_animation=self.main_menu.fade_in_animation
        )
        self.fade_in_animation.main_menu_fade_in_animation = self.main_menu.fade_in_animation
        self.fade_in_animation.license_fade_in_animation = self.license.fade_in_animation
        self.fade_in_animation.onboarding_fade_in_animation = self.onboarding.fade_in_animation
        self.fade_in_animation.game_fade_in_animation = self.game.fade_in_animation
        self.fade_in_animation.settings_fade_in_animation = self.settings.fade_in_animation
        self.fade_in_animation.bonus_code_activation_fade_in_animation = self.bonus_code_activation.fade_in_animation
        self.fade_out_animation.main_menu_fade_out_animation = self.main_menu.fade_out_animation
        self.fade_out_animation.license_fade_out_animation = self.license.fade_out_animation
        self.fade_out_animation.onboarding_fade_out_animation = self.onboarding.fade_out_animation
        self.fade_out_animation.game_fade_out_animation = self.game.fade_out_animation
        self.fade_out_animation.settings_fade_out_animation = self.settings.fade_out_animation
        self.fade_out_animation.bonus_code_activation_fade_out_animation = self.bonus_code_activation.fade_out_animation
        self.child_controllers = [
            self.main_menu, self.onboarding, self.license, self.game,
            self.settings, self.bonus_code_activation
        ]

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.model.on_save_and_commit_locale(new_locale)

    def on_save_state(self):
        super().on_save_state()
        on_commit()

    def on_update_clock_state(self, clock_24h_enabled):
        super().on_update_clock_state(clock_24h_enabled)
        self.model.on_save_and_commit_clock_state(clock_24h_enabled)

    def on_fullscreen_button_click(self):
        WINDOW.set_size(*self.model.fullscreen_resolution)
        if self.model.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_on()

    def on_restore_button_click(self):
        self.on_fullscreen_mode_turned_off()
        WINDOW.set_size(*self.settings.model.windowed_resolution)

    def on_fullscreen_mode_turned_on(self):
        self.model.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.model.on_fullscreen_mode_turned_off()

    def on_activate_main_menu_view(self):
        self.main_menu.on_activate_view()

    def on_activate_game_view(self):
        self.game.on_activate_view()

    def on_open_license(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.settings_to_main_menu_transition_animation.on_deactivate()
        self.bonus_code_activation_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_license_transition_animation.on_activate()

    def on_close_license(self):
        self.main_menu_to_license_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_activate()

    def on_open_onboarding(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.settings_to_main_menu_transition_animation.on_deactivate()
        self.bonus_code_activation_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_onboarding_transition_animation.on_activate()

    def on_close_onboarding(self):
        self.game.on_unlock_map(PASSENGER_MAP)
        self.main_menu_to_onboarding_transition_animation.on_deactivate()
        self.onboarding_to_game_transition_animation.on_activate()
        self.onboarding.on_save_and_commit_onboarding_state()
        self.game.on_resume_game()

    def on_back_to_the_station(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.settings_to_main_menu_transition_animation.on_deactivate()
        self.bonus_code_activation_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_game_transition_animation.on_activate()
        self.game.on_resume_game()

    def on_open_bonus_code(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.settings_to_main_menu_transition_animation.on_deactivate()
        self.bonus_code_activation_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_bonus_code_activation_transition_animation.on_activate()

    def on_close_bonus_code(self):
        self.main_menu_to_bonus_code_activation_transition_animation.on_deactivate()
        self.bonus_code_activation_to_main_menu_transition_animation.on_activate()

    def on_open_settings_from_main_menu(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.settings_to_main_menu_transition_animation.on_deactivate()
        self.bonus_code_activation_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_settings_transition_animation.on_activate()
        self.settings.navigated_from_main_menu = True

    def on_open_settings_from_game(self):
        self.main_menu_to_game_transition_animation.on_deactivate()
        self.settings_to_game_transition_animation.on_deactivate()
        self.onboarding_to_game_transition_animation.on_deactivate()
        self.game_to_settings_transition_animation.on_activate()
        self.settings.navigated_from_game = True

    def on_close_settings(self):
        if self.settings.navigated_from_main_menu:
            self.settings.navigated_from_main_menu = False
            self.main_menu_to_settings_transition_animation.on_deactivate()
            self.settings_to_main_menu_transition_animation.on_activate()
        elif self.settings.navigated_from_game:
            self.settings.navigated_from_game = False
            self.game_to_settings_transition_animation.on_deactivate()
            self.settings_to_game_transition_animation.on_activate()

    def on_activate_new_bonus_code(self, sha512_hash):
        self.game.on_activate_new_bonus_code(sha512_hash)

    def on_accept_changes(
            self, windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
            level_up_notification_enabled, feature_unlocked_notification_enabled,
            construction_completed_notification_enabled, enough_money_notification_enabled,
            bonus_expired_notification_enabled, shop_storage_notification_enabled,
            voice_not_found_notification_enabled, master_volume, announcements_enabled
    ):
        self.settings.on_accept_changes(
            windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
            level_up_notification_enabled, feature_unlocked_notification_enabled,
            construction_completed_notification_enabled, enough_money_notification_enabled,
            bonus_expired_notification_enabled, shop_storage_notification_enabled,
            voice_not_found_notification_enabled, master_volume, announcements_enabled
        )
        self.on_update_fade_animation_state(fade_animations_enabled)
        self.on_update_clock_state(clock_24h_enabled)
        self.on_change_level_up_notification_state(level_up_notification_enabled)
        self.on_change_feature_unlocked_notification_state(feature_unlocked_notification_enabled)
        self.on_change_construction_completed_notification_state(construction_completed_notification_enabled)
        self.on_change_enough_money_notification_state(enough_money_notification_enabled)
        self.on_change_bonus_expired_notification_state(bonus_expired_notification_enabled)
        self.on_change_shop_storage_notification_state(shop_storage_notification_enabled)
        self.on_change_voice_not_found_notification_state(voice_not_found_notification_enabled)
        self.on_master_volume_update(master_volume)
        self.on_update_announcements_state(announcements_enabled)
        if not WINDOW.fullscreen:
            WINDOW.set_size(*windowed_resolution)

        if display_fps:
            self.view.fps_display.on_activate()
        else:
            self.view.fps_display.on_deactivate()

    def on_save_and_commit_bonus_code_abuse(self):
        self.model.on_save_and_commit_bonus_code_abuse()

    def on_master_volume_update(self, new_master_volume):
        self.game.on_master_volume_update(new_master_volume)

    def on_update_announcements_state(self, new_state):
        self.game.on_update_announcements_state(new_state)
