from logging import getLogger

from model import *
from ui import SURFACE


class SettingsModel(Model):
    """
    Implements Settings model.
    Settings object is responsible for user-defined settings.
    """
    def __init__(self):
        """
        Properties:
            display_fps                         indicates if FPS value is displayed in game
            windowed_resolution                 screen resolution in windowed mode
            fade_animations_enabled             indicates if fade animations are turned on
            clock_24h_enabled                   indicates if 24h clock is enabled
            level_up_notification_enabled
                                indicates if level up notifications are enabled by user in game settings
            feature_unlocked_notification_enabled
                                indicates if feature unlocked notifications are enabled by user in game settings
            construction_completed_notification_enabled
                                indicates if construction completed notifications are enabled by user in game settings
            enough_money_notification_enabled
                                indicates if enough money notifications are enabled by user in game settings

        """
        super().__init__(logger=getLogger('root.app.settings.model'))
        self.user_db_cursor.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT display_fps, fade_animations_enabled FROM graphics')
        self.display_fps, self.fade_animations_enabled = tuple(map(bool, self.user_db_cursor.fetchone()))
        self.user_db_cursor.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(self.user_db_cursor.fetchone()[0])
        self.user_db_cursor.execute('SELECT * FROM notification_settings')
        self.level_up_notification_enabled, self.feature_unlocked_notification_enabled, \
            self.construction_completed_notification_enabled, self.enough_money_notification_enabled \
            = tuple(map(bool, self.user_db_cursor.fetchone()))

    def on_activate_view(self):
        """
        Activates the Settings view, updates temp values for fade animations, windowed resolution
        and updates available windowed resolutions.
        """
        self.view.temp_display_fps = self.display_fps
        self.view.temp_fade_animations_enabled = self.fade_animations_enabled
        self.view.temp_clock_24h_enabled = self.clock_24h_enabled
        self.view.on_change_temp_windowed_resolution(self.windowed_resolution)
        self.view.temp_level_up_notification_enabled = self.level_up_notification_enabled
        self.view.temp_feature_unlocked_notification_enabled = self.feature_unlocked_notification_enabled
        self.view.temp_construction_completed_notification_enabled = self.construction_completed_notification_enabled
        self.view.temp_enough_money_notification_enabled = self.enough_money_notification_enabled
        self.view.on_activate()

    def on_save_and_commit_state(self):
        """
        Notifies the app controller about user-defined settings update.
        Saves user-defined settings to user progress database and makes commit.
        """
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
        self.controller.parent_controller.on_change_level_up_notification_state(self.level_up_notification_enabled)
        self.controller.parent_controller\
            .on_change_feature_unlocked_notification_state(self.feature_unlocked_notification_enabled)
        self.controller.parent_controller\
            .on_change_construction_completed_notification_state(self.construction_completed_notification_enabled)
        self.controller.parent_controller\
            .on_change_enough_money_notification_state(self.enough_money_notification_enabled)

        self.user_db_cursor.execute('''UPDATE graphics SET app_width = ?, app_height = ?, display_fps = ?, 
                                       fade_animations_enabled = ?''',
                                    (self.windowed_resolution[0], self.windowed_resolution[1], int(self.display_fps),
                                     int(self.fade_animations_enabled)))
        self.user_db_cursor.execute('''UPDATE notification_settings SET level_up_notification_enabled = ?, 
                                       feature_unlocked_notification_enabled = ?, 
                                       construction_completed_notification_enabled = ?, 
                                       enough_money_notification_enabled = ?''',
                                    tuple(map(int, (self.level_up_notification_enabled,
                                                    self.feature_unlocked_notification_enabled,
                                                    self.construction_completed_notification_enabled,
                                                    self.enough_money_notification_enabled))))
        self.user_db_cursor.execute('UPDATE i18n SET clock_24h = ?', (int(self.clock_24h_enabled), ))
        self.user_db_connection.commit()

    def on_update_clock_state(self, clock_24h_enabled):
        """
        Updates clock state.

        :param clock_24h_enabled:               indicates if 24h clock is enabled
        """
        self.clock_24h_enabled = clock_24h_enabled
