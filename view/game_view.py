from logging import getLogger

from ui.knob.time_speed_knob import TimeSpeedKnob
from view import *
from ui.button.open_settings_game_view_button import OpenSettingsGameViewButton
from ui.button.open_map_switcher_button import OpenMapSwitcherButton
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
class GameView(GameBaseView):
    def __init__(self, controller):
        def on_open_settings(button):
            button.on_deactivate()
            self.controller.parent_controller.on_open_settings_from_game()

        def on_open_map_switcher(button):
            button.on_deactivate(instant=True)
            button.state = 'normal'
            self.controller.on_open_map_switcher()

        def on_leave_action():
            self.controller.on_map_move_mode_available()

        def on_hover_action():
            self.controller.on_map_move_mode_unavailable()

        super().__init__(controller, logger=getLogger('root.app.game.view'))
        self.game_paused = True
        self.exp_progress_bar = ExpProgressBar(parent_viewport=self.viewport)
        self.money_progress_bar = MoneyProgressBar(parent_viewport=self.viewport)
        self.open_settings_button = OpenSettingsGameViewButton(on_click_action=on_open_settings,
                                                               parent_viewport=self.viewport)
        self.open_map_switcher_button = OpenMapSwitcherButton(on_click_action=on_open_map_switcher,
                                                              on_hover_action=on_hover_action,
                                                              on_leave_action=on_leave_action,
                                                              parent_viewport=self.viewport)
        self.buttons = [self.open_settings_button, self.open_map_switcher_button]
        self.main_clock_label_24h = MainClockLabel24H(parent_viewport=self.viewport)
        self.main_clock_label_12h = MainClockLabel12H(parent_viewport=self.viewport)
        self.exp_percent = 0
        self.money_percent = 0
        self.shader_sprite = GameViewShaderSprite(view=self)
        self.time_speed_knob = TimeSpeedKnob(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend([
            *self.exp_progress_bar.on_window_resize_handlers, *self.money_progress_bar.on_window_resize_handlers,
            self.main_clock_label_24h.on_window_resize, self.main_clock_label_12h.on_window_resize,
            self.shader_sprite.on_window_resize, *self.time_speed_knob.on_window_resize_handlers
        ])
        self.on_append_window_handlers()
        USER_DB_CURSOR.execute('''SELECT exp, money_target FROM game_progress''')
        self.exp, self.money_target = USER_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute('''SELECT player_progress FROM player_progress_config 
                                    WHERE level = ?''', (self.level, ))
        self.player_progress = CONFIG_DB_CURSOR.fetchone()[0]

    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.main_clock_label_24h.on_update_args(
            ((self.game_time // SECONDS_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
             (self.game_time // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
        )
        self.main_clock_label_12h.on_update_args(
            ((self.game_time // SECONDS_IN_ONE_HOUR + 11) % 12 + 1,
             (self.game_time // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
             I18N_RESOURCES['am_pm_string'][self.current_locale][
                 ((self.game_time // SECONDS_IN_ONE_HOUR) // 12 + 1) % 2
             ])
        )
        if self.clock_24h_enabled:
            self.main_clock_label_24h.create()
        else:
            self.main_clock_label_12h.create()

        self.exp_progress_bar.on_update_text_label_args((self.level,))
        self.exp_progress_bar.on_activate()
        self.exp_progress_bar.on_update_progress_bar_state(self.exp, self.player_progress)
        self.money_progress_bar.on_update_text_label_args((int(self.money),))
        self.money_progress_bar.on_activate()
        self.money_progress_bar.on_update_progress_bar_state(self.money, self.money_target)
        self.time_speed_knob.on_activate()

    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.exp_progress_bar.on_deactivate()
        self.money_progress_bar.on_deactivate()
        self.time_speed_knob.on_deactivate()

    @view_is_active
    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.main_clock_label_24h.on_update_current_locale(self.current_locale)
        self.main_clock_label_12h.on_update_current_locale(self.current_locale)
        self.exp_progress_bar.on_update_current_locale(self.current_locale)
        self.time_speed_knob.on_update_current_locale(self.current_locale)

    def on_update_clock_state(self, clock_24h_enabled):
        super().on_update_clock_state(clock_24h_enabled)
        if self.clock_24h_enabled:
            self.main_clock_label_12h.delete()
            self.main_clock_label_24h.create()
        else:
            self.main_clock_label_24h.delete()
            self.main_clock_label_12h.create()

    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.exp_progress_bar.on_update_opacity(self.opacity)
        self.money_progress_bar.on_update_opacity(self.opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.main_clock_label_24h.on_update_opacity(self.opacity)
        self.main_clock_label_12h.on_update_opacity(self.opacity)
        self.time_speed_knob.on_update_opacity(self.opacity)

    def on_update_time(self, dt):
        super().on_update_time(dt)
        self.main_clock_label_24h.on_update_args(
            ((self.game_time // (SECONDS_IN_ONE_MINUTE * MINUTES_IN_ONE_HOUR) + 12) % HOURS_IN_ONE_DAY,
             (self.game_time // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
        )
        self.main_clock_label_12h.on_update_args(
            ((self.game_time // (SECONDS_IN_ONE_MINUTE * MINUTES_IN_ONE_HOUR) + 11) % 12 + 1,
             (self.game_time // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
             I18N_RESOURCES['am_pm_string'][self.current_locale][
                 ((self.game_time // (SECONDS_IN_ONE_MINUTE * MINUTES_IN_ONE_HOUR)) // 12 + 1) % 2
             ])
        )

    def on_level_up(self):
        self.level += 1
        self.exp_progress_bar.on_update_text_label_args((self.level, ))
        CONFIG_DB_CURSOR.execute('''SELECT player_progress FROM player_progress_config 
                                    WHERE level = ?''', (self.level, ))
        self.player_progress = CONFIG_DB_CURSOR.fetchone()[0]

    def on_update_money(self, money):
        super().on_update_money(money)
        self.money_progress_bar.on_update_text_label_args((int(self.money), ))
        self.money_progress_bar.on_update_progress_bar_state(self.money, self.money_target)

    def on_resume_game(self):
        self.game_paused = False

    def on_update_exp(self, exp):
        self.exp = exp
        self.exp_progress_bar.on_update_progress_bar_state(self.exp, self.player_progress)

    def on_update_money_target(self, money_target):
        self.money_target = money_target
        self.money_progress_bar.on_update_progress_bar_state(self.money, self.money_target)

    @notifications_available
    @level_up_notification_enabled
    def on_send_level_up_notification(self):
        self.notifications.append(LevelUpNotification(self.current_locale, self.level))

    @notifications_available
    @enough_money_notification_enabled
    def on_send_enough_money_track_notification(self):
        self.notifications.append(EnoughMoneyTrackNotification(self.current_locale))

    @notifications_available
    @enough_money_notification_enabled
    def on_send_enough_money_environment_notification(self):
        self.notifications.append(EnoughMoneyEnvironmentNotification(self.current_locale))
