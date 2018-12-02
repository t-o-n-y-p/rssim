from .view_base import View
from pyglet.image import load
from pyglet.sprite import Sprite


class GameView(View):
    def __init__(self, surface, batch, groups):
        super().__init__(surface, batch, groups)
        self.screen_resolution = None
        self.game_frame = load('img/main_frame/game_frame_1280_720.png')
        self.game_frame_sprite = None

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

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.game_frame = load('img/main_frame/game_frame_{}_{}.png'.format(self.screen_resolution[0],
                                                                            self.screen_resolution[1]))
        if self.is_activated:
            self.game_frame_sprite.image = self.game_frame

        for b in self.buttons:
            b.on_position_changed((self.screen_resolution[0] - b.x_margin, 0))
