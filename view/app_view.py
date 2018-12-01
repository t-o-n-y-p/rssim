from .view_base import View
from pyglet.image import load
from pyglet.sprite import Sprite
from .button import CloseGameButton, IconifyGameButton, FullscreenButton, RestoreButton


class AppView(View):
    def __init__(self, game_config, surface, batch, groups):
        def on_close_game(button):
            self.controller.on_close_game()

        def on_iconify_game(button):
            self.surface.minimize()

        def on_app_window_fullscreen(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_fullscreen_mode_turned_on()

        def on_app_window_restore(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_fullscreen_mode_turned_off()

        super().__init__(game_config, surface, batch, groups)
        self.screen_resolution = None
        self.main_frame = None
        self.main_frame_sprite = None
        self.buttons.append(CloseGameButton(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                            groups=self.groups, on_click_action=on_close_game))
        self.buttons.append(IconifyGameButton(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                              groups=self.groups, on_click_action=on_iconify_game))
        fullscreen_button = FullscreenButton(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                             groups=self.groups, on_click_action=on_app_window_fullscreen)
        restore_button = RestoreButton(game_config=self.game_config, surface=self.surface, batch=self.batch,
                                       groups=self.groups, on_click_action=on_app_window_restore)
        fullscreen_button.paired_button = restore_button
        restore_button.paired_button = fullscreen_button
        self.buttons.append(fullscreen_button)
        self.buttons.append(restore_button)

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
        self.main_frame_sprite = Sprite(self.main_frame, x=0, y=0, batch=self.batch, group=self.groups['main_frame'])
        self.main_frame_sprite.opacity = 0
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.main_frame = load('img/main_frame/main_frame_{}_{}.png'.format(self.screen_resolution[0],
                                                                            self.screen_resolution[1]))
        if self.is_activated:
            self.main_frame_sprite.image = self.main_frame

        for b in self.buttons:
            b.on_position_changed((self.screen_resolution[0] - b.x_margin, self.screen_resolution[1] - b.y_margin))

    def on_fullscreen_mode_turned_on(self):
        self.surface.set_fullscreen(fullscreen=True)

    def on_fullscreen_mode_turned_off(self):
        self.surface.set_fullscreen(fullscreen=False)
