from logging import getLogger

from model import *
from database import USER_DB_CURSOR, on_commit


@final
class SettingsModel(AppBaseModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, logger=getLogger('root.app.settings.model'))
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
            = (bool(t) for t in USER_DB_CURSOR.fetchone())

    def on_save_and_commit_state(self):
        USER_DB_CURSOR.execute('''UPDATE graphics SET app_width = ?, app_height = ?, display_fps = ?, 
                                  fade_animations_enabled = ?''',
                               (*self.windowed_resolution, int(self.display_fps), int(self.fade_animations_enabled)))
        USER_DB_CURSOR.execute('''UPDATE notification_settings SET level_up_notification_enabled = ?, 
                                  feature_unlocked_notification_enabled = ?, 
                                  construction_completed_notification_enabled = ?, 
                                  enough_money_notification_enabled = ?, bonus_expired_notification_enabled = ?,
                                  shop_storage_notification_enabled = ?''',
                               tuple(int(i) for i in (self.level_up_notification_enabled,
                                                      self.feature_unlocked_notification_enabled,
                                                      self.construction_completed_notification_enabled,
                                                      self.enough_money_notification_enabled,
                                                      self.bonus_expired_notification_enabled,
                                                      self.shop_storage_notification_enabled))
                               )
        USER_DB_CURSOR.execute('UPDATE i18n SET clock_24h = ?', (int(self.clock_24h_enabled), ))
        on_commit()

    def on_accept_changes(self, windowed_resolution, display_fps, fade_animations_enabled, clock_24h_enabled,
                          level_up_notification_enabled, feature_unlocked_notification_enabled,
                          construction_completed_notification_enabled, enough_money_notification_enabled,
                          bonus_expired_notification_enabled, shop_storage_notification_enabled):
        self.windowed_resolution = windowed_resolution
        self.display_fps = display_fps
        self.fade_animations_enabled = fade_animations_enabled
        self.clock_24h_enabled = clock_24h_enabled
        self.level_up_notification_enabled = level_up_notification_enabled
        self.feature_unlocked_notification_enabled = feature_unlocked_notification_enabled
        self.construction_completed_notification_enabled = construction_completed_notification_enabled
        self.enough_money_notification_enabled = enough_money_notification_enabled
        self.bonus_expired_notification_enabled = bonus_expired_notification_enabled
        self.shop_storage_notification_enabled = shop_storage_notification_enabled
