from logging import getLogger

from view import *
from ui.button import create_two_state_button
from ui.button.open_settings_game_view_button import OpenSettingsGameViewButton
from ui.button.pause_game_button import PauseGameButton
from ui.button.resume_game_button import ResumeGameButton
from notifications.level_up_notification import LevelUpNotification
from notifications.enough_money_track_notification import EnoughMoneyTrackNotification
from notifications.enough_money_environment_notification import EnoughMoneyEnvironmentNotification
from i18n import I18N_RESOURCES
from ui.label.main_clock_label_24h import MainClockLabel24H
from ui.label.main_clock_label_12h import MainClockLabel12H
from ui.rectangle_progress_bar.exp_progress_bar import ExpProgressBar
from ui.rectangle_progress_bar.money_progress_bar import MoneyProgressBar
from ui.shader_sprite.game_view_shader_sprite import GameViewShaderSprite


@final
class GameView(View):
    def __init__(self):
        def on_pause_game(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate(instant=True)
            self.controller.on_pause_game()

        def on_resume_game(button):
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate(instant=True)
            self.controller.on_resume_game()

        def on_open_settings(button):
            button.on_deactivate()
            self.controller.parent_controller.on_open_settings_from_game()

        super().__init__(logger=getLogger('root.app.game.view'))
        USER_DB_CURSOR.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = USER_DB_CURSOR.fetchone()[0]
        self.exp_progress_bar = ExpProgressBar(parent_viewport=self.viewport)
        self.money_progress_bar = MoneyProgressBar(parent_viewport=self.viewport)
        self.pause_game_button, self.resume_game_button \
            = create_two_state_button(PauseGameButton(on_click_action=on_pause_game, parent_viewport=self.viewport),
                                      ResumeGameButton(on_click_action=on_resume_game, parent_viewport=self.viewport))
        self.open_settings_button = OpenSettingsGameViewButton(on_click_action=on_open_settings,
                                                               parent_viewport=self.viewport)
        self.buttons = [self.pause_game_button, self.resume_game_button, self.open_settings_button]
        self.main_clock_label_24h = MainClockLabel24H(parent_viewport=self.viewport)
        self.main_clock_label_12h = MainClockLabel12H(parent_viewport=self.viewport)
        self.exp_percent = 0
        self.money_percent = 0
        self.level = 0
        USER_DB_CURSOR.execute('''SELECT level_up_notification_enabled, enough_money_notification_enabled
                                  FROM notification_settings''')
        self.level_up_notification_enabled, self.enough_money_notification_enabled \
            = map(bool, USER_DB_CURSOR.fetchone())
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(USER_DB_CURSOR.fetchone()[0])
        self.shader_sprite = GameViewShaderSprite(view=self)
        USER_DB_CURSOR.execute('''SELECT level, exp, money, money_target FROM game_progress''')
        self.level, self.exp, self.money, self.money_target = USER_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute('''SELECT player_progress FROM player_progress_config 
                                    WHERE level = ?''', (self.level, ))
        self.player_progress = CONFIG_DB_CURSOR.fetchone()[0]

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        if self.clock_24h_enabled:
            self.main_clock_label_24h.on_update_args(
                ((self.game_time // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                 (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
            )
            self.main_clock_label_24h.create()
        else:
            self.main_clock_label_12h.on_update_args(
                ((self.game_time // FRAMES_IN_ONE_HOUR + 11) % 12 + 1,
                 (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
                 I18N_RESOURCES['am_pm_string'][self.current_locale][
                     ((self.game_time // FRAMES_IN_ONE_HOUR) // 12 + 1) % 2
                     ])
            )
            self.main_clock_label_12h.create()

        self.exp_progress_bar.on_update_text_label_args((self.level,))
        self.exp_progress_bar.on_activate()
        self.exp_progress_bar.on_update_progress_bar_state(self.exp, self.player_progress)
        self.money_progress_bar.on_update_text_label_args((int(self.money),))
        self.money_progress_bar.on_activate()
        self.money_progress_bar.on_update_progress_bar_state(self.money, self.money_target)

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.exp_progress_bar.on_deactivate()
        self.money_progress_bar.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = 0
        self.viewport.y1 = 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.exp_progress_bar.on_change_screen_resolution(self.screen_resolution)
        self.money_progress_bar.on_change_screen_resolution(self.screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.main_clock_label_24h.on_change_screen_resolution(self.screen_resolution)
        self.main_clock_label_12h.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.main_clock_label_24h.on_update_current_locale(self.current_locale)
        self.main_clock_label_12h.on_update_current_locale(self.current_locale)
        self.exp_progress_bar.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.exp_progress_bar.on_update_opacity(self.opacity)
        self.money_progress_bar.on_update_opacity(self.opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.main_clock_label_24h.on_update_opacity(self.opacity)
        self.main_clock_label_12h.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    @view_is_active
    def on_pause_game(self):
        pass

    @view_is_active
    def on_resume_game(self):
        pass

    def on_update_time(self):
        self.game_time += 1
        self.main_clock_label_24h.on_update_args(
            ((self.game_time // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
             (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
        )
        self.main_clock_label_12h.on_update_args(
            ((self.game_time // FRAMES_IN_ONE_HOUR + 11) % 12 + 1,
             (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
             I18N_RESOURCES['am_pm_string'][self.current_locale][
                 ((self.game_time // FRAMES_IN_ONE_HOUR) // 12 + 1) % 2
             ])
        )

    def on_update_exp(self, exp):
        self.exp = exp
        self.exp_progress_bar.on_update_progress_bar_state(self.exp, self.player_progress)

    def on_level_up(self):
        self.level += 1
        self.exp_progress_bar.on_update_text_label_args((self.level, ))
        CONFIG_DB_CURSOR.execute('''SELECT player_progress FROM player_progress_config 
                                    WHERE level = ?''', (self.level, ))
        self.player_progress = CONFIG_DB_CURSOR.fetchone()[0]

    def on_update_money(self, money):
        self.money = money
        self.money_progress_bar.on_update_text_label_args((int(self.money), ))
        self.money_progress_bar.on_update_progress_bar_state(self.money, self.money_target)

    def on_update_money_target(self, money_target):
        self.money_target = money_target
        self.money_progress_bar.on_update_progress_bar_state(self.money, self.money_target)

    @notifications_available
    @level_up_notification_enabled
    def on_send_level_up_notification(self):
        level_up_notification = LevelUpNotification()
        level_up_notification.send(self.current_locale, message_args=(self.level,))
        self.controller.parent_controller.on_append_notification(level_up_notification)

    @notifications_available
    @enough_money_notification_enabled
    def on_send_enough_money_track_notification(self):
        enough_money_track_notification = EnoughMoneyTrackNotification()
        enough_money_track_notification.send(self.current_locale)
        self.controller.parent_controller.on_append_notification(enough_money_track_notification)

    @notifications_available
    @enough_money_notification_enabled
    def on_send_enough_money_environment_notification(self):
        enough_money_environment_notification = EnoughMoneyEnvironmentNotification()
        enough_money_environment_notification.send(self.current_locale)
        self.controller.parent_controller.on_append_notification(enough_money_environment_notification)

    def on_change_level_up_notification_state(self, notification_state):
        self.level_up_notification_enabled = notification_state

    def on_change_enough_money_notification_state(self, notification_state):
        self.enough_money_notification_enabled = notification_state

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()

    def on_update_clock_state(self, clock_24h_enabled):
        self.clock_24h_enabled = clock_24h_enabled
        if self.clock_24h_enabled:
            self.main_clock_label_12h.delete()
            self.main_clock_label_24h.create()
        else:
            self.main_clock_label_24h.delete()
            self.main_clock_label_12h.create()
