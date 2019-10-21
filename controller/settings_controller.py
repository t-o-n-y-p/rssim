from logging import getLogger

from controller import *


@final
class SettingsController(AppBaseController):
    def __init__(self, app):
        super().__init__(parent_controller=app, logger=getLogger('root.app.settings.controller'))
        self.navigated_from_main_menu = False
        self.navigated_from_game = False

    def on_accept_changes(self, windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
                          level_up_notification_enabled, feature_unlocked_notification_enabled,
                          construction_completed_notification_enabled, enough_money_notification_enabled,
                          bonus_expired_notification_enabled, shop_storage_notification_enabled):
        self.model.on_accept_changes(windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
                                     level_up_notification_enabled, feature_unlocked_notification_enabled,
                                     construction_completed_notification_enabled, enough_money_notification_enabled,
                                     bonus_expired_notification_enabled, shop_storage_notification_enabled)
