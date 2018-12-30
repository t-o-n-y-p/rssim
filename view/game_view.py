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
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        def on_pause_game(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_pause_game()

        def on_resume_game(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_resume_game()

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.screen_resolution = (1280, 720)
        self.game_frame = load('img/game_frame/game_frame_1280_720.png')
        self.game_frame_sprite = None
        self.progress_bar_inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.progress_bar_exp_inactive = None
        self.progress_bar_money_inactive = None
        self.progress_bar_exp_active_image = load('img/game_progress_bars/progress_bar_active.png')
        self.progress_bar_money_active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.progress_bar_exp_active = None
        self.progress_bar_money_active = None
        self.exp_offset = 90
        self.money_offset = 300
        self.pause_game_button = PauseGameButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                 on_click_action=on_pause_game)
        self.resume_game_button = ResumeGameButton(surface=self.surface, batch=self.batch, groups=self.groups,
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

    def on_update(self):
        if self.is_activated:
            if self.game_frame_sprite.opacity < 255:
                self.game_frame_sprite.opacity += 15

            if self.progress_bar_exp_inactive.opacity < 255:
                self.progress_bar_exp_inactive.opacity += 15

            if self.progress_bar_exp_active.opacity < 255:
                self.progress_bar_exp_active.opacity += 15

            if self.progress_bar_money_inactive.opacity < 255:
                self.progress_bar_money_inactive.opacity += 15

            if self.progress_bar_money_active.opacity < 255:
                self.progress_bar_money_active.opacity += 15

        if not self.is_activated:
            if self.game_frame_sprite is not None:
                if self.game_frame_sprite.opacity > 0:
                    self.game_frame_sprite.opacity -= 15
                    if self.game_frame_sprite.opacity <= 0:
                        self.game_frame_sprite.delete()
                        self.game_frame_sprite = None

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
        if self.game_frame_sprite is None:
            self.game_frame_sprite = Sprite(self.game_frame, x=0, y=0, batch=self.batch,
                                            group=self.groups['main_frame'])
            self.game_frame_sprite.opacity = 0

        if self.progress_bar_exp_inactive is None:
            self.progress_bar_exp_inactive = Sprite(self.progress_bar_inactive_image, x=self.exp_offset, y=10,
                                                    batch=self.batch, group=self.groups['button_background'])

        if self.progress_bar_money_inactive is None:
            self.progress_bar_money_inactive = Sprite(self.progress_bar_inactive_image, x=self.money_offset, y=10,
                                                      batch=self.batch, group=self.groups['button_background'])

        if self.progress_bar_exp_active is None:
            self.progress_bar_exp_active = Sprite(self.progress_bar_exp_active_image, x=self.exp_offset, y=10,
                                                  batch=self.batch, group=self.groups['button_text'])

        if self.progress_bar_money_active is None:
            self.progress_bar_money_active = Sprite(self.progress_bar_money_active_image, x=self.money_offset, y=10,
                                                    batch=self.batch, group=self.groups['button_text'])

        self.level_text = Label('LEVEL 0', font_name='Perfo', bold=True, font_size=22, x=self.exp_offset + 100, y=40,
                                anchor_x='center', anchor_y='center', batch=self.batch,
                                group=self.groups['button_text'])
        self.money_text = Label('{0:0>8} ¤'.format(0), font_name='Perfo', bold=True, color=(0, 192, 0, 255),
                                font_size=22, x=self.money_offset + 100, y=40, anchor_x='center', anchor_y='center',
                                batch=self.batch, group=self.groups['button_text'])

        self.day_sprite = Label(f'DAY  {1 + self.game_time // 345600}', font_name='Perfo', bold=True, font_size=22,
                                color=(255, 255, 255, 255), x=self.screen_resolution[0] - 181, y=57,
                                anchor_x='center', anchor_y='center', batch=self.batch,
                                group=self.groups['button_text'])
        self.time_sprite = Label('{0:0>2} : {1:0>2}'.format((self.game_time // 14400 + 12) % 24,
                                                            (self.game_time // 240) % 60),
                                 font_name='Perfo', bold=True, font_size=22, color=(255, 255, 255, 255),
                                 x=self.screen_resolution[0] - 181, y=26, anchor_x='center', anchor_y='center',
                                 batch=self.batch, group=self.groups['button_text'])

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
        self.game_frame = load('img/game_frame/game_frame_{}_{}.png'.format(screen_resolution[0], screen_resolution[1]))
        if self.is_activated:
            self.game_frame_sprite.image = self.game_frame

            self.day_sprite.delete()
            self.day_sprite = None
            self.day_sprite = Label(f'DAY  {1 + self.game_time // 345600}', font_name='Perfo', bold=True, font_size=22,
                                    color=(255, 255, 255, 255), x=self.screen_resolution[0] - 181, y=57,
                                    anchor_x='center', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
            self.time_sprite.delete()
            self.time_sprite = None
            self.time_sprite = Label('{0:0>2} : {1:0>2}'.format((self.game_time // 14400 + 12) % 24,
                                                                (self.game_time // 240) % 60),
                                     font_name='Perfo', bold=True, font_size=22, color=(255, 255, 255, 255),
                                     x=self.screen_resolution[0] - 181, y=26, anchor_x='center', anchor_y='center',
                                     batch=self.batch, group=self.groups['button_text'])

        for b in self.buttons:
            b.on_position_changed((self.screen_resolution[0] - b.x_margin, 0))

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
            exp_percent = 0
        else:
            exp_percent = int(exp / player_progress * 100)
            if exp_percent > 100:
                exp_percent = 100

        if exp_percent == 0:
            image_region = self.progress_bar_exp_active_image.get_region(0, 0, 1, 10)
        else:
            image_region = self.progress_bar_exp_active_image.get_region(0, 0, exp_percent * 2, 60)

        self.progress_bar_exp_active.image = image_region
        if exp_percent < 100:
            image_region = self.progress_bar_inactive_image.get_region(exp_percent * 2, 0, 200 - exp_percent * 2, 60)
        else:
            image_region = self.progress_bar_inactive_image.get_region(199, 0, 1, 10)

        self.progress_bar_exp_inactive.image = image_region
        self.progress_bar_exp_inactive.position = (self.exp_offset + exp_percent * 2, 10)

    @_view_is_active
    def on_update_level(self, level):
        self.level_text.text = f'LEVEL {level}'

    @_view_is_active
    def on_update_money(self, money, money_target):
        if money_target < 1:
            money_percent = 0
        else:
            money_percent = int(money / money_target * 100)
            if money_percent > 100:
                money_percent = 100

        if money_percent == 0:
            image_region = self.progress_bar_money_active_image.get_region(0, 0, 1, 10)
        else:
            image_region = self.progress_bar_money_active_image.get_region(0, 0, money_percent * 2, 60)

        self.progress_bar_money_active.image = image_region
        if money_percent < 100:
            image_region = self.progress_bar_inactive_image.get_region(money_percent * 2, 0,
                                                                       200 - money_percent * 2, 60)
        else:
            image_region = self.progress_bar_inactive_image.get_region(199, 0, 1, 10)

        self.progress_bar_money_inactive.image = image_region
        self.progress_bar_money_inactive.position = (self.money_offset + money_percent * 2, 10)
