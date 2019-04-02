from logging import getLogger

from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui.button import create_two_state_button
from ui.button.build_construction_button import BuildConstructionButton
from ui.button.set_money_target_button import SetMoneyTargetButton
from ui.button.reset_money_target_button import ResetMoneyTargetButton
from ui.button.checked_checkbox_button import CheckedCheckboxButton
from ui.button.unchecked_checkbox_button import UncheckedCheckboxButton


# --------------------- CONSTANTS ---------------------
SCHEDULE_ROWS = 12                              # number of schedule rows on schedule screen
SCHEDULE_COLUMNS = 2                            # number of schedule columns on schedule screen
# track and environment state matrix properties
LOCKED = 0                                      # property #0 indicates if track/env. is locked
UNDER_CONSTRUCTION = 1                          # property #1 indicates if track/env. is under construction
CONSTRUCTION_TIME = 2                           # property #2 indicates construction time left
UNLOCK_CONDITION_FROM_LEVEL = 3                 # property #3 indicates if unlock condition from level is met
UNLOCK_CONDITION_FROM_PREVIOUS_TRACK = 4        # property #4 indicates if unlock condition from previous track is met
UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT = 4  # property #4 indicates if unlock condition from previous env. is met
UNLOCK_CONDITION_FROM_ENVIRONMENT = 5           # property #5 indicates if unlock condition from environment is met
UNLOCK_AVAILABLE = 6                            # property #6 indicates if all unlock conditions are met
PRICE = 7                                       # property #7 indicates track/env. price
LEVEL_REQUIRED = 8                              # property #8 indicates required level for this track/env.
ENVIRONMENT_REQUIRED = 9                        # property #9 indicates required environment tier for this track
# colors
GREY = (112, 112, 112, 255)                     # grey UI color
ORANGE = (255, 127, 0, 255)                     # orange UI color
GREEN = (0, 192, 0, 255)                        # green UI color
RED = (255, 0, 0, 255)                          # red UI color
# time
FRAMES_IN_ONE_DAY = 345600                      # indicates how many frames fit in one in-game day
FRAMES_IN_ONE_HOUR = 14400                      # indicates how many frames fit in one in-game hour
FRAMES_IN_ONE_MINUTE = 240                      # indicates how many frames fit in one in-game minute
FRAMES_IN_ONE_SECOND = 4                        # indicates how many frames fit in one in-game second
MINUTES_IN_ONE_HOUR = 60
SECONDS_IN_ONE_MINUTE = 60
HOURS_IN_ONE_DAY = 24
# base_schedule matrix properties
TRAIN_ID = 0                                    # property #0 indicates train identification number
ARRIVAL_TIME = 1                                # property #1 indicates arrival time
DIRECTION = 2                                   # property #2 indicates direction
NEW_DIRECTION = 3                               # property #3 indicates new direction
CARS = 4                                        # property #4 indicates number of cars
STOP_TIME = 5                                   # property #5 indicates how much stop time left
EXP = 6                                         # property #6 indicates how much exp the train gives
MONEY = 7                                       # property #7 indicates how much money the train gives
# ------------------- END CONSTANTS -------------------


def cell_is_active(fn):
    """
    Use this decorator to execute function only if cell is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_cell_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_cell_is_activated


def cell_is_not_active(fn):
    """
    Use this decorator to execute function only if cell is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_cell_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_cell_is_not_activated


def row_is_active(fn):
    """
    Use this decorator to execute function only if cell is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_row_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_row_is_activated


def row_is_not_active(fn):
    """
    Use this decorator to execute function only if cell is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_row_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_row_is_not_activated


class ConstructorCell:
    """
    Implements base class for constructor cell.
    """
    def __init__(self, construction_type, row, surface, batches, groups, current_locale,
                 on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action):
        """
        Button click handlers:
            on_set_money_target                 on_click handler for set money target button
            on_reset_money_target               on_click handler for reset money target button
            on_buy_construction                 on_click handler for build construction button

        Properties:
            logger                              telemetry instance
            is_activated                        indicates if cell is active
            construction_type                   type of construction: track or environment
            row                                 number of cell on constructor screen
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            current_locale                      current locale selected by player
            on_buy_construction_action          is activated when player buys construction
            on_set_money_target_action          is activated when money target is activated by player
            on_reset_money_target_action        is activated when money target is deactivated by player
            entity_number                       number of track or environment tier
            data                                one row of data from construction state matrix
            screen_resolution                   current game window resolution
            position                            position of the left bottom corner of the cell
            size                                cell width and height
            locked_label                        label for locked entity or not enough money case
            title_key                           resource key for cell title
            title_label                         label for cell title
            description_keys                    dictionary of resource keys for cell description
            description_label                   label for cell description
            placeholder_key                     resource key for cell placeholder
            placeholder_label                   label for cell placeholder
            enable_money_target_button          SetMoneyTargetButton object
            disable_money_target_button         ResetMoneyTargetButton object
            build_button                        BuildConstructionButton object
            buttons                             list of all buttons
            money                               amount of money the player can operate
            money_target_activated              indicates if money target is activated for this cell

        :param construction_type:               type of construction: track or environment
        :param row:                             number of cell on constructor screen
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        :param current_locale:                  current locale selected by player
        :param on_buy_construction_action:      is activated when player buys construction
        :param on_set_money_target_action:      is activated when money target is activated by player
        :param on_reset_money_target_action:    is activated when money target is deactivated by player
        """
        def on_set_money_target(button):
            """
            Deactivates set target button, activated reset target button.
            Notifies the view about money target update.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.on_set_money_target_action(self.construction_type, self.row, self.entity_number)

        def on_reset_money_target(button):
            """
            Deactivates reset target button, activated set target button.
            Notifies the view about money target update.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.on_reset_money_target_action()

        def on_buy_construction(button):
            """
            Deactivates all buttons. Notifies the view about construction state update.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.enable_money_target_button.on_deactivate()
            self.disable_money_target_button.on_deactivate()
            self.on_buy_construction_action(self.construction_type, self.row, self.entity_number)

        self.logger = getLogger(f'root.app.game.map.constructor.view.cell.{construction_type}.{row}')
        self.is_activated = False
        self.construction_type, self.row = construction_type, row
        self.surface, self.batches, self.groups, self.current_locale = surface, batches, groups, current_locale
        self.on_buy_construction_action = on_buy_construction_action
        self.on_set_money_target_action = on_set_money_target_action
        self.on_reset_money_target_action = on_reset_money_target_action
        self.entity_number = None
        self.data = None
        self.screen_resolution = (0, 0)
        self.position = [0, 0]
        self.size = [0, 0]
        self.locked_label = None
        self.title_key = None
        self.title_label = None
        self.description_keys = {}
        self.description_label = None
        self.placeholder_key = None
        self.placeholder_label = None
        self.enable_money_target_button, self.disable_money_target_button \
            = create_two_state_button(SetMoneyTargetButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                           groups=self.groups, on_click_action=on_set_money_target),
                                      ResetMoneyTargetButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                             groups=self.groups, on_click_action=on_reset_money_target))
        self.build_button = BuildConstructionButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                    groups=self.groups, on_click_action=on_buy_construction)
        self.buttons = [self.enable_money_target_button, self.disable_money_target_button, self.build_button]
        self.money = 0
        self.money_target_activated = False

    @cell_is_active
    def on_assign_new_data(self, entity_number, data):
        """
        Fully updates data inside the cell.

        :param entity_number:           number of the track or environment tier
        :param data:                    one row of data from construction state matrix
        """
        self.entity_number = entity_number
        self.data = data
        # when data is empty, it means no more tracks/tiers are available, only placeholder is active
        if len(self.data) == 0 or self.entity_number == 0:
            if self.placeholder_label is None:
                self.placeholder_label = Label(I18N_RESOURCES[self.placeholder_key][self.current_locale],
                                               font_name='Arial', font_size=int(11 * self.size[1] / 40), color=GREY,
                                               x=self.position[0] + self.size[0] // 2,
                                               y=self.position[1] + self.size[1] // 2,
                                               anchor_x='center', anchor_y='center',
                                               batch=self.batches['ui_batch'], group=self.groups['button_text'])
            else:
                self.placeholder_label.text = I18N_RESOURCES[self.placeholder_key][self.current_locale]

            if self.locked_label is not None:
                self.locked_label.delete()
                self.locked_label = None

            if self.title_label is not None:
                self.title_label.delete()
                self.title_label = None

            if self.description_label is not None:
                self.description_label.delete()
                self.description_label = None

            for b in self.buttons:
                b.on_deactivate()

        else:
            if self.placeholder_label is not None:
                self.placeholder_label.delete()
                self.placeholder_label = None

            if not self.data[UNLOCK_AVAILABLE] and not self.data[UNDER_CONSTRUCTION]:
                if self.locked_label is None:
                    self.locked_label = Label('', font_name='Webdings',
                                              font_size=int(self.build_button.base_font_size_property * self.size[1]),
                                              color=GREY, x=self.position[0] + self.size[0] - self.size[1] // 2,
                                              y=self.position[1] + self.size[1] // 2,
                                              anchor_x='center', anchor_y='center',
                                              batch=self.batches['ui_batch'], group=self.groups['button_text'])
                else:
                    self.locked_label.text = ''

            if self.title_label is None:
                self.title_label = Label(I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number),
                                         font_name='Arial', font_size=int(0.3 * self.size[1]),
                                         x=self.position[0] + self.size[1] // 8,
                                         y=self.position[1] + int(0.7 * self.size[1]),
                                         anchor_x='left', anchor_y='center',
                                         batch=self.batches['ui_batch'], group=self.groups['button_text'])
            else:
                self.title_label.text = I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number)

            if self.description_label is None:
                self.description_label = Label(' ', font_name='Arial', font_size=self.size[1] // 5, color=GREY,
                                               x=self.position[0] + self.size[1] // 8,
                                               y=self.position[1] + int(22 * self.size[1] / 80),
                                               anchor_x='left', anchor_y='center',
                                               batch=self.batches['ui_batch'], group=self.groups['button_text'])

            self.on_update_description_label()
            self.on_update_build_button_state()

    def on_update_description_label(self):
        """
        Updates cell description based on data.
        Different constructions have different states, so this method must be overridden by subclasses.
        """
        pass

    @cell_is_active
    def on_update_state(self, data):
        """
        Updates buttons and description state.

        :param data:                    one row of data from construction state matrix
        """
        self.data = data
        # when UNLOCK_AVAILABLE flag becomes enabled, we need to activate build button
        # (or locked label if there is no enough money) and set money target button
        if self.data[UNLOCK_AVAILABLE]:
            self.on_update_build_button_state()
            if not self.money_target_activated and not self.enable_money_target_button.is_activated \
                    and not self.disable_money_target_button.is_activated:
                self.on_deactivate_money_target()

        if self.is_activated:
            self.on_update_description_label()

    def on_update_money(self, money):
        """
        Updates cell state based on available money.

        :param money:                   amount of money the player can operate
        """
        self.money = money
        self.on_update_build_button_state()

    @cell_is_active
    def on_update_build_button_state(self):
        """
        Updates locked label and build button state based on available money.
        """
        if self.data[UNLOCK_AVAILABLE]:
            if self.money >= self.data[PRICE]:
                self.build_button.on_activate()
                if self.locked_label is not None:
                    self.locked_label.delete()
                    self.locked_label = None

            else:
                self.build_button.on_deactivate()
                if self.locked_label is None:
                    self.locked_label = Label('', font_name='Webdings',
                                              font_size=int(self.build_button.base_font_size_property * self.size[1]),
                                              color=GREY, x=self.position[0] + self.size[0] - self.size[1] // 2,
                                              y=self.position[1] + self.size[1] // 2,
                                              anchor_x='center', anchor_y='center',
                                              batch=self.batches['ui_batch'], group=self.groups['button_text'])
                else:
                    self.locked_label.text = ''

    @cell_is_not_active
    def on_activate(self):
        """
        Activates the cell.
        """
        self.is_activated = True

    @cell_is_active
    def on_deactivate(self):
        """
        Deactivates the cell, deletes all labels, deactivates all buttons.
        """
        self.is_activated = False
        self.data = []
        if self.locked_label is not None:
            self.locked_label.delete()
            self.locked_label = None

        if self.title_label is not None:
            self.title_label.delete()
            self.title_label = None

        if self.description_label is not None:
            self.description_label.delete()
            self.description_label = None

        if self.placeholder_label is not None:
            self.placeholder_label.delete()
            self.placeholder_label = None

        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        self.size = (int(6.875 * int(72 / 1280 * self.screen_resolution[0])),
                     int(72 / 1280 * self.screen_resolution[0]))
        interval_between_cells = int(72 / 1280 * self.screen_resolution[0]) // 4
        general_height = 4 * self.size[1] + 3 * interval_between_cells
        fetched_coords = (self.screen_resolution[0] // 2 - self.size[0] - interval_between_cells // 2,
                          self.screen_resolution[1] // 2 + general_height // 2 - self.size[1] // 4 - self.size[1] // 2)
        self.position = (fetched_coords[0] + self.construction_type * (self.size[0] + interval_between_cells),
                         fetched_coords[1] - self.row * (self.size[1] + interval_between_cells))
        if self.locked_label is not None:
            self.locked_label.x = self.position[0] + self.size[0] - self.size[1] // 2
            self.locked_label.y = self.position[1] + self.size[1] // 2
            self.locked_label.font_size = int(self.build_button.base_font_size_property * self.size[1])

        if self.title_label is not None:
            self.title_label.x = self.position[0] + self.size[1] // 8
            self.title_label.y = self.position[1] + int(0.7 * self.size[1])
            self.title_label.font_size = int(0.3 * self.size[1])

        if self.description_label is not None:
            self.description_label.x = self.position[0] + self.size[1] // 8
            self.description_label.y = self.position[1] + int(22 * self.size[1] / 80)
            self.description_label.font_size = self.size[1] // 5

        if self.placeholder_label is not None:
            self.placeholder_label.x = self.position[0] + self.size[0] // 2
            self.placeholder_label.y = self.position[1] + self.size[1] // 2
            self.placeholder_label.font_size = int(11 * self.size[1] / 40)

        self.build_button.on_size_changed((self.size[1], self.size[1]))
        self.enable_money_target_button.on_size_changed((self.size[1], self.size[1]))
        self.disable_money_target_button.on_size_changed((self.size[1], self.size[1]))
        self.build_button.x_margin = self.position[0] + self.size[0] - self.size[1]
        self.build_button.y_margin = self.position[1]
        self.enable_money_target_button.x_margin = self.position[0] + self.size[0] - self.size[1] * 2 + 2
        self.enable_money_target_button.y_margin = self.position[1]
        self.disable_money_target_button.x_margin = self.position[0] + self.size[0] - self.size[1] * 2 + 2
        self.disable_money_target_button.y_margin = self.position[1]

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            if len(self.data) == 0 or self.entity_number == 0:
                self.placeholder_label.text = I18N_RESOURCES[self.placeholder_key][self.current_locale]
            else:
                self.title_label.text = I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number)
                self.on_update_description_label()

    def on_activate_money_target(self):
        """
        Activates money target for the cell and all appropriate buttons.
        """
        self.money_target_activated = True
        if self.is_activated and len(self.data) > 0:
            self.enable_money_target_button.on_deactivate()
            if self.data[UNLOCK_AVAILABLE]:
                self.disable_money_target_button.on_activate()
            else:
                self.disable_money_target_button.on_deactivate()

    def on_deactivate_money_target(self):
        """
        Deactivates money target for the cell and all appropriate buttons.
        """
        self.money_target_activated = False
        if self.is_activated and len(self.data) > 0:
            self.disable_money_target_button.on_deactivate()
            if self.data[UNLOCK_AVAILABLE]:
                self.enable_money_target_button.on_activate()
            else:
                self.enable_money_target_button.on_deactivate()


class ScheduleRow:
    """
    Implements base class for schedule row.
    """
    def __init__(self, column, row, surface, batches, groups, current_locale):
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
            main_sprite                         label for all params except departure location
            arrival_sprite                      label for departure location
            screen_resolution                   current game window resolution
            position                            position of the middle point of schedule row
            size                                schedule row width and height

        :param column:                          number of schedule column
        :param row:                             number of schedule row
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        :param current_locale:                  current locale selected by player
        """
        self.logger = getLogger(f'root.app.game.map.scheduler.view.row.{column}.{row}')
        self.column, self.row = column, row
        self.surface, self.batches, self.groups, self.current_locale = surface, batches, groups, current_locale
        self.data = None
        self.main_sprite = None
        self.arrival_sprite = None
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.size = (0, 0)
        self.is_activated = False

    def on_activate(self):
        """
        Activates the schedule row.
        """
        self.is_activated = True

    @row_is_active
    def on_deactivate(self):
        """
        Deactivates the schedule row, deletes all labels, deactivates all buttons.
        """
        self.is_activated = False
        self.data = []
        self.main_sprite.delete()
        self.main_sprite = None
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
                = Label('{0:0>6}    {1:0>2} : {2:0>2}                             {3:0>2}   {4:0>2} : {5:0>2}'
                        .format(self.data[TRAIN_ID],
                                (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                                (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
                                self.data[CARS], self.data[STOP_TIME] // FRAMES_IN_ONE_MINUTE,
                                (self.data[STOP_TIME] // FRAMES_IN_ONE_SECOND) % SECONDS_IN_ONE_MINUTE),
                        font_name='Perfo', bold=True, font_size=self.size[1] // 5 * 3,
                        x=self.position[0], y=self.position[1], anchor_x='center', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])
        else:
            self.main_sprite.text \
                = '{0:0>6}    {1:0>2} : {2:0>2}                             {3:0>2}   {4:0>2} : {5:0>2}'\
                .format(self.data[TRAIN_ID],
                        (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                        (self.data[ARRIVAL_TIME] // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
                        self.data[CARS], self.data[STOP_TIME] // FRAMES_IN_ONE_MINUTE,
                        (self.data[STOP_TIME] // FRAMES_IN_ONE_SECOND) % SECONDS_IN_ONE_MINUTE)

        if self.arrival_sprite is None:
            self.arrival_sprite \
                = Label(I18N_RESOURCES['departed_from_string'][self.current_locale][self.data[DIRECTION]],
                        font_name='Perfo', bold=True, font_size=self.size[1] // 5 * 3,
                        x=self.position[0] + self.size[0] // 16, y=self.position[1],
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
        general_height = 4 * int(72 / 1280 * self.screen_resolution[0]) \
                         + 3 * int(72 / 1280 * self.screen_resolution[0]) // 4
        self.size = (int(6.875 * int(72 / 1280 * self.screen_resolution[0])),
                     general_height // (SCHEDULE_ROWS + 1))
        schedule_interval_between_columns = int(72 / 1280 * self.screen_resolution[0]) // 4
        top_left_row_position = (self.screen_resolution[0] // 2
                                 - int(6.875 * int(72 / 1280 * self.screen_resolution[0])) // 2
                                 - schedule_interval_between_columns // 2,
                                 self.screen_resolution[1]
                                 - ((self.screen_resolution[1] - int(72 / 1280 * self.screen_resolution[0]) // 2
                                     - int(72 / 1280 * self.screen_resolution[0]) - general_height) // 2
                                    + self.size[1] // 2 * 3)
                                 - int(72 / 1280 * self.screen_resolution[0]) // 2)
        self.position = (top_left_row_position[0] + self.column * (self.size[0] + schedule_interval_between_columns),
                         top_left_row_position[1] - self.row * self.size[1])
        if self.main_sprite is not None:
            self.main_sprite.x = self.position[0]
            self.main_sprite.y = self.position[1]
            self.main_sprite.font_size = self.size[1] // 5 * 3

        if self.arrival_sprite is not None:
            self.arrival_sprite.x = self.position[0] + self.size[0] // 16
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


class Checkbox:
    """
    Implements base class fo all checkboxes in the app.
    """
    def __init__(self, column, row, on_update_state_action, surface, batches, groups, current_locale, logger):
        def on_check(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.on_update_state_action(True)

        def on_uncheck(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.on_update_state_action(False)

        self.logger = logger
        self.column, self.row = column, row
        self.surface, self.batches, self.groups, self.current_locale = surface, batches, groups, current_locale
        self.on_update_state_action = on_update_state_action
        self.checked_checkbox_button, self.unchecked_checkbox_button \
            = create_two_state_button(CheckedCheckboxButton(surface=self.surface,
                                                            batch=self.batches['ui_batch'], groups=self.groups,
                                                            on_click_action=on_uncheck),
                                      UncheckedCheckboxButton(surface=self.surface,
                                                              batch=self.batches['ui_batch'], groups=self.groups,
                                                              on_click_action=on_check))
        self.buttons = [self.checked_checkbox_button, self.unchecked_checkbox_button]
        self.screen_resolution = (1280, 720)
        self.anchor_left_center_point = (0, 0)
        self.height = 0
        self.description_key = None
        self.description_label = None
        self.is_activated = False

    def on_activate(self):
        """
        Activates the checkbox, creates description label.
        """
        self.is_activated = True
        self.description_label = Label(I18N_RESOURCES[self.description_key][self.current_locale],
                                       font_name='Arial', font_size=self.height // 5 * 2,
                                       x=self.anchor_left_center_point[0]
                                         + int(72 / 1280 * self.screen_resolution[0]) * 2,
                                       y=self.anchor_left_center_point[1], anchor_x='left', anchor_y='center',
                                       batch=self.batches['ui_batch'], group=self.groups['button_text'])

    def on_init_state(self, initial_state):
        """
        Activates button depending on initial state of the checkbox.

        :param initial_state:                   indicates if checkbox is checked at the moment of activation
        """
        if initial_state:
            self.checked_checkbox_button.on_activate()
        else:
            self.unchecked_checkbox_button.on_activate()

    def on_deactivate(self):
        """
        Deactivates the checkbox, deletes all labels, deactivates all buttons.
        """
        self.is_activated = False
        self.description_label.delete()
        self.description_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        medium_line = self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4
        self.height = int(72 / 1280 * self.screen_resolution[0]) // 2
        row_step = 5 * self.height // 8
        column_step = self.screen_resolution[0] // 4
        self.anchor_left_center_point = (self.screen_resolution[0] // 4 + self.column * column_step,
                                         medium_line - self.row * row_step)
        self.checked_checkbox_button.on_size_changed((self.height, self.height))
        self.unchecked_checkbox_button.on_size_changed((self.height, self.height))
        self.checked_checkbox_button.x_margin = self.anchor_left_center_point[0] \
                                                + int(72 / 1280 * self.screen_resolution[0])
        self.checked_checkbox_button.y_margin = self.anchor_left_center_point[1] \
                                                - int(72 / 1280 * self.screen_resolution[0]) // 4
        self.unchecked_checkbox_button.x_margin = self.anchor_left_center_point[0] \
                                                  + int(72 / 1280 * self.screen_resolution[0])
        self.unchecked_checkbox_button.y_margin = self.anchor_left_center_point[1] \
                                                  - int(72 / 1280 * self.screen_resolution[0]) // 4
        if self.description_label is not None:
            self.description_label.x = self.anchor_left_center_point[0] + int(72 / 1280 * self.screen_resolution[0]) * 2
            self.description_label.y = self.anchor_left_center_point[1]
            self.description_label.font_size = self.height // 5 * 2

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.description_label is not None:
            self.description_label.text = I18N_RESOURCES[self.description_key][self.current_locale]