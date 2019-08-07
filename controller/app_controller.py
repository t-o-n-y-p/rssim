from sys import exit
from logging import getLogger

from controller import *


class AppController(Controller):
    def __init__(self, loader):
        super().__init__(logger=getLogger('root.app.controller'))
        self.loader = loader
        self.main_menu = None
        self.onboarding = None
        self.license = None
        self.game = None
        self.settings = None
        self.fps = None
        self.main_menu_to_game_transition_animation = None
        self.main_menu_to_onboarding_transition_animation = None
        self.game_to_main_menu_transition_animation = None
        self.main_menu_to_license_transition_animation = None
        self.license_to_main_menu_transition_animation = None
        self.game_to_settings_transition_animation = None
        self.settings_to_game_transition_animation = None
        self.onboarding_to_game_transition_animation = None
        self.main_menu_to_settings_transition_animation = None
        self.settings_to_main_menu_transition_animation = None

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()
        self.license.on_update_view()
        self.main_menu.on_update_view()
        self.onboarding.on_update_view()
        self.game.on_update_view()
        self.settings.on_update_view()
        self.fps.on_update_view()

    def on_activate_view(self):
        self.model.on_activate_view()
        self.main_menu.on_activate_view()
        self.fps.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.main_menu.on_deactivate_view()
        self.onboarding.on_deactivate_view()
        self.license.on_deactivate_view()
        self.game.on_deactivate_view()
        self.settings.on_deactivate_view()
        self.fps.on_deactivate_view()

    def on_fullscreen_button_click(self):
        self.on_change_screen_resolution(self.model.fullscreen_resolution)
        if self.model.fullscreen_mode_available:
            self.on_fullscreen_mode_turned_on()

    def on_restore_button_click(self):
        self.on_fullscreen_mode_turned_off()
        self.on_change_screen_resolution(self.settings.model.windowed_resolution)

    def on_fullscreen_mode_turned_on(self):
        self.model.on_fullscreen_mode_turned_on()

    def on_fullscreen_mode_turned_off(self):
        self.model.on_fullscreen_mode_turned_off()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        self.main_menu.on_change_screen_resolution(screen_resolution)
        self.onboarding.on_change_screen_resolution(screen_resolution)
        self.license.on_change_screen_resolution(screen_resolution)
        self.game.on_change_screen_resolution(screen_resolution)
        self.settings.on_change_screen_resolution(screen_resolution)
        self.fps.on_change_screen_resolution(screen_resolution)

    def on_close_game(self):
        self.on_deactivate_view()
        self.game.on_save_and_commit_state()
        exit()

    def on_activate_main_menu_view(self):
        self.main_menu.on_activate_view()

    def on_activate_game_view(self):
        self.game.on_activate_view()

    def on_update_fps(self, fps):
        self.fps.on_update_fps(fps)

    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()
        self.main_menu.on_apply_shaders_and_draw_vertices()
        self.onboarding.on_apply_shaders_and_draw_vertices()
        self.license.on_apply_shaders_and_draw_vertices()
        self.settings.on_apply_shaders_and_draw_vertices()
        self.game.on_apply_shaders_and_draw_vertices()

    def on_update_current_locale(self, new_locale):
        self.model.on_save_and_commit_locale(new_locale)
        self.view.on_update_current_locale(new_locale)
        self.main_menu.on_update_current_locale(new_locale)
        self.onboarding.on_update_current_locale(new_locale)
        self.license.on_update_current_locale(new_locale)
        self.game.on_update_current_locale(new_locale)
        self.settings.on_update_current_locale(new_locale)
        self.fps.on_update_current_locale(new_locale)

    def on_update_clock_state(self, clock_24h_enabled):
        self.model.on_save_and_commit_clock_state(clock_24h_enabled)
        self.game.on_update_clock_state(clock_24h_enabled)
        self.settings.on_update_clock_state(clock_24h_enabled)

    def on_disable_notifications(self):
        self.view.on_disable_notifications()
        self.game.on_disable_notifications()
        self.settings.on_disable_notifications()
        self.fps.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()
        self.game.on_enable_notifications()
        self.settings.on_enable_notifications()
        self.fps.on_enable_notifications()

    def on_append_notification(self, notification):
        self.loader.notifications.append(notification)

    def on_change_level_up_notification_state(self, notification_state):
        self.game.on_change_level_up_notification_state(notification_state)

    def on_change_feature_unlocked_notification_state(self, notification_state):
        self.game.on_change_feature_unlocked_notification_state(notification_state)

    def on_change_construction_completed_notification_state(self, notification_state):
        self.game.on_change_construction_completed_notification_state(notification_state)

    def on_change_enough_money_notification_state(self, notification_state):
        self.game.on_change_enough_money_notification_state(notification_state)

    def on_resume_game(self):
        self.game.on_resume_game()

    def on_open_license(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_license_transition_animation.on_activate()

    def on_close_license(self):
        self.main_menu_to_license_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_activate()

    def on_open_onboarding(self):
        self.game_to_main_menu_transition_animation.on_deactivate()
        self.license_to_main_menu_transition_animation.on_deactivate()
        self.main_menu_to_onboarding_transition_animation.on_activate()

    def on_close_onboarding(self):
        self.settings_to_game_transition_animation.on_deactivate()
        self.main_menu_to_game_transition_animation.on_deactivate()
        self.onboarding_to_game_transition_animation.on_activate()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        self.main_menu.on_update_fade_animation_state(new_state)
        self.onboarding.on_update_fade_animation_state(new_state)
        self.license.on_update_fade_animation_state(new_state)
        self.game.on_update_fade_animation_state(new_state)
        self.settings.on_update_fade_animation_state(new_state)
        self.fps.on_update_fade_animation_state(new_state)
