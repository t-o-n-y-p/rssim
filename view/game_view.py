from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import Label
from pyglet.resource import add_font

from .view_base import View
from .button import PauseGameButton, ResumeGameButton


class GameView(View):
    def __init__(self, surface, batch, groups):
        def on_pause_game(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_pause_game()

        def on_resume_game(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_resume_game()

        super().__init__(surface, batch, groups)
        self.screen_resolution = (1280, 720)
        self.game_frame = load('img/main_frame/game_frame_1280_720.png')
        self.game_frame_sprite = None
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
        self.game_time = 0

    def on_update(self):
        if self.is_activated and self.game_frame_sprite.opacity < 255:
            self.game_frame_sprite.opacity += 15

        if not self.is_activated and self.game_frame_sprite is not None:
            if self.game_frame_sprite.opacity > 0:
                self.game_frame_sprite.opacity -= 15
                if self.game_frame_sprite.opacity <= 0:
                    self.game_frame_sprite.delete()
                    self.game_frame_sprite = None

    def on_activate(self):
        self.is_activated = True
        if self.game_frame_sprite is None:
            self.game_frame_sprite = Sprite(self.game_frame, x=0, y=0, batch=self.batch,
                                            group=self.groups['main_frame'])
            self.game_frame_sprite.opacity = 0

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

    def on_deactivate(self):
        self.is_activated = False
        self.day_sprite.delete()
        self.day_sprite = None
        self.time_sprite.delete()
        self.time_sprite = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.game_frame = load('img/main_frame/game_frame_{}_{}.png'.format(screen_resolution[0], screen_resolution[1]))
        if self.is_activated:
            self.game_frame_sprite.image = self.game_frame

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
