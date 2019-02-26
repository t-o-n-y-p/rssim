from logging import getLogger

from pyglet.text import Label

from view import *
from button.close_schedule_button import CloseScheduleButton


class SchedulerView(View):
    """
    Implements Scheduler view.
    Scheduler object is responsible for properties, UI and events related to the train schedule.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_close_schedule                   on_click handler for close schedule button

        Properties:
            schedule_opacity                    general opacity of the schedule screen
            schedule_top_left_line              position of schedule top left line label
            schedule_departure_top_left_line    position of schedule top left line departure label
            schedule_line_step_x                distance between two schedule rows
            schedule_line_step_y                distance between two schedule columns
            schedule_font_size                  font size for schedule table
            schedule_left_caption               position of schedule caption for left column
            schedule_caption_font_size          font size for schedule caption
            train_labels    `                   schedule table labels
            base_schedule                       generated train queue sorted by arrival time
            game_time                           current in-game time
            left_schedule_caption_label         label from caption for left schedule column
            right_schedule_caption_label        label from caption for right schedule column
            close_schedule_button               CloseScheduleButton object
            buttons                             list of all buttons

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        def on_close_schedule(button):
            """
            Notifies controller that player has closed schedule screen.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_CLOSE_SCHEDULE')
            self.controller.on_deactivate_view()
            self.logger.info('END ON_CLOSE_SCHEDULE')

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.map.scheduler.view'))
        self.logger.info('START INIT')
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
        self.left_schedule_caption_label = None
        self.right_schedule_caption_label = None
        self.close_schedule_button = CloseScheduleButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                         groups=self.groups, on_click_action=on_close_schedule)
        self.logger.debug('buttons created successfully')
        self.buttons.append(self.close_schedule_button)
        self.logger.debug(f'buttons list length: {len(self.buttons)}')
        self.logger.info('END INIT')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.left_schedule_caption_label \
            = Label('Train #          Arrival          Departed from       Cars   Stop, m:s',
                    font_name='Arial', bold=True, font_size=self.schedule_caption_font_size,
                    x=self.schedule_left_caption[0], y=self.schedule_left_caption[1],
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.logger.debug(f'left_schedule_caption_label text: {self.left_schedule_caption_label.text}')
        self.logger.debug('left_schedule_caption_label position: {}'
                          .format((self.left_schedule_caption_label.x, self.left_schedule_caption_label.y)))
        self.logger.debug(f'left_schedule_caption_label font size: {self.left_schedule_caption_label.font_size}')
        self.right_schedule_caption_label \
            = Label('Train #          Arrival          Departed from       Cars   Stop, m:s',
                    font_name='Arial', bold=True, font_size=self.schedule_caption_font_size,
                    x=self.schedule_left_caption[0] + self.schedule_line_step_x, y=self.schedule_left_caption[1],
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.logger.debug(f'right_schedule_caption_label text: {self.right_schedule_caption_label.text}')
        self.logger.debug('right_schedule_caption_label position: {}'
                          .format((self.right_schedule_caption_label.x, self.right_schedule_caption_label.y)))
        self.logger.debug(f'right_schedule_caption_label font size: {self.right_schedule_caption_label.font_size}')
        for b in self.buttons:
            self.logger.debug(f'button: {b.__class__.__name__}')
            self.logger.debug(f'to_activate_on_controller_init: {b.to_activate_on_controller_init}')
            if b.to_activate_on_controller_init:
                b.on_activate()

        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.left_schedule_caption_label.delete()
        self.left_schedule_caption_label = None
        self.right_schedule_caption_label.delete()
        self.right_schedule_caption_label = None
        for label in self.train_labels:
            label.delete()

        self.train_labels.clear()
        for b in self.buttons:
            b.on_deactivate()

    def on_update(self):
        if self.is_activated:
            if self.schedule_opacity < 255:
                self.schedule_opacity += 15

            for i in range(min(len(self.base_schedule), SCHEDULE_ROWS * SCHEDULE_COLUMNS)):
                if self.base_schedule[i][1] < self.game_time + FRAMES_IN_ONE_HOUR \
                        and len(self.train_labels) < (i + 1) * 2:
                    self.train_labels.append(
                        Label('{0:0>6}    {1:0>2} : {2:0>2}                             {3:0>2}   {4:0>2} : {5:0>2}'
                              .format(self.base_schedule[i][TRAIN_ID],
                                      (self.base_schedule[i][ARRIVAL_TIME] // FRAMES_IN_ONE_HOUR + 12)
                                      % HOURS_IN_ONE_DAY,
                                      (self.base_schedule[i][ARRIVAL_TIME] // FRAMES_IN_ONE_MINUTE)
                                      % MINUTES_IN_ONE_HOUR,
                                      self.base_schedule[i][CARS],
                                      self.base_schedule[i][STOP_TIME] // FRAMES_IN_ONE_MINUTE,
                                      (self.base_schedule[i][STOP_TIME] // FRAMES_IN_ONE_SECOND)
                                      % SECONDS_IN_ONE_MINUTE),
                              font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                              x=self.schedule_top_left_line[0] + self.schedule_line_step_x * (i // SCHEDULE_ROWS),
                              y=self.schedule_top_left_line[1] - (i % SCHEDULE_ROWS) * self.schedule_line_step_y,
                              anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                              group=self.groups['button_text']))
                    self.train_labels.append(
                        Label(DEPARTURE_TEXT[self.base_schedule[i][DIRECTION]],
                              font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                              x=self.schedule_departure_top_left_line[0]
                                + self.schedule_line_step_x * (i // SCHEDULE_ROWS),
                              y=self.schedule_departure_top_left_line[1]
                                - (i % SCHEDULE_ROWS) * self.schedule_line_step_y,
                              anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                              group=self.groups['button_text']))
                    break

        if not self.is_activated:
            if self.schedule_opacity > 0:
                self.schedule_opacity -= 15

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.on_read_ui_info()
        if self.is_activated:
            self.left_schedule_caption_label.x = self.schedule_left_caption[0]
            self.left_schedule_caption_label.y = self.schedule_left_caption[1]
            self.left_schedule_caption_label.font_size = self.schedule_caption_font_size
            self.right_schedule_caption_label.x = self.schedule_left_caption[0] + self.schedule_line_step_x
            self.right_schedule_caption_label.y = self.schedule_left_caption[1]
            self.right_schedule_caption_label.font_size = self.schedule_caption_font_size
            for i in range(len(self.train_labels) // 2):
                self.train_labels[i * 2].x = self.schedule_top_left_line[0] \
                                           + self.schedule_line_step_x * (i // SCHEDULE_ROWS)
                self.train_labels[i * 2].y = self.schedule_top_left_line[1] \
                                           - (i % SCHEDULE_ROWS) * self.schedule_line_step_y
                self.train_labels[i * 2].font_size = self.schedule_font_size
                self.train_labels[i * 2 + 1].x \
                    = self.schedule_departure_top_left_line[0] + self.schedule_line_step_x * (i // SCHEDULE_ROWS)
                self.train_labels[i * 2 + 1].y \
                    = self.schedule_departure_top_left_line[1] - (i % SCHEDULE_ROWS) * self.schedule_line_step_y
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

    @view_is_active
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
