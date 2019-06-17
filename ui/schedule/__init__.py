from logging import getLogger

from pyglet.text import Label

from ui import *
from database import USER_DB_CURSOR
from i18n import I18N_RESOURCES


def row_is_active(fn):
    """
    Use this decorator to execute function only if row is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_row_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_row_is_activated


def row_is_not_active(fn):
    """
    Use this decorator to execute function only if row is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_row_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_row_is_not_activated


class ScheduleRow:
    """
    Implements base class for schedule row.
    """
    def __init__(self, column, row):
        """
        Properties:
            logger                              telemetry instance
            is_activated                        indicates if schedule row is activated
            column                              number of schedule column
            row                                 number of schedule row
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            current_locale                      current locale selected by player
            data                                one row of data from base schedule matrix
            clock_24h_enabled                   indicates if 24h clock is enabled
            main_sprite                         label for all params except departure location
            arrival_sprite                      label for departure location
            screen_resolution                   current game window resolution
            position                            position of the middle point of schedule row
            size                                schedule row width and height
            opacity                             current row opacity

        :param column:                          number of schedule column
        :param row:                             number of schedule row
        """
        self.logger = getLogger(f'root.app.game.map.scheduler.view.row.{column}.{row}')
        self.column, self.row = column, row
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.data = None
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(USER_DB_CURSOR.fetchone()[0])
        self.main_sprite = None
        self.arrival_sprite = None
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.size = (0, 0)
        self.is_activated = False
        self.opacity = 0

    def on_activate(self):
        """
        Activates the schedule row.
        """
        self.is_activated = True

    @row_is_active
    def on_deactivate(self, instant=True):
        """
        Deactivates the schedule row, deletes all labels, deactivates all buttons.

        :param instant:                         indicates if row should be destroyed straight away
        """
        self.is_activated = False
        self.data = []
        if instant:
            self.opacity = 0
            if self.main_sprite is not None:
                self.main_sprite.delete()
                self.main_sprite = None

            if self.arrival_sprite is not None:
                self.arrival_sprite.delete()
                self.arrival_sprite = None

    def on_assign_data(self, data):
        """
        Fully updates data inside the schedule row.

        :param data:                    one row of data from base schedule matrix
        """
        self.data = data
        if self.main_sprite is None:
            self.main_sprite \
                = Label(self.get_main_sprite_text(),
                        font_name='Perfo', bold=True, font_size=self.size[1] // 5 * 3, color=(*WHITE_RGB, self.opacity),
                        x=self.position[0], y=self.position[1], anchor_x='center', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])
        else:
            self.main_sprite.text = self.get_main_sprite_text()

        if self.arrival_sprite is None:
            self.arrival_sprite \
                = Label(I18N_RESOURCES['departed_from_string'][self.current_locale][self.data[DIRECTION]],
                        font_name='Perfo', bold=True, font_size=self.size[1] // 5 * 3, color=(*WHITE_RGB, self.opacity),
                        x=self.position[0] + 5 * self.size[0] // 32, y=self.position[1],
                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                        group=self.groups['button_text'])
        else:
            self.arrival_sprite.text = I18N_RESOURCES['departed_from_string'][self.current_locale][self.data[DIRECTION]]

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        bottom_bar_height = get_bottom_bar_height(self.screen_resolution)
        inner_area_rect = get_inner_area_rect(self.screen_resolution)
        self.size = (int(6.875 * bottom_bar_height), inner_area_rect[3] // (SCHEDULE_ROWS + 1))
        schedule_interval_between_columns = bottom_bar_height // 4
        top_left_row_position = (self.screen_resolution[0] // 2 - self.size[0] // 2
                                 - schedule_interval_between_columns // 2,
                                 self.screen_resolution[1]
                                 - ((self.screen_resolution[1] - bottom_bar_height // 2
                                     - bottom_bar_height - inner_area_rect[3]) // 2
                                    + self.size[1] // 2 * 3)
                                 - bottom_bar_height // 2)
        self.position = (top_left_row_position[0] + self.column * (self.size[0] + schedule_interval_between_columns),
                         top_left_row_position[1] - self.row * self.size[1])
        if self.main_sprite is not None:
            self.main_sprite.x = self.position[0]
            self.main_sprite.y = self.position[1]
            self.main_sprite.font_size = self.size[1] // 5 * 3

        if self.arrival_sprite is not None:
            self.arrival_sprite.x = self.position[0] + 5 * self.size[0] // 32
            self.arrival_sprite.y = self.position[1]
            self.arrival_sprite.font_size = self.size[1] // 5 * 3

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.arrival_sprite is not None:
            self.arrival_sprite.text = I18N_RESOURCES['departed_from_string'][self.current_locale][self.data[DIRECTION]]

        if self.main_sprite is not None:
            self.main_sprite.text = self.get_main_sprite_text()

    def on_update_opacity(self, new_opacity):
        """
        Updates button opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            if self.main_sprite is not None:
                self.main_sprite.delete()
                self.main_sprite = None

            if self.arrival_sprite is not None:
                self.arrival_sprite.delete()
                self.arrival_sprite = None
        else:
            if self.main_sprite is not None:
                self.main_sprite.color = (*WHITE_RGB, self.opacity)

            if self.arrival_sprite is not None:
                self.arrival_sprite.color = (*WHITE_RGB, self.opacity)

    def get_main_sprite_text(self):
        if self.clock_24h_enabled:
            # !!! FIGURE SPACE is used for {3: >2}, not regular space
            return '{0:0>6}       {1:0>2} : {2:0>2}                                     {3: >2}'\
                .format(self.data[TRAIN_ID], (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                        (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR, self.data[CARS])
        else:
            am_pm_index = ((self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_HOUR) // 12 + 1) % 2
            # !!! FIGURE SPACE is used for {1: >2} and {4: >2}, not regular space
            return '{0:0>6}    {1: >2} : {2:0>2} {3}                                  {4: >2}'\
                .format(self.data[TRAIN_ID], (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_HOUR + 11) % 12 + 1,
                        (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
                        I18N_RESOURCES['am_pm_string'][self.current_locale][am_pm_index], self.data[CARS])

    def on_update_clock_state(self, clock_24h_enabled):
        """
        Updates main game clock when clock state is updated.

        :param clock_24h_enabled:               indicates if 24h clock is enabled
        """
        self.clock_24h_enabled = clock_24h_enabled
        if self.main_sprite is not None:
            self.main_sprite.text = self.get_main_sprite_text()
