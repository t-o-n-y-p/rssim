from logging import getLogger

from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.resource import add_font
from pyglet.gl import GL_QUADS
from pyshaders import from_files_names

from view import *
from ui.button import create_two_state_button
from ui.button.open_settings_game_view_button import OpenSettingsGameViewButton
from ui.button.pause_game_button import PauseGameButton
from ui.button.resume_game_button import ResumeGameButton
from notifications.level_up_notification import LevelUpNotification
from notifications.enough_money_track_notification import EnoughMoneyTrackNotification
from notifications.enough_money_environment_notification import EnoughMoneyEnvironmentNotification
from i18n import I18N_RESOURCES


class GameView(View):
    """
    Implements Game view.
    Game object is responsible for properties, UI and events related to the game process.
    """
    def __init__(self):
        """
        Button click handlers:
            on_pause_game                           on_click handler for pause game button
            on_resume_game                          on_click handler for resume game button
            on_open_settings                        on_click handler for open settings button

        Properties:
            progress_bar_inactive_image             base image for exp amd money progress bar
            progress_bar_exp_inactive               sprite from base image for exp progress bar
            progress_bar_money_inactive             sprite from base image for money progress bar
            progress_bar_exp_active_image           image for exp progress bar
            progress_bar_money_active_image         image for money progress bar
            progress_bar_exp_active                 sprite from image for exp progress bar
            progress_bar_money_active               sprite from image for money progress bar
            exp_offset                              offset from the left edge for exp progress bar
            money_offset                            offset from the left edge for money progress bar
            pause_game_button                       PauseGameButton object
            resume_game_button                      ResumeGameButton object
            open_settings_button                    OpenSettingsButton object
            buttons                                 list of all buttons
            time_label                              time label
            level_label                             "LEVEL X" label
            money_label                             money label
            game_time                               in-game timestamp
            exp_percent                             exp percentage for current level
            money_percent                           money percentage from money target
            level_up_notification_enabled           indicates if level up notifications are enabled by user
                                                    in game settings
            enough_money_notification_enabled       indicates if enough money notifications are enabled by user
                                                    in game settings
            clock_24h_enabled                       indicates if 24h clock is enabled
            game_view_shader_upper_limit            upper edge for game_view_shader_sprite

        """
        def on_pause_game(button):
            """
            Deactivates pause game button. Activates resume game button.
            Notifies controller that player has paused the game.

            :param button:                      button that was clicked
            """
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate(instant=True)
            self.controller.on_pause_game()

        def on_resume_game(button):
            """
            Deactivates resume game button. Activates pause game button.
            Notifies controller that player has resumed the game.

            :param button:                      button that was clicked
            """
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate(instant=True)
            self.controller.on_resume_game()

        def on_open_settings(button):
            """
            Deactivates settings button.
            Notifies controller that player has opened settings screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.parent_controller.settings_to_game_transition_animation.on_deactivate()
            self.controller.parent_controller.game_to_settings_transition_animation.on_activate()
            self.controller.parent_controller.settings.navigated_from_game = True

        super().__init__(logger=getLogger('root.app.game.view'))
        self.progress_bar_inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.progress_bar_exp_inactive = None
        self.progress_bar_money_inactive = None
        self.progress_bar_exp_active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.progress_bar_money_active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.progress_bar_exp_active = None
        self.progress_bar_money_active = None
        self.exp_offset = self.bottom_bar_height + self.bottom_bar_height // 8
        self.money_offset = self.exp_offset + self.bottom_bar_height // 8 \
                          + int(self.progress_bar_inactive_image.width * self.bottom_bar_height / 80)
        self.pause_game_button, self.resume_game_button \
            = create_two_state_button(PauseGameButton(on_click_action=on_pause_game),
                                      ResumeGameButton(on_click_action=on_resume_game))
        self.open_settings_button = OpenSettingsGameViewButton(on_click_action=on_open_settings)
        self.buttons = [self.pause_game_button, self.resume_game_button, self.open_settings_button]
        add_font('perfo-bold.ttf')
        self.time_label = None
        self.level_label = None
        self.money_label = None
        self.game_time = 0
        self.exp_percent = 0
        self.money_percent = 0
        self.level = 0
        self.user_db_cursor.execute('''SELECT level_up_notification_enabled, enough_money_notification_enabled
                                       FROM notification_settings''')
        self.level_up_notification_enabled, self.enough_money_notification_enabled = self.user_db_cursor.fetchone()
        self.level_up_notification_enabled = bool(self.level_up_notification_enabled)
        self.enough_money_notification_enabled = bool(self.enough_money_notification_enabled)
        self.user_db_cursor.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(self.user_db_cursor.fetchone()[0])
        self.shader = from_files_names('shaders/shader.vert', 'shaders/game_view/shader.frag')
        self.game_view_shader_upper_limit = 0.0
        self.on_init_graphics()

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.shader_sprite = None
            self.time_label.delete()
            self.time_label = None
            self.progress_bar_exp_inactive.delete()
            self.progress_bar_exp_inactive = None
            self.progress_bar_exp_active.delete()
            self.progress_bar_exp_active = None
            self.progress_bar_money_inactive.delete()
            self.progress_bar_money_inactive = None
            self.progress_bar_money_active.delete()
            self.progress_bar_money_active = None
            self.money_label.delete()
            self.money_label = None
            self.level_label.delete()
            self.level_label = None
        else:
            self.time_label.color = (*WHITE_RGB, self.opacity)
            self.progress_bar_exp_inactive.opacity = self.opacity
            self.progress_bar_exp_active.opacity = self.opacity
            self.progress_bar_money_inactive.opacity = self.opacity
            self.progress_bar_money_active.opacity = self.opacity
            self.level_label.color = (*WHITE_RGB, self.opacity)
            self.money_label.color = (*GREEN_RGB, self.opacity)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels.
        """
        self.is_activated = True
        if self.shader_sprite is None:
            self.shader_sprite\
                = self.batches['main_frame'].add(4, GL_QUADS, self.groups['main_frame'],
                                                 ('v2f/static', (-1.0, -1.0, -1.0, self.game_view_shader_upper_limit,
                                                                 1.0, self.game_view_shader_upper_limit, 1.0, -1.0)))

        if self.time_label is None:
            self.time_label = Label(self.get_time_text(), font_name='Perfo', bold=True,
                                    font_size=int(32 / 80 * self.bottom_bar_height), color=(*WHITE_RGB, self.opacity),
                                    x=self.screen_resolution[0] - int(200 / 80 * self.bottom_bar_height),
                                    y=self.bottom_bar_height // 2, anchor_x='center', anchor_y='center',
                                    batch=self.batches['ui_batch'], group=self.groups['button_text'])

        if self.progress_bar_exp_inactive is None:
            self.progress_bar_exp_inactive = Sprite(self.progress_bar_inactive_image,
                                                    x=self.exp_offset,
                                                    y=self.bottom_bar_height // 8,
                                                    batch=self.batches['ui_batch'],
                                                    group=self.groups['button_background'])
            self.progress_bar_exp_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_inactive.opacity = self.opacity

        if self.progress_bar_exp_active is None:
            self.progress_bar_exp_active = Sprite(self.progress_bar_exp_active_image, x=self.exp_offset,
                                                  y=self.bottom_bar_height // 8,
                                                  batch=self.batches['ui_batch'],
                                                  group=self.groups['button_text'])
            self.progress_bar_exp_active.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_active.opacity = self.opacity

        if self.level_label is None:
            self.level_label = Label(I18N_RESOURCES['level_string'][self.current_locale].format(0),
                                     font_name='Perfo', bold=True, color=(*WHITE_RGB, self.opacity),
                                     font_size=int(22 / 80 * self.bottom_bar_height),
                                     x=self.exp_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                             * self.bottom_bar_height),
                                     y=self.bottom_bar_height // 2,
                                     anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                     group=self.groups['button_text'])

        if self.progress_bar_money_inactive is None:
            self.progress_bar_money_inactive = Sprite(self.progress_bar_inactive_image,
                                                      x=self.money_offset,
                                                      y=self.bottom_bar_height // 8,
                                                      batch=self.batches['ui_batch'],
                                                      group=self.groups['button_background'])
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_money_inactive.opacity = self.opacity

        if self.progress_bar_money_active is None:
            self.progress_bar_money_active = Sprite(self.progress_bar_money_active_image, x=self.money_offset,
                                                    y=self.bottom_bar_height // 8,
                                                    batch=self.batches['ui_batch'],
                                                    group=self.groups['button_text'])
            self.progress_bar_money_active.scale = self.bottom_bar_height / 80
            self.progress_bar_money_active.opacity = self.opacity

        if self.money_label is None:
            self.money_label = Label('0', font_name='Perfo', bold=True, color=(*GREEN_RGB, self.opacity),
                                     font_size=int(22 / 80 * self.bottom_bar_height),
                                     x=self.money_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                               * self.bottom_bar_height),
                                     y=self.bottom_bar_height // 2,
                                     anchor_x='center', anchor_y='center',
                                     batch=self.batches['ui_batch'], group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.exp_offset = self.bottom_bar_height + self.bottom_bar_height // 8
        self.money_offset = self.exp_offset + self.bottom_bar_height // 8 \
                          + int(self.progress_bar_inactive_image.width * self.bottom_bar_height / 80)
        self.game_view_shader_upper_limit = self.bottom_bar_height / self.screen_resolution[1] * 2 - 1
        if self.is_activated:
            self.level_label.x = self.exp_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                       * self.bottom_bar_height)
            self.level_label.y = self.bottom_bar_height // 2
            self.level_label.font_size = int(22 / 80 * self.bottom_bar_height)
            self.money_label.x = self.money_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                         * self.bottom_bar_height)
            self.money_label.y = self.bottom_bar_height // 2
            self.money_label.font_size = int(22 / 80 * self.bottom_bar_height)
            self.time_label.x = self.screen_resolution[0] - int(200 / 80 * self.bottom_bar_height)
            self.time_label.y = self.bottom_bar_height // 2
            self.time_label.font_size = int(32 / 80 * self.bottom_bar_height)
            self.progress_bar_exp_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_inactive.position = (self.exp_offset, self.bottom_bar_height // 8)
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_money_inactive.position = (self.money_offset, self.bottom_bar_height // 8)
            self.progress_bar_exp_active.update(x=self.exp_offset, y=self.bottom_bar_height // 8,
                                                scale=self.bottom_bar_height / 80)
            self.progress_bar_money_active.update(x=self.money_offset, y=self.bottom_bar_height // 8,
                                                  scale=self.bottom_bar_height / 80)
            self.shader_sprite.vertices = (-1.0, -1.0, -1.0, self.game_view_shader_upper_limit,
                                           1.0, self.game_view_shader_upper_limit, 1.0, -1.0)

        self.open_settings_button.x_margin = self.screen_resolution[0] - self.bottom_bar_height
        self.open_settings_button.y_margin = 0
        self.open_settings_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.pause_game_button.x_margin = self.screen_resolution[0] - 5 * self.bottom_bar_height
        self.pause_game_button.y_margin = 0
        self.resume_game_button.x_margin = self.screen_resolution[0] - 5 * self.bottom_bar_height
        self.resume_game_button.y_margin = 0
        self.pause_game_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.resume_game_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    @view_is_active
    def on_pause_game(self):
        """
        Reserved for future use.
        """
        pass

    @view_is_active
    def on_resume_game(self):
        """
        Reserved for future use.
        """
        pass

    def on_update_time(self, game_time):
        """
        Updates in-game time in the bottom bar.

        :param game_time:                       current in-game time
        """
        self.game_time = game_time
        if self.is_activated:
            self.time_label.text = self.get_time_text()

    @view_is_active
    def on_update_exp(self, exp, player_progress):
        """
        Updates exp value and exp progress bar.

        :param exp:                             exp value
        :param player_progress:                 exp needed to hit next level
        """
        if player_progress < 1:
            self.exp_percent = 0
        else:
            self.exp_percent = int(exp / player_progress * 100)
            if self.exp_percent > 100:
                self.exp_percent = 100

        if self.exp_percent == 0:
            image_region = self.progress_bar_exp_active_image\
                .get_region(self.progress_bar_exp_active_image.height // 2,
                            self.progress_bar_exp_active_image.height // 2, 1, 1)
        else:
            image_region = self.progress_bar_exp_active_image\
                .get_region(0, 0, self.exp_percent * self.progress_bar_exp_active_image.width // 100,
                            self.progress_bar_exp_active_image.height)

        self.progress_bar_exp_active.image = image_region

    @view_is_active
    def on_update_level(self, level):
        """
        Updates level and level label.

        :param level:                           current player level
        """
        self.level = level
        self.level_label.text = I18N_RESOURCES['level_string'][self.current_locale].format(self.level)

    @view_is_active
    def on_update_money(self, money, money_target):
        """
        Updates money value and money progress bar.

        :param money:                           money value
        :param money_target:                    current money target assigned by player
        """
        money_str = '{0:0>10}  ¤'.format(int(money))
        self.money_label.text = ' '.join((money_str[0], money_str[1:4], money_str[4:7], money_str[7:13]))
        if money_target < 1:
            self.money_percent = 0
        else:
            self.money_percent = int(money / money_target * 100)
            if self.money_percent > 100:
                self.money_percent = 100

        if self.money_percent == 0:
            image_region = self.progress_bar_money_active_image\
                .get_region(self.progress_bar_money_active_image.height // 2,
                            self.progress_bar_money_active_image.height // 2, 1, 1)
        else:
            image_region = self.progress_bar_money_active_image\
                .get_region(0, 0, self.money_percent * self.progress_bar_money_active_image.width // 100,
                            self.progress_bar_money_active_image.height)

        self.progress_bar_money_active.image = image_region

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.level_label.text = I18N_RESOURCES['level_string'][self.current_locale].format(self.level)
            self.time_label.text = self.get_time_text()

    @notifications_available
    @level_up_notification_enabled
    def on_send_level_up_notification(self, level):
        """
        Sends system notification about level update.

        :param level:                           new level
        """
        level_up_notification = LevelUpNotification()
        level_up_notification.send(self.current_locale, message_args=(level,))
        self.controller.parent_controller.on_append_notification(level_up_notification)

    @notifications_available
    @enough_money_notification_enabled
    def on_send_enough_money_track_notification(self):
        """
        Notifies the player he/she can now buy the next track.
        """
        enough_money_track_notification = EnoughMoneyTrackNotification()
        enough_money_track_notification.send(self.current_locale)
        self.controller.parent_controller.on_append_notification(enough_money_track_notification)

    @notifications_available
    @enough_money_notification_enabled
    def on_send_enough_money_environment_notification(self):
        """
        Notifies the player he/she can now buy the next track.
        """
        enough_money_environment_notification = EnoughMoneyEnvironmentNotification()
        enough_money_environment_notification.send(self.current_locale)
        self.controller.parent_controller.on_append_notification(enough_money_environment_notification)

    def on_change_level_up_notification_state(self, notification_state):
        """
        Updates level up notification state.

        :param notification_state:              new notification state defined by player
        """
        self.level_up_notification_enabled = notification_state

    def on_change_enough_money_notification_state(self, notification_state):
        """
        Updates enough money notification state.

        :param notification_state:              new notification state defined by player
        """
        self.enough_money_notification_enabled = notification_state

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.screen_resolution = self.screen_resolution
        self.shader.uniforms.bottom_bar_height = self.bottom_bar_height
        self.shader.uniforms.game_frame_opacity = self.opacity
        self.shader_sprite.draw(GL_QUADS)
        self.shader.clear()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    def get_time_text(self):
        if self.clock_24h_enabled:
            return '{0:0>2} : {1:0>2}'.format((self.game_time // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                                              (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
        else:
            am_pm_index = ((self.game_time // FRAMES_IN_ONE_HOUR) // 12 + 1) % 2
            return '{0} : {1:0>2} {2}'.format((self.game_time // FRAMES_IN_ONE_HOUR + 11) % 12 + 1,
                                              (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
                                              I18N_RESOURCES['am_pm_string'][self.current_locale][am_pm_index])

    def on_update_clock_state(self, clock_24h_enabled):
        """
        Updates main game clock when clock state is updated.

        :param clock_24h_enabled:               indicates if 24h clock is enabled
        """
        self.clock_24h_enabled = clock_24h_enabled
        if self.is_activated:
            self.time_label.text = self.get_time_text()
