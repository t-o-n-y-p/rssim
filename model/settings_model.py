from logging import getLogger

from model import *
from ui import SURFACE
from database import USER_DB_CURSOR, on_commit


class SettingsModel(Model):
    def __init__(self):
        super().__init__(logger=getLogger('root.app.settings.model'))
        USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('SELECT display_fps, fade_animations_enabled FROM graphics')
        self.display_fps, self.fade_animations_enabled = tuple(map(bool, USER_DB_CURSOR.fetchone()))
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(USER_DB_CURSOR.fetchone()[0])
        USER_DB_CURSOR.execute('SELECT * FROM notification_settings')
        self.level_up_notification_enabled, self.feature_unlocked_notification_enabled, \
            self.construction_completed_notification_enabled, self.enough_money_notification_enabled, \
            self.bonus_expired_notification_enabled, self.shop_storage_notification_enabled \
            = tuple(map(bool, USER_DB_CURSOR.fetchone()))

    def on_activate_view(self):
        self.view.temp_display_fps = self.display_fps
        self.view.temp_fade_animations_enabled = self.fade_animations_enabled
        self.view.temp_clock_24h_enabled = self.clock_24h_enabled
        self.view.on_change_temp_windowed_resolution(self.windowed_resolution)
        self.view.temp_level_up_notification_enabled = self.level_up_notification_enabled
        self.view.temp_feature_unlocked_notification_enabled = self.feature_unlocked_notification_enabled
        self.view.temp_construction_completed_notification_enabled = self.construction_completed_notification_enabled
        self.view.temp_enough_money_notification_enabled = self.enough_money_notification_enabled
        self.view.temp_bonus_expired_notification_enabled = self.bonus_expired_notification_enabled
        self.view.temp_shop_storage_notification_enabled = self.shop_storage_notification_enabled
        self.view.on_activate()

    def on_save_and_commit_state(self):
        self.display_fps = self.view.temp_display_fps
        self.controller.parent_controller.fps.on_update_display_fps(self.display_fps)
        self.fade_animations_enabled = self.view.temp_fade_animations_enabled
        self.controller.parent_controller.on_update_fade_animation_state(self.fade_animations_enabled)
        # clock_24h_enabled property is not updated straight away
        # because on_update_clock_state() method is called by settings controller via app controller
        self.controller.parent_controller.on_update_clock_state(self.view.temp_clock_24h_enabled)
        self.windowed_resolution = self.view.temp_windowed_resolution
        if not SURFACE.fullscreen:
            self.controller.parent_controller.on_change_screen_resolution(self.windowed_resolution)

        self.level_up_notification_enabled = self.view.temp_level_up_notification_enabled
        self.feature_unlocked_notification_enabled = self.view.temp_feature_unlocked_notification_enabled
        self.construction_completed_notification_enabled = self.view.temp_construction_completed_notification_enabled
        self.enough_money_notification_enabled = self.view.temp_enough_money_notification_enabled
        self.bonus_expired_notification_enabled = self.view.temp_bonus_expired_notification_enabled
        self.shop_storage_notification_enabled = self.view.temp_shop_storage_notification_enabled
        self.controller.parent_controller.on_change_level_up_notification_state(self.level_up_notification_enabled)
        self.controller.parent_controller\
            .on_change_feature_unlocked_notification_state(self.feature_unlocked_notification_enabled)
        self.controller.parent_controller\
            .on_change_construction_completed_notification_state(self.construction_completed_notification_enabled)
        self.controller.parent_controller\
            .on_change_enough_money_notification_state(self.enough_money_notification_enabled)
        self.controller.parent_controller\
            .on_change_bonus_expired_notification_state(self.bonus_expired_notification_enabled)
        self.controller.parent_controller\
            .on_change_shop_storage_notification_state(self.shop_storage_notification_enabled)
        USER_DB_CURSOR.execute('''UPDATE graphics SET app_width = ?, app_height = ?, display_fps = ?, 
                                  fade_animations_enabled = ?''',
                               (*self.windowed_resolution, int(self.display_fps), int(self.fade_animations_enabled)))
        USER_DB_CURSOR.execute('''UPDATE notification_settings SET level_up_notification_enabled = ?, 
                                  feature_unlocked_notification_enabled = ?, 
                                  construction_completed_notification_enabled = ?, 
                                  enough_money_notification_enabled = ?, bonus_expired_notification_enabled = ?,
                                  shop_storage_notification_enabled = ?''',
                               tuple(map(int, (self.level_up_notification_enabled,
                                               self.feature_unlocked_notification_enabled,
                                               self.construction_completed_notification_enabled,
                                               self.enough_money_notification_enabled,
                                               self.bonus_expired_notification_enabled,
                                               self.shop_storage_notification_enabled))))
        USER_DB_CURSOR.execute('UPDATE i18n SET clock_24h = ?', (int(self.clock_24h_enabled), ))
        on_commit()

    def on_apply_clock_state(self, clock_24h_enabled):
        self.clock_24h_enabled = clock_24h_enabled
