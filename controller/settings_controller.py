from logging import getLogger

from controller import *
from model.settings_model import SettingsModel
from view.settings_view import SettingsView
from ui.fade_animation.fade_in_animation.settings_fade_in_animation import SettingsFadeInAnimation
from ui.fade_animation.fade_out_animation.settings_fade_out_animation import SettingsFadeOutAnimation


@final
class SettingsController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.settings.controller'))
        self.navigated_from_main_menu = False
        self.navigated_from_game = False
        self.view = SettingsView(controller=self)
        self.model = SettingsModel(controller=self, view=self.view)
        self.fade_in_animation = SettingsFadeInAnimation(self.view)
        self.fade_out_animation = SettingsFadeOutAnimation(self.view)

    def on_accept_changes(self, windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
                          level_up_notification_enabled, feature_unlocked_notification_enabled,
                          construction_completed_notification_enabled, enough_money_notification_enabled,
                          bonus_expired_notification_enabled, shop_storage_notification_enabled):
        self.model.on_accept_changes(windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
                                     level_up_notification_enabled, feature_unlocked_notification_enabled,
                                     construction_completed_notification_enabled, enough_money_notification_enabled,
                                     bonus_expired_notification_enabled, shop_storage_notification_enabled)

    def on_save_and_commit_state(self):
        self.model.on_save_and_commit_state()
