from logging import getLogger

from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.resource import add_font

from view import *
from button.pause_game_button import PauseGameButton
from button.resume_game_button import ResumeGameButton


class GameView(View):
    """
    Implements Game view.
    Game object is responsible for properties, UI and events related to the game process.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_pause_game                       on_click handler for pause game button
            on_resume_game                      on_click handler for resume game button

        Properties:
            game_frame_opacity                  overall opacity of all game sprites
            progress_bar_inactive_image         base image for exp amd money progress bar
            progress_bar_exp_inactive           sprite from base image for exp progress bar
            progress_bar_money_inactive         sprite from base image for money progress bar
            progress_bar_exp_active_image       image for exp progress bar
            progress_bar_money_active_image     image for money progress bar
            progress_bar_exp_active             sprite from image for exp progress bar
            progress_bar_money_active           sprite from image for money progress bar
            exp_offset                          offset from the left edge for exp progress bar
            money_offset                        offset from the left edge for money progress bar
            pause_game_button                   PauseGameButton object
            resume_game_button                  ResumeGameButton object
            buttons                             list of all buttons
            day_label                           "DAY X" label
            time_label                          time label
            level_label                         "LEVEL X" label
            money_label                         money label
            game_time                           in-game timestamp
            exp_percent                         exp percentage for current level
            money_percent                       money percentage from money target

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        def on_pause_game(button):
            """
            Deactivates pause game button. Activates resume game button.
            Notifies controller that player has paused the game.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_PAUSE_GAME')
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_pause_game()
            self.logger.info('END ON_PAUSE_GAME')

        def on_resume_game(button):
            """
            Deactivates resume game button. Activates pause game button.
            Notifies controller that player has resumed the game.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_RESUME_GAME')
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_resume_game()
            self.logger.info('END ON_RESUME_GAME')

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.view'))
        self.logger.info('START INIT')
        self.game_frame_opacity = 0
        self.progress_bar_inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.progress_bar_exp_inactive = None
        self.progress_bar_money_inactive = None
        self.progress_bar_exp_active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.progress_bar_money_active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.progress_bar_exp_active = None
        self.progress_bar_money_active = None
        self.logger.debug('images loaded successfully')
        self.exp_offset = self.bottom_bar_height + self.bottom_bar_height // 8
        self.logger.debug(f'exp_offset: {self.exp_offset}')
        self.money_offset = self.exp_offset + self.bottom_bar_height // 8 \
                          + int(self.progress_bar_inactive_image.width * self.bottom_bar_height / 80)
        self.pause_game_button = PauseGameButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                 groups=self.groups, on_click_action=on_pause_game)
        self.resume_game_button = ResumeGameButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                   groups=self.groups, on_click_action=on_resume_game)
        self.pause_game_button.paired_button = self.resume_game_button
        self.resume_game_button.paired_button = self.pause_game_button
        self.logger.debug('buttons created successfully')
        self.buttons.append(self.pause_game_button)
        self.buttons.append(self.resume_game_button)
        self.logger.debug(f'buttons list length: {len(self.buttons)}')
        add_font('perfo-bold.ttf')
        self.day_label = None
        self.time_label = None
        self.level_label = None
        self.money_label = None
        self.game_time = 0
        self.exp_percent = 0
        self.money_percent = 0
        self.level = 0
        self.logger.info('END INIT')

    def on_update(self):

        if self.is_activated:
            if self.game_frame_opacity < 255:
                self.game_frame_opacity += 15
                self.progress_bar_exp_inactive.opacity += 15
                self.progress_bar_exp_active.opacity += 15
                self.progress_bar_money_inactive.opacity += 15
                self.progress_bar_money_active.opacity += 15

        if not self.is_activated:
            if self.game_frame_opacity > 0:
                self.game_frame_opacity -= 15
                self.progress_bar_exp_inactive.opacity -= 15
                if self.progress_bar_exp_inactive.opacity <= 0:
                    self.progress_bar_exp_inactive.delete()
                    self.progress_bar_exp_inactive = None

                self.progress_bar_exp_active.opacity -= 15
                if self.progress_bar_exp_active.opacity <= 0:
                    self.progress_bar_exp_active.delete()
                    self.progress_bar_exp_active = None

                self.progress_bar_money_inactive.opacity -= 15
                if self.progress_bar_money_inactive.opacity <= 0:
                    self.progress_bar_money_inactive.delete()
                    self.progress_bar_money_inactive = None

                self.progress_bar_money_active.opacity -= 15
                if self.progress_bar_money_active.opacity <= 0:
                    self.progress_bar_money_active.delete()
                    self.progress_bar_money_active = None

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if self.progress_bar_exp_inactive is None:
            self.progress_bar_exp_inactive = Sprite(self.progress_bar_inactive_image,
                                                    x=self.exp_offset,
                                                    y=self.bottom_bar_height // 8,
                                                    batch=self.batches['ui_batch'],
                                                    group=self.groups['button_background'])
            self.progress_bar_exp_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_inactive.opacity = 0

        if self.progress_bar_money_inactive is None:
            self.progress_bar_money_inactive = Sprite(self.progress_bar_inactive_image,
                                                      x=self.money_offset,
                                                      y=self.bottom_bar_height // 8,
                                                      batch=self.batches['ui_batch'],
                                                      group=self.groups['button_background'])
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_money_inactive.opacity = 0

        if self.progress_bar_exp_active is None:
            self.progress_bar_exp_active = Sprite(self.progress_bar_exp_active_image, x=self.exp_offset,
                                                  y=self.bottom_bar_height // 8,
                                                  batch=self.batches['ui_batch'],
                                                  group=self.groups['button_text'])
            self.progress_bar_exp_active.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_active.opacity = 0

        if self.progress_bar_money_active is None:
            self.progress_bar_money_active = Sprite(self.progress_bar_money_active_image, x=self.money_offset,
                                                    y=self.bottom_bar_height // 8,
                                                    batch=self.batches['ui_batch'],
                                                    group=self.groups['button_text'])
            self.progress_bar_money_active.scale = self.bottom_bar_height / 80
            self.progress_bar_money_active.opacity = 0

        self.level_label = Label('LEVEL  0', font_name='Perfo', bold=True,
                                 font_size=int(22 / 80 * self.bottom_bar_height),
                                 x=self.exp_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                         * self.bottom_bar_height),
                                 y=self.bottom_bar_height // 2,
                                 anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                 group=self.groups['button_text'])
        self.money_label = Label('{0:0>10}  ¤'.format(0), font_name='Perfo', bold=True, color=GREEN,
                                 font_size=int(22 / 80 * self.bottom_bar_height),
                                 x=self.money_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                           * self.bottom_bar_height),
                                 y=self.bottom_bar_height // 2,
                                 anchor_x='center', anchor_y='center',
                                 batch=self.batches['ui_batch'], group=self.groups['button_text'])

        self.day_label = Label(f'DAY  {1 + self.game_time // FRAMES_IN_ONE_DAY}', font_name='Perfo', bold=True,
                               font_size=int(22 / 80 * self.bottom_bar_height),
                               x=self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height),
                               y=int(57 / 80 * self.bottom_bar_height),
                               anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                               group=self.groups['button_text'])
        self.time_label = Label('{0:0>2} : {1:0>2}'
                                .format((self.game_time // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                                        (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR),
                                font_name='Perfo', bold=True, font_size=int(22 / 80 * self.bottom_bar_height),
                                x=self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height),
                                y=int(26 / 80 * self.bottom_bar_height), anchor_x='center', anchor_y='center',
                                batch=self.batches['ui_batch'], group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.level_label.delete()
        self.level_label = None
        self.money_label.delete()
        self.money_label = None
        self.day_label.delete()
        self.day_label = None
        self.time_label.delete()
        self.time_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.exp_offset = self.bottom_bar_height + self.bottom_bar_height // 8
        self.money_offset = self.exp_offset + self.bottom_bar_height // 8 \
                          + int(self.progress_bar_inactive_image.width * self.bottom_bar_height / 80)
        if self.is_activated:
            self.level_label.x = self.exp_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                       * self.bottom_bar_height)
            self.level_label.y = self.bottom_bar_height // 2
            self.level_label.font_size = int(22 / 80 * self.bottom_bar_height)
            self.money_label.x = self.money_offset + int(self.progress_bar_inactive_image.width / 2 / 80
                                                         * self.bottom_bar_height)
            self.money_label.y = self.bottom_bar_height // 2
            self.money_label.font_size = int(22 / 80 * self.bottom_bar_height)
            self.day_label.x = self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height)
            self.day_label.y = int(57 / 80 * self.bottom_bar_height)
            self.day_label.font_size = int(22 / 80 * self.bottom_bar_height)
            self.time_label.x = self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height)
            self.time_label.y = int(26 / 80 * self.bottom_bar_height)
            self.time_label.font_size = int(22 / 80 * self.bottom_bar_height)
            self.progress_bar_exp_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_inactive.position \
                = (self.exp_offset,
                   self.bottom_bar_height // 8)
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_money_inactive.position \
                = (self.money_offset,
                   self.bottom_bar_height // 8)
            self.progress_bar_exp_active.update(x=self.exp_offset, y=self.bottom_bar_height // 8,
                                                scale=self.bottom_bar_height / 80)
            self.progress_bar_money_active.update(x=self.money_offset, y=self.bottom_bar_height // 8,
                                                  scale=self.bottom_bar_height / 80)

        self.pause_game_button.x_margin = self.screen_resolution[0] - 9 * self.bottom_bar_height // 2
        self.resume_game_button.x_margin = self.screen_resolution[0] - 9 * self.bottom_bar_height // 2
        self.pause_game_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                               self.bottom_bar_height // 2)
        self.resume_game_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                self.bottom_bar_height // 2)
        for b in self.buttons:
            b.on_position_changed((b.x_margin, 0))

    def on_pause_game(self):
        pass

    def on_resume_game(self):
        pass

    def on_update_game_time(self, game_time):
        self.game_time = game_time
        if self.is_activated:
            self.time_label.text = '{0:0>2} : {1:0>2}'\
                .format((self.game_time // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                        (self.game_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
            self.day_label.text = f'DAY  {1 + self.game_time // FRAMES_IN_ONE_DAY}'

    @view_is_active
    def on_update_exp(self, exp, player_progress):
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
        self.level_label.text = f'LEVEL  {self.level}'

    @view_is_active
    def on_update_level(self, level):
        self.level = level
        self.level_label.text = f'LEVEL  {self.level}'

    @view_is_active
    def on_update_money(self, money, money_target):
        self.money_label.text = '{0:0>10}  ¤'.format(int(money))
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
