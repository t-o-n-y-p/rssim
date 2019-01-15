from pyglet.text import Label

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
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        def on_close_schedule(button):
            self.controller.on_deactivate_view()

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups)
        self.departure_text = ['West City', 'East City', 'North-West City', 'South-East City']
        self.screen_resolution = (1280, 720)
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.schedule_opacity = 0
        self.schedule_top_left_line = [0, 0]
        self.schedule_departure_top_left_line = [0, 0]
        self.schedule_line_step_x = 0
        self.schedule_line_step_y = 0
        self.schedule_font_size = 0
        self.schedule_left_caption = [0, 0]
        self.schedule_caption_font_size = 0
        self.on_read_ui_info()
        self.train_labels = []
        self.base_schedule = None
        self.game_time = None
        self.left_schedule_caption_sprite = None
        self.right_schedule_caption_sprite = None
        self.close_schedule_button = CloseScheduleButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                         groups=self.groups, on_click_action=on_close_schedule)
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
        self.left_schedule_caption_sprite \
            = Label('Train #          Arrival          Departed from       Cars   Stop, m:s',
                    font_name='Arial', bold=True, font_size=self.schedule_caption_font_size,
                    x=self.schedule_left_caption[0], y=self.schedule_left_caption[1],
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.right_schedule_caption_sprite \
            = Label('Train #          Arrival          Departed from       Cars   Stop, m:s',
                    font_name='Arial', bold=True, font_size=self.schedule_caption_font_size,
                    x=self.schedule_left_caption[0] + self.schedule_line_step_x, y=self.schedule_left_caption[1],
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.left_schedule_caption_sprite.delete()
        self.left_schedule_caption_sprite = None
        self.right_schedule_caption_sprite.delete()
        self.right_schedule_caption_sprite = None
        for label in self.train_labels:
            label.delete()

        self.train_labels.clear()
        for b in self.buttons:
            b.on_deactivate()

    def on_update(self):
        if self.is_activated:
            if self.schedule_opacity < 255:
                self.schedule_opacity += 15

            for i in range(min(len(self.base_schedule), 32)):
                if self.base_schedule[i][1] < self.game_time + 14400 and len(self.train_labels) < (i + 1) * 2:
                    self.train_labels.append(
                        Label('{0:0>6}    {1:0>2} : {2:0>2}                             {3:0>2}   {4:0>2} : {5:0>2}'
                              .format(self.base_schedule[i][self.base_train_id],
                                      (self.base_schedule[i][self.base_arrival_time] // 14400 + 12) % 24,
                                      (self.base_schedule[i][self.base_arrival_time] // 240) % 60,
                                      self.base_schedule[i][self.base_cars],
                                      self.base_schedule[i][self.base_stop_time] // 240,
                                      (self.base_schedule[i][self.base_stop_time] // 4) % 60),
                              font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                              x=self.schedule_top_left_line[0] + self.schedule_line_step_x * (i // 16),
                              y=self.schedule_top_left_line[1] - (i % 16) * self.schedule_line_step_y,
                              anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                              group=self.groups['button_text']))
                    self.train_labels.append(
                        Label(self.departure_text[self.base_schedule[i][self.base_direction]],
                              font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                              x=self.schedule_departure_top_left_line[0] + self.schedule_line_step_x * (i // 16),
                              y=self.schedule_departure_top_left_line[1] - (i % 16) * self.schedule_line_step_y,
                              anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                              group=self.groups['button_text']))
                    break

        if not self.is_activated:
            if self.schedule_opacity > 0:
                self.schedule_opacity -= 15

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.on_read_ui_info()
        if self.is_activated:
            self.left_schedule_caption_sprite.x = self.schedule_left_caption[0]
            self.left_schedule_caption_sprite.y = self.schedule_left_caption[1]
            self.left_schedule_caption_sprite.font_size = self.schedule_caption_font_size
            self.right_schedule_caption_sprite.x = self.schedule_left_caption[0] + self.schedule_line_step_x
            self.right_schedule_caption_sprite.y = self.schedule_left_caption[1]
            self.right_schedule_caption_sprite.font_size = self.schedule_caption_font_size
            for i in range(len(self.train_labels) // 2):
                self.train_labels[i * 2].x = self.schedule_top_left_line[0] + self.schedule_line_step_x * (i // 16)
                self.train_labels[i * 2].y = self.schedule_top_left_line[1] - (i % 16) * self.schedule_line_step_y
                self.train_labels[i * 2].font_size = self.schedule_font_size
                self.train_labels[i * 2 + 1].x \
                    = self.schedule_departure_top_left_line[0] + self.schedule_line_step_x * (i // 16)
                self.train_labels[i * 2 + 1].y \
                    = self.schedule_departure_top_left_line[1] - (i % 16) * self.schedule_line_step_y
                self.train_labels[i * 2 + 1].font_size = self.schedule_font_size

        self.close_schedule_button.x_margin = self.screen_resolution[0] - 11 * self.bottom_bar_height // 2 + 2
        self.close_schedule_button.y_margin = 0
        self.close_schedule_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                   int(24 / 80 * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin,  b.y_margin))

    def on_update_train_labels(self, base_schedule, game_time):
        self.base_schedule = base_schedule
        self.game_time = game_time

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
                                         schedule_line_step_x, schedule_line_step_y, schedule_font_size,
                                         schedule_left_caption_x, schedule_left_caption_y, 
                                         schedule_caption_font_size
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.schedule_top_left_line[0], self.schedule_top_left_line[1], \
            self.schedule_departure_top_left_line[0], self.schedule_departure_top_left_line[1], \
            self.schedule_line_step_x, self.schedule_line_step_y, self.schedule_font_size, \
            self.schedule_left_caption[0], self.schedule_left_caption[1], self.schedule_caption_font_size \
            = self.config_db_cursor.fetchone()
