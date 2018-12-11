from pyglet.text import Label
from pyglet.image import load
from pyglet.sprite import Sprite

from .view_base import View
from .button import CloseScheduleButton


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


class SchedulerView(View):
    def __init__(self, surface, batch, groups):
        def on_close_schedule(button):
            self.controller.on_deactivate()

        super().__init__(surface, batch, groups)
        self.departure_text = ['West City', 'East City', 'North-West City', 'South-East City']
        self.screen_resolution = (1280, 720)
        self.background_image = load('img/main_frame/schedule_1280_720.png')
        self.background_sprite = None
        self.train_labels = []
        self.close_schedule_button = CloseScheduleButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                         on_click_action=on_close_schedule)
        self.buttons.append(self.close_schedule_button)

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if self.background_sprite is None:
            self.background_sprite = Sprite(self.background_image, x=0, y=78, batch=self.batch,
                                            group=self.groups['main_frame'])
            self.background_sprite.opacity = 0

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for label in self.train_labels:
            label.delete()

        self.train_labels.clear()
        for b in self.buttons:
            b.on_deactivate()

    def on_update(self):
        if self.is_activated and self.background_sprite.opacity < 255:
            self.background_sprite.opacity += 15

        if not self.is_activated and self.background_sprite is not None:
            if self.background_sprite.opacity > 0:
                self.background_sprite.opacity -= 15
                if self.background_sprite.opacity <= 0:
                    self.background_sprite.delete()
                    self.background_sprite = None

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        if self.is_activated:
            for i in range(len(self.train_labels) // 2):
                self.train_labels[i * 2].x = (self.screen_resolution[0] // 2 - 320) + 640 * (i // 16)
                self.train_labels[i * 2].y = (self.screen_resolution[1] - 165) - (i % 16) * 27
                self.train_labels[i * 2 + 1].x = (self.screen_resolution[0] // 2 - 287) + 640 * (i // 16)
                self.train_labels[i * 2 + 1].y = (self.screen_resolution[1] - 165) - (i % 16) * 27

        self.close_schedule_button.y_margin = self.screen_resolution[1]
        for b in self.buttons:
            b.on_position_changed((screen_resolution[0] - b.x_margin, screen_resolution[1] - b.y_margin))

    @_view_is_active
    def on_update_train_labels(self, base_schedule, game_time):
        for i in range(min(len(base_schedule), 32)):
            if base_schedule[i][1] < game_time + 14400 and len(self.train_labels) < (i + 1) * 2:
                self.train_labels.append(
                    Label('{0:0>6}   {1:0>2} : {2:0>2}                           {3:0>2}   {4:0>2} : {5:0>2}'
                          .format(base_schedule[i][0], (base_schedule[i][1] // 14400 + 12) % 24,
                                  (base_schedule[i][1] // 240) % 60, base_schedule[i][4], base_schedule[i][5] // 240,
                                  (base_schedule[i][5] // 4) % 60),
                          font_name='Perfo', bold=True, font_size=18,
                          x=(self.screen_resolution[0] // 2 - 320) + 640 * (i // 16),
                          y=(self.screen_resolution[1] - 165) - (i % 16) * 27, anchor_x='center', anchor_y='center',
                          batch=self.batch, group=self.groups['button_text']))
                self.train_labels.append(
                    Label(self.departure_text[base_schedule[i][2]], font_name='Perfo', bold=True, font_size=18,
                          x=(self.screen_resolution[0] // 2 - 287) + 640 * (i // 16),
                          y=(self.screen_resolution[1] - 165) - (i % 16) * 27, anchor_x='center', anchor_y='center',
                          batch=self.batch, group=self.groups['button_text']))
                break

