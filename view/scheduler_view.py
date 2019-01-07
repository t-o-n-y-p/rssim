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
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        def on_close_schedule(button):
            self.controller.on_deactivate_view()

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.departure_text = ['West City', 'East City', 'North-West City', 'South-East City']
        self.screen_resolution = (1280, 720)
        self.background_image = load('img/schedule/schedule_1280_720.png')
        self.background_sprite = None
        self.schedule_top_left_line = [0, 0]
        self.schedule_departure_top_left_line = [0, 0]
        self.schedule_line_step_x = 0
        self.schedule_line_step_y = 0
        self.schedule_font_size = 0
        self.on_read_ui_info()
        self.train_labels = []
        self.close_schedule_button = CloseScheduleButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                         on_click_action=on_close_schedule)
        self.buttons.append(self.close_schedule_button)
        self.base_train_id = 0
        self.base_arrival_time = 1
        self.base_direction = 2
        self.base_new_direction = 3
        self.base_cars = 4
        self.base_stop_time = 5
        self.base_exp = 6
        self.base_money = 7

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
        self.background_image = load('img/schedule/schedule_{}_{}.png'
                                     .format(self.screen_resolution[0], self.screen_resolution[1]))
        self.on_read_ui_info()
        if self.is_activated:
            self.background_sprite.image = self.background_image
            for i in range(len(self.train_labels) // 2):
                self.train_labels[i * 2].x = self.schedule_top_left_line[0] + self.schedule_line_step_x * (i // 16)
                self.train_labels[i * 2].y = self.schedule_top_left_line[1] - (i % 16) * self.schedule_line_step_y
                self.train_labels[i * 2].font_size = self.schedule_font_size
                self.train_labels[i * 2 + 1].x \
                    = self.schedule_departure_top_left_line[0] + self.schedule_line_step_x * (i // 16)
                self.train_labels[i * 2 + 1].y \
                    = self.schedule_departure_top_left_line[1] - (i % 16) * self.schedule_line_step_y
                self.train_labels[i * 2 + 1].font_size = self.schedule_font_size

        self.close_schedule_button.y_margin = self.screen_resolution[1]
        for b in self.buttons:
            b.on_position_changed((screen_resolution[0] - b.x_margin, screen_resolution[1] - b.y_margin))

    @_view_is_active
    def on_update_train_labels(self, base_schedule, game_time):
        for i in range(min(len(base_schedule), 32)):
            if base_schedule[i][1] < game_time + 14400 and len(self.train_labels) < (i + 1) * 2:
                self.train_labels.append(
                    Label('{0:0>6}    {1:0>2} : {2:0>2}                             {3:0>2}   {4:0>2} : {5:0>2}'
                          .format(base_schedule[i][self.base_train_id],
                                  (base_schedule[i][self.base_arrival_time] // 14400 + 12) % 24,
                                  (base_schedule[i][self.base_arrival_time] // 240) % 60,
                                  base_schedule[i][self.base_cars], base_schedule[i][self.base_stop_time] // 240,
                                  (base_schedule[i][self.base_stop_time] // 4) % 60),
                          font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                          x=self.schedule_top_left_line[0] + self.schedule_line_step_x * (i // 16),
                          y=self.schedule_top_left_line[1] - (i % 16) * self.schedule_line_step_y,
                          anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']))
                self.train_labels.append(
                    Label(self.departure_text[base_schedule[i][self.base_direction]],
                          font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                          x=self.schedule_departure_top_left_line[0] + self.schedule_line_step_x * (i // 16),
                          y=self.schedule_departure_top_left_line[1] - (i % 16) * self.schedule_line_step_y,
                          anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']))
                break

    @_view_is_active
    def on_release_train(self, index):
        for i in range(index * 2, len(self.train_labels) // 2 - 1):
            self.train_labels[i * 2].text = self.train_labels[(i + 1) * 2].text
            self.train_labels[i * 2 + 1].text = self.train_labels[(i + 1) * 2 + 1].text

        self.train_labels[-2].delete()
        self.train_labels[-1].delete()
        self.train_labels.pop(-2)
        self.train_labels.pop(-1)

    def on_read_ui_info(self):
        self.config_db_cursor.execute('''SELECT schedule_top_left_line_x, schedule_top_left_line_y,
                                         schedule_departure_top_left_line_x, schedule_departure_top_left_line_y,
                                         schedule_line_step_x, schedule_line_step_y, schedule_font_size
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.schedule_top_left_line[0], self.schedule_top_left_line[1], \
            self.schedule_departure_top_left_line[0], self.schedule_departure_top_left_line[1], \
            self.schedule_line_step_x, self.schedule_line_step_y, self.schedule_font_size \
            = self.config_db_cursor.fetchone()
