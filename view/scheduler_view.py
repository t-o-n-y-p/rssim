from logging import getLogger

from pyglet.text import Label

from view import *
from button.close_schedule_button import CloseScheduleButton
from i18n import I18N_RESOURCES


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
            self.controller.on_deactivate_view()

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.map.scheduler.view'))
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
        self.buttons.append(self.close_schedule_button)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.left_schedule_caption_label \
            = Label(I18N_RESOURCES['schedule_caption_string'][self.current_locale],
                    font_name='Arial', bold=True, font_size=self.schedule_caption_font_size,
                    x=self.schedule_left_caption[0], y=self.schedule_left_caption[1],
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        self.right_schedule_caption_label \
            = Label(I18N_RESOURCES['schedule_caption_string'][self.current_locale],
                    font_name='Arial', bold=True, font_size=self.schedule_caption_font_size,
                    x=self.schedule_left_caption[0] + self.schedule_line_step_x, y=self.schedule_left_caption[1],
                    anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                    group=self.groups['button_text'])
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
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
        """
        Updates fade-in/fade-out animations and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        if self.is_activated:
            if self.schedule_opacity < 255:
                self.schedule_opacity += 15

            for i in range(min(len(self.base_schedule), SCHEDULE_ROWS * SCHEDULE_COLUMNS)):
                if self.base_schedule[i][ARRIVAL_TIME] < self.game_time + FRAMES_IN_ONE_HOUR \
                        and len(self.train_labels) < (i + 1) * 2:
                    # 2 sprites are created for each train: departure location (first one)
                    # and all other options (second one)
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
                        Label(I18N_RESOURCES['departed_from_string'][self.current_locale]
                              [self.base_schedule[i][DIRECTION]],
                              font_name='Perfo', bold=True, font_size=self.schedule_font_size,
                              x=self.schedule_departure_top_left_line[0]
                              + self.schedule_line_step_x * (i // SCHEDULE_ROWS),
                              y=self.schedule_departure_top_left_line[1]
                              - (i % SCHEDULE_ROWS) * self.schedule_line_step_y,
                              anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                              group=self.groups['button_text']))
                    break

        if not self.is_activated and self.schedule_opacity > 0:
            self.schedule_opacity -= 15

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
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
                                                   int(self.close_schedule_button.base_font_size_property
                                                       * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin,  b.y_margin))

    def on_update_live_schedule(self, base_schedule, game_time):
        """
        Updates base schedule matrix and game time for on_update() method.

        :param base_schedule                       generated train queue sorted by arrival time
        :param game_time                           current in-game time
        """
        self.base_schedule = base_schedule
        self.game_time = game_time

    @view_is_active
    def on_release_train(self, index):
        """
        Removes train from schedule table once it has arrived to the station entry.

        :param index:                               train position in table (from 0)
        """
        for i in range(index * 2, len(self.train_labels) // 2 - 1):
            self.train_labels[i * 2].text = self.train_labels[(i + 1) * 2].text
            self.train_labels[i * 2 + 1].text = self.train_labels[(i + 1) * 2 + 1].text

        self.train_labels[-2].delete()
        self.train_labels[-1].delete()
        self.train_labels.pop(-2)
        self.train_labels.pop(-1)

    def on_read_ui_info(self):
        """
        Reads aff offsets and font size from the database.
        """
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

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.left_schedule_caption_label.text = I18N_RESOURCES['schedule_caption_string'][self.current_locale]
            self.right_schedule_caption_label.text = I18N_RESOURCES['schedule_caption_string'][self.current_locale]
            for i in range(len(self.train_labels) // 2):
                self.train_labels[i * 2 + 1].text \
                    = I18N_RESOURCES['departed_from_string'][self.current_locale][self.base_schedule[i][DIRECTION]]
