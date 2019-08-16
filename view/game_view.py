from logging import getLogger
from ctypes import windll

from pyglet.resource import add_font

from database import CONFIG_DB_CURSOR
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
from ui.label.money_bonus_value_percent_label import MoneyBonusValuePercentLabel
from ui.label.exp_bonus_value_percent_label import ExpBonusValuePercentLabel
from ui.label.exp_bonus_placeholder_label import ExpBonusPlaceholderLabel
from ui.label.money_bonus_placeholder_label import MoneyBonusPlaceholderLabel
from notifications.exp_bonus_expired_notification import ExpBonusExpiredNotification
from notifications.money_bonus_expired_notification import MoneyBonusExpiredNotification


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
            self.controller.parent_controller.settings_to_game_transition_animation.on_deactivate()
            self.controller.parent_controller.game_to_settings_transition_animation.on_activate()
            self.controller.parent_controller.settings.navigated_from_game = True

        super().__init__(logger=getLogger('root.app.game.view'))
        self.exp_progress_bar = ExpProgressBar(parent_viewport=self.viewport)
        self.money_progress_bar = MoneyProgressBar(parent_viewport=self.viewport)
        self.pause_game_button, self.resume_game_button \
            = create_two_state_button(PauseGameButton(on_click_action=on_pause_game, parent_viewport=self.viewport),
                                      ResumeGameButton(on_click_action=on_resume_game, parent_viewport=self.viewport))
        self.open_settings_button = OpenSettingsGameViewButton(on_click_action=on_open_settings,
                                                               parent_viewport=self.viewport)
        self.buttons = [self.pause_game_button, self.resume_game_button, self.open_settings_button]
        add_font('perfo-bold.ttf')
        self.main_clock_label_24h = MainClockLabel24H(parent_viewport=self.viewport)
        self.main_clock_label_12h = MainClockLabel12H(parent_viewport=self.viewport)
        self.game_time = 0
        self.exp_percent = 0
        self.money_percent = 0
        self.level = 0
        USER_DB_CURSOR.execute('''SELECT level_up_notification_enabled, enough_money_notification_enabled,
                                  bonus_expired_notification_enabled FROM notification_settings''')
        self.level_up_notification_enabled, self.enough_money_notification_enabled, \
            self.bonus_expired_notification_enabled = map(bool, USER_DB_CURSOR.fetchone())
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(USER_DB_CURSOR.fetchone()[0])
        self.shader_sprite = GameViewShaderSprite(view=self)
        USER_DB_CURSOR.execute('SELECT exp_bonus_multiplier, money_bonus_multiplier FROM game_progress')
        self.exp_bonus_multiplier, self.money_bonus_multiplier = USER_DB_CURSOR.fetchone()
        self.exp_bonus_percent_label = ExpBonusValuePercentLabel(parent_viewport=self.viewport)
        self.money_bonus_percent_label = MoneyBonusValuePercentLabel(parent_viewport=self.viewport)
        self.exp_bonus_placeholder_label = ExpBonusPlaceholderLabel(parent_viewport=self.viewport)
        self.money_bonus_placeholder_label = MoneyBonusPlaceholderLabel(parent_viewport=self.viewport)

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.shader_sprite.create()
        if self.clock_24h_enabled:
            self.main_clock_label_24h.create()
        else:
            self.main_clock_label_12h.create()

        self.exp_progress_bar.on_activate()
        self.money_progress_bar.on_activate()
        if self.exp_bonus_multiplier > 1.0:
            self.exp_bonus_placeholder_label.delete()
            self.exp_bonus_percent_label.on_update_args((round(self.exp_bonus_multiplier * 100 - 100), ))
            self.exp_bonus_percent_label.create()
        else:
            self.exp_bonus_percent_label.delete()
            self.exp_bonus_placeholder_label.create()

        if self.money_bonus_multiplier > 1.0:
            self.money_bonus_placeholder_label.delete()
            self.money_bonus_percent_label.on_update_args((round(self.money_bonus_multiplier * 100 - 100), ))
            self.money_bonus_percent_label.create()
        else:
            self.money_bonus_percent_label.delete()
            self.money_bonus_placeholder_label.create()

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.exp_progress_bar.on_deactivate()
        self.money_progress_bar.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

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
        self.exp_bonus_percent_label.on_change_screen_resolution(self.screen_resolution)
        self.money_bonus_percent_label.on_change_screen_resolution(self.screen_resolution)
        self.exp_bonus_placeholder_label.on_change_screen_resolution(self.screen_resolution)
        self.money_bonus_placeholder_label.on_change_screen_resolution(self.screen_resolution)
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
        self.exp_bonus_percent_label.on_update_opacity(self.opacity)
        self.money_bonus_percent_label.on_update_opacity(self.opacity)
        self.exp_bonus_placeholder_label.on_update_opacity(self.opacity)
        self.money_bonus_placeholder_label.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    @view_is_active
    def on_pause_game(self):
        pass

    @view_is_active
    def on_resume_game(self):
        pass

    def on_update_time(self, game_time):
        self.game_time = game_time
        am_pm_index = ((self.game_time // FRAMES_IN_ONE_HOUR) // 12 + 1) % 2
        self.main_clock_label_24h.on_update_args(
            ((self.game_time // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
             (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
        )
        self.main_clock_label_12h.on_update_args(
            ((self.game_time // FRAMES_IN_ONE_HOUR + 11) % 12 + 1,
             (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
             I18N_RESOURCES['am_pm_string'][self.current_locale][am_pm_index])
        )

    @view_is_active
    def on_update_exp(self, exp, player_progress):
        self.exp_progress_bar.on_update_progress_bar_state(exp, player_progress)

    @view_is_active
    def on_update_level(self, level):
        self.level = level
        self.exp_progress_bar.on_update_text_label_args((self.level, ))

    @view_is_active
    def on_update_money(self, money, money_target):
        self.money_progress_bar.on_update_text_label_args((int(money), ))
        self.money_progress_bar.on_update_progress_bar_state(money, money_target)

    @notifications_available
    @level_up_notification_enabled
    def on_send_level_up_notification(self, level):
        level_up_notification = LevelUpNotification()
        level_up_notification.send(self.current_locale, message_args=(level,))
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

    @notifications_available
    @bonus_expired_notification_enabled
    def on_send_exp_bonus_expired_notification(self):
        exp_bonus_expired_notification = ExpBonusExpiredNotification()
        exp_bonus_expired_notification.send(self.current_locale)
        self.controller.parent_controller.on_append_notification(exp_bonus_expired_notification)

    @notifications_available
    @bonus_expired_notification_enabled
    def on_send_money_bonus_expired_notification(self):
        money_bonus_expired_notification = MoneyBonusExpiredNotification()
        money_bonus_expired_notification.send(self.current_locale)
        self.controller.parent_controller.on_append_notification(money_bonus_expired_notification)

    def on_change_level_up_notification_state(self, notification_state):
        self.level_up_notification_enabled = notification_state

    def on_change_enough_money_notification_state(self, notification_state):
        self.enough_money_notification_enabled = notification_state

    def on_change_bonus_expired_notification_state(self, notification_state):
        self.bonus_expired_notification_enabled = notification_state

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

    def on_activate_exp_bonus_code(self, value):
        self.exp_bonus_multiplier = round(1.0 + value, 2)
        if self.is_activated:
            self.exp_bonus_placeholder_label.delete()
            self.exp_bonus_percent_label.on_update_args((round(self.exp_bonus_multiplier * 100 - 100), ))
            self.exp_bonus_percent_label.create()

    def on_deactivate_exp_bonus_code(self):
        self.exp_bonus_multiplier = 1.0
        if self.is_activated:
            self.exp_bonus_percent_label.delete()
            self.exp_bonus_placeholder_label.create()

    def on_activate_money_bonus_code(self, value):
        self.money_bonus_multiplier = round(1.0 + value, 2)
        if self.is_activated:
            self.money_bonus_placeholder_label.delete()
            self.money_bonus_percent_label.on_update_args((round(self.money_bonus_multiplier * 100 - 100), ))
            self.money_bonus_percent_label.create()

    def on_deactivate_money_bonus_code(self):
        self.money_bonus_multiplier = 1.0
        if self.is_activated:
            self.money_bonus_percent_label.delete()
            self.money_bonus_placeholder_label.create()
