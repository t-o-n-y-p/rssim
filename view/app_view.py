from sys import exit

from .view_base import View
from pyglet.image import load
from pyglet.sprite import Sprite
from .button import CloseGameButton, IconifyGameButton


class AppView(View):
    def __init__(self, game_config, surface, batch, groups):
        def on_close_game(button):
            self.surface.close()
            exit()

        def on_iconify_game(button):
            self.surface.minimize()

        super().__init__(game_config, surface, batch, groups)
        self.is_activated = True
        self.screen_resolution = self.game_config.screen_resolution
        self.main_frame = None
        self.main_frame_sprite = None
        self.buttons.append(CloseGameButton(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                            groups=self.groups, on_click_action=on_close_game))
        self.buttons.append(IconifyGameButton(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                              groups=self.groups, on_click_action=on_iconify_game))

    def on_update(self):
        if self.is_activated and self.main_frame_sprite.opacity < 255:
            self.main_frame_sprite.opacity += 15

        if not self.is_activated and self.main_frame_sprite is not None:
            if self.main_frame_sprite.opacity > 0:
                self.main_frame_sprite.opacity -= 15
                if self.main_frame_sprite.opacity <= 0:
                    self.main_frame_sprite.delete()
                    self.main_frame_sprite = None

    def on_activate(self):
        self.is_activated = True
        self.main_frame = load('img/main_frame/main_frame_{}_{}.png'.format(self.screen_resolution[0],
                                                                            self.screen_resolution[1]))
        self.main_frame_sprite = Sprite(self.main_frame, x=0, y=0, batch=self.batch, group=self.groups['main_frame'])
        self.main_frame_sprite.opacity = 0

    def on_deactivate(self):
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.main_frame_sprite.image = load('img/main_frame/main_frame_{}_{}.png'.format(self.screen_resolution[0],
                                                                                         self.screen_resolution[1]))
