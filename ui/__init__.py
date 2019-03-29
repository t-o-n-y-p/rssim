from pyglet.text import Label

from i18n import I18N_RESOURCES
from button import create_two_state_button
from button.build_construction_button import BuildConstructionButton
from button.set_money_target_button import SetMoneyTargetButton
from button.reset_money_target_button import ResetMoneyTargetButton


# --------------------- CONSTANTS ---------------------
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


class ConstructorCell:
    def __init__(self, construction_type, row, config_db_cursor, surface, batches, groups, current_locale,
                 on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action):
        def on_set_money_target(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.on_set_money_target_action(self.construction_type, self.row, self.entity_number)

        def on_reset_money_target(button):
            button.on_deactivate()
            button.paired_button.on_activate()
            self.on_reset_money_target_action()

        def on_buy_construction(button):
            button.on_deactivate()
            self.enable_money_target_button.on_deactivate()
            self.disable_money_target_button.on_deactivate()
            self.on_buy_construction_action(self.construction_type, self.row, self.entity_number)

        self.is_activated = False
        self.construction_type, self.row, self.config_db_cursor = construction_type, row, config_db_cursor
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
        self.entity_number = entity_number
        self.data = data
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
        pass

    @cell_is_active
    def on_update_state(self, data):
        self.data = data
        if self.data[UNLOCK_AVAILABLE]:
            self.on_update_build_button_state()
            if not self.money_target_activated and not self.enable_money_target_button.is_activated \
                    and not self.disable_money_target_button.is_activated:
                self.on_deactivate_money_target()

        if self.is_activated:
            self.on_update_description_label()

    def on_update_money(self, money):
        self.money = money
        self.on_update_build_button_state()

    @cell_is_active
    def on_update_build_button_state(self):
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
        self.is_activated = True

    @cell_is_active
    def on_deactivate(self):
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

    def on_change_screen_resolution(self, new_screen_resolution):
        self.screen_resolution = new_screen_resolution
        self.config_db_cursor.execute('''SELECT constructor_top_left_cell_x, constructor_top_left_cell_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        fetched_coords = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT constructor_cell_width, constructor_cell_height, 
                                         constructor_interval_between_cells
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.size[0], self.size[1], interval_between_cells = self.config_db_cursor.fetchone()
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

        self.build_button.on_size_changed((self.size[1], self.size[1]),
                                          int(self.build_button.base_font_size_property * self.size[1]))
        self.enable_money_target_button.on_size_changed((self.size[1], self.size[1]),
                                                        int(self.enable_money_target_button.base_font_size_property
                                                           * self.size[1]))
        self.disable_money_target_button.on_size_changed((self.size[1], self.size[1]),
                                                         int(self.disable_money_target_button.base_font_size_property
                                                            * self.size[1]))
        self.build_button.x_margin = self.position[0] + self.size[0] - self.size[1]
        self.build_button.y_margin = self.position[1]
        self.enable_money_target_button.x_margin = self.position[0] + self.size[0] - self.size[1] * 2 + 2
        self.enable_money_target_button.y_margin = self.position[1]
        self.disable_money_target_button.x_margin = self.position[0] + self.size[0] - self.size[1] * 2 + 2
        self.disable_money_target_button.y_margin = self.position[1]

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        if self.is_activated:
            if len(self.data) == 0 or self.entity_number == 0:
                self.placeholder_label.text = I18N_RESOURCES[self.placeholder_key][self.current_locale]
            else:
                self.title_label.text = I18N_RESOURCES[self.title_key][self.current_locale].format(self.entity_number)
                self.on_update_description_label()

    def on_activate_money_target(self):
        self.money_target_activated = True
        if len(self.data) > 0:
            self.enable_money_target_button.on_deactivate()
            if self.data[UNLOCK_AVAILABLE]:
                self.disable_money_target_button.on_activate()
            else:
                self.disable_money_target_button.on_deactivate()

    def on_deactivate_money_target(self):
        self.money_target_activated = False
        if len(self.data) > 0:
            self.disable_money_target_button.on_deactivate()
            if self.data[UNLOCK_AVAILABLE]:
                self.enable_money_target_button.on_activate()
            else:
                self.enable_money_target_button.on_deactivate()
