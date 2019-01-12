from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.resource import add_font

from .view_base import View
from .button import PauseGameButton, ResumeGameButton


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


class GameView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups):
        def on_pause_game(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_pause_game()

        def on_resume_game(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_resume_game()

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
        self.screen_resolution = (1280, 720)
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.game_frame_opacity = 0
        self.progress_bar_inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.progress_bar_exp_inactive = None
        self.progress_bar_money_inactive = None
        self.progress_bar_exp_active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.progress_bar_money_active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.progress_bar_exp_active = None
        self.progress_bar_money_active = None
        self.exp_offset = self.bottom_bar_height + 10
        self.money_offset = self.exp_offset + 10 + int(200 * self.bottom_bar_height / 80)
        self.pause_game_button = PauseGameButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                 on_click_action=on_pause_game)
        self.resume_game_button = ResumeGameButton(surface=self.surface, batch=self.ui_batch, groups=self.groups,
                                                   on_click_action=on_resume_game)
        self.pause_game_button.paired_button = self.resume_game_button
        self.resume_game_button.paired_button = self.pause_game_button
        self.buttons.append(self.pause_game_button)
        self.buttons.append(self.resume_game_button)
        add_font('perfo-bold.ttf')
        self.day_sprite = None
        self.time_sprite = None
        self.level_text = None
        self.money_text = None
        self.game_time = 0
        self.exp_percent = 0
        self.money_percent = 0

    def on_update(self):
        if self.is_activated:
            if self.game_frame_opacity < 255:
                self.game_frame_opacity += 15

            if self.progress_bar_exp_inactive.opacity < 255:
                self.progress_bar_exp_inactive.opacity += 15

            if self.progress_bar_exp_active.opacity < 255:
                self.progress_bar_exp_active.opacity += 15

            if self.progress_bar_money_inactive.opacity < 255:
                self.progress_bar_money_inactive.opacity += 15

            if self.progress_bar_money_active.opacity < 255:
                self.progress_bar_money_active.opacity += 15

        if not self.is_activated:
            if self.game_frame_opacity > 0:
                self.game_frame_opacity -= 15

            if self.progress_bar_exp_inactive is not None:
                if self.progress_bar_exp_inactive.opacity > 0:
                    self.progress_bar_exp_inactive.opacity -= 15
                    if self.progress_bar_exp_inactive.opacity <= 0:
                        self.progress_bar_exp_inactive.delete()
                        self.progress_bar_exp_inactive = None

            if self.progress_bar_exp_active is not None:
                if self.progress_bar_exp_active.opacity > 0:
                    self.progress_bar_exp_active.opacity -= 15
                    if self.progress_bar_exp_active.opacity <= 0:
                        self.progress_bar_exp_active.delete()
                        self.progress_bar_exp_active = None

            if self.progress_bar_money_inactive is not None:
                if self.progress_bar_money_inactive.opacity > 0:
                    self.progress_bar_money_inactive.opacity -= 15
                    if self.progress_bar_money_inactive.opacity <= 0:
                        self.progress_bar_money_inactive.delete()
                        self.progress_bar_money_inactive = None

            if self.progress_bar_money_active is not None:
                if self.progress_bar_money_active.opacity > 0:
                    self.progress_bar_money_active.opacity -= 15
                    if self.progress_bar_money_active.opacity <= 0:
                        self.progress_bar_money_active.delete()
                        self.progress_bar_money_active = None

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if self.progress_bar_exp_inactive is None:
            self.progress_bar_exp_inactive = Sprite(self.progress_bar_inactive_image,
                                                    x=self.exp_offset + round(self.exp_percent * 2
                                                                              * self.bottom_bar_height / 80),
                                                    y=self.bottom_bar_height // 8,
                                                    batch=self.ui_batch, group=self.groups['button_background'])
            self.progress_bar_exp_inactive.scale = self.bottom_bar_height / 80

        if self.progress_bar_money_inactive is None:
            self.progress_bar_money_inactive = Sprite(self.progress_bar_inactive_image,
                                                      x=self.money_offset + round(self.money_percent * 2
                                                                                  * self.bottom_bar_height / 80),
                                                      y=self.bottom_bar_height // 8,
                                                      batch=self.ui_batch, group=self.groups['button_background'])
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80

        if self.progress_bar_exp_active is None:
            self.progress_bar_exp_active = Sprite(self.progress_bar_exp_active_image, x=self.exp_offset,
                                                  y=self.bottom_bar_height // 8,
                                                  batch=self.ui_batch, group=self.groups['button_text'])
            self.progress_bar_exp_active.scale = self.bottom_bar_height / 80

        if self.progress_bar_money_active is None:
            self.progress_bar_money_active = Sprite(self.progress_bar_money_active_image, x=self.money_offset,
                                                    y=self.bottom_bar_height // 8,
                                                    batch=self.ui_batch, group=self.groups['button_text'])
            self.progress_bar_money_active.scale = self.bottom_bar_height / 80

        self.level_text = Label('LEVEL 0', font_name='Perfo', bold=True,
                                font_size=int(22 / 80 * self.bottom_bar_height),
                                x=self.exp_offset + int(100 / 80 * self.bottom_bar_height),
                                y=self.bottom_bar_height // 2,
                                anchor_x='center', anchor_y='center', batch=self.ui_batch,
                                group=self.groups['button_text'])
        self.money_text = Label('{0:0>8} ¤'.format(0), font_name='Perfo', bold=True, color=(0, 192, 0, 255),
                                font_size=int(22 / 80 * self.bottom_bar_height),
                                x=self.money_offset + int(100 / 80 * self.bottom_bar_height),
                                y=self.bottom_bar_height // 2,
                                anchor_x='center', anchor_y='center',
                                batch=self.ui_batch, group=self.groups['button_text'])

        self.day_sprite = Label(f'DAY  {1 + self.game_time // 345600}', font_name='Perfo', bold=True,
                                font_size=int(22 / 80 * self.bottom_bar_height),
                                color=(255, 255, 255, 255),
                                x=self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height),
                                y=int(57 / 80 * self.bottom_bar_height),
                                anchor_x='center', anchor_y='center', batch=self.ui_batch,
                                group=self.groups['button_text'])
        self.time_sprite = Label('{0:0>2} : {1:0>2}'.format((self.game_time // 14400 + 12) % 24,
                                                            (self.game_time // 240) % 60),
                                 font_name='Perfo', bold=True, font_size=int(22 / 80 * self.bottom_bar_height),
                                 color=(255, 255, 255, 255),
                                 x=self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height),
                                 y=int(26 / 80 * self.bottom_bar_height), anchor_x='center', anchor_y='center',
                                 batch=self.ui_batch, group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.level_text.delete()
        self.level_text = None
        self.money_text.delete()
        self.money_text = None
        self.day_sprite.delete()
        self.day_sprite = None
        self.time_sprite.delete()
        self.time_sprite = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.exp_offset = self.bottom_bar_height + 10
        self.money_offset = self.exp_offset + 10 + int(200 * self.bottom_bar_height / 80)
        if self.is_activated:
            self.level_text.x = self.exp_offset + int(100 / 80 * self.bottom_bar_height)
            self.level_text.y = self.bottom_bar_height // 2
            self.level_text.font_size = int(22 / 80 * self.bottom_bar_height)
            self.money_text.x = self.money_offset + int(100 / 80 * self.bottom_bar_height)
            self.money_text.y = self.bottom_bar_height // 2
            self.money_text.font_size = int(22 / 80 * self.bottom_bar_height)
            self.day_sprite.x = self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height)
            self.day_sprite.y = int(57 / 80 * self.bottom_bar_height)
            self.day_sprite.font_size = int(22 / 80 * self.bottom_bar_height)
            self.time_sprite.x = self.screen_resolution[0] - int(181 / 80 * self.bottom_bar_height)
            self.time_sprite.y = int(26 / 80 * self.bottom_bar_height)
            self.time_sprite.font_size = int(22 / 80 * self.bottom_bar_height)
            self.progress_bar_exp_inactive.x = self.exp_offset + round(self.exp_percent * 2
                                                                       * self.bottom_bar_height / 80)
            self.progress_bar_exp_inactive.y = self.bottom_bar_height // 8
            self.progress_bar_exp_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_money_inactive.x = self.money_offset + round(self.money_percent * 2
                                                                           * self.bottom_bar_height / 80)
            self.progress_bar_money_inactive.y = self.bottom_bar_height // 8
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_exp_active.x = self.exp_offset
            self.progress_bar_exp_active.y = self.bottom_bar_height // 8
            self.progress_bar_exp_active.scale = self.bottom_bar_height / 80
            self.progress_bar_money_active.x = self.money_offset
            self.progress_bar_money_active.y = self.bottom_bar_height // 8
            self.progress_bar_money_active.scale = self.bottom_bar_height / 80

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
            self.time_sprite.text = '{0:0>2} : {1:0>2}'.format((self.game_time // 14400 + 12) % 24,
                                                               (self.game_time // 240) % 60)
            self.day_sprite.text = f'DAY  {1 + self.game_time // 345600}'

    @_view_is_active
    def on_update_exp(self, exp, player_progress):
        if player_progress < 1:
            self.exp_percent = 0
        else:
            self.exp_percent = int(exp / player_progress * 100)
            if self.exp_percent > 100:
                self.exp_percent = 100

        if self.exp_percent == 0:
            image_region = self.progress_bar_exp_active_image.get_region(30, 30, 1, 1)
        else:
            image_region = self.progress_bar_exp_active_image.get_region(0, 0, self.exp_percent * 2, 60)

        self.progress_bar_exp_active.image = image_region
        if self.exp_percent < 100:
            image_region = self.progress_bar_inactive_image.get_region(self.exp_percent * 2, 0,
                                                                       200 - self.exp_percent * 2, 60)
        else:
            image_region = self.progress_bar_inactive_image.get_region(30, 30, 1, 1)

        self.progress_bar_exp_inactive.image = image_region
        self.progress_bar_exp_inactive.position \
            = (self.exp_offset + round(self.exp_percent * 2 * self.bottom_bar_height / 80), self.bottom_bar_height // 8)

    @_view_is_active
    def on_update_level(self, level):
        self.level_text.text = f'LEVEL {level}'

    @_view_is_active
    def on_update_money(self, money, money_target):
        self.money_text.text = '{0:0>8} ¤'.format(int(money))
        if money_target < 1:
            self.money_percent = 0
        else:
            self.money_percent = int(money / money_target * 100)
            if self.money_percent > 100:
                self.money_percent = 100

        if self.money_percent == 0:
            image_region = self.progress_bar_money_active_image.get_region(30, 30, 1, 1)
        else:
            image_region = self.progress_bar_money_active_image.get_region(0, 0, self.money_percent * 2, 60)

        self.progress_bar_money_active.image = image_region
        if self.money_percent < 100:
            image_region = self.progress_bar_inactive_image.get_region(self.money_percent * 2, 0,
                                                                       200 - self.money_percent * 2, 60)
        else:
            image_region = self.progress_bar_inactive_image.get_region(30, 30, 1, 1)

        self.progress_bar_money_inactive.image = image_region
        self.progress_bar_money_inactive.position \
            = (self.money_offset + round(self.money_percent * 2 * self.bottom_bar_height / 80),
               self.bottom_bar_height // 8)
