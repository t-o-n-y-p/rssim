from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui import *
from ui.button import create_two_state_button
from ui.button.increment_button import IncrementButton
from ui.button.decrement_button import DecrementButton


class EnumValueControl:
    """
    Implements base class for all enum value controls on settings screen
    """
    def __init__(self, column, row, current_locale, possible_values_list,
                 on_update_state_action, logger):
        """
        Button click handlers:
            on_increment                        on_click handler for increment button
            on_decrement                        on_click handler for decrement button

        Properties:
            logger                              telemetry instance
            column                              number of settings column
            row                                 number of settings row
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            current_locale                      current locale selected by player
            on_update_state_action              method to call when control state is being updated
            possible_values_list                list of values for enum property
            choice_state                        index of currently selected value
            screen_resolution                   current game window resolution
            anchor_center_point                 center point of settings screen cell
            height                              settings cell height
            description_key                     resource key for checkbox description
            description_label                   text label for checkbox description
            temp_value_label                    text label for currently selected value
            is_activated                        indicates if checkbox is activated or not
            increment_button                    IncrementButton object
            decrement_button                    DecrementButton object
            buttons                             list of all buttons
            opacity                             current control opacity

        :param column:                          number of settings column
        :param row:                             number of settings row
        :param current_locale:                  current locale selected by player
        :param possible_values_list:            list of values for enum property
        :param on_update_state_action:          method to call when checkbox state is being updated
        :param logger:                          telemetry instance
        """
        def on_increment(button):
            """
            Calls on_update_state_action when value index is being incremented.
            Updates temp value label. Checks buttons state based on index.

            :param button:                      button that was clicked
            """
            self.choice_state += 1
            self.on_update_temp_value_label()
            self.on_update_state_action(self.choice_state)
            if self.choice_state >= len(self.possible_values_list) - 1:
                button.on_deactivate(instant=True)

            if self.choice_state > 0:
                button.paired_button.on_activate(instant=True)

        def on_decrement(button):
            """
            Calls on_update_state_action when value index is being decremented.
            Updates temp value label. Checks buttons state based on index.

            :param button:                      button that was clicked
            """
            self.choice_state -= 1
            self.on_update_temp_value_label()
            self.on_update_state_action(self.choice_state)
            if self.choice_state <= 0:
                button.on_deactivate(instant=True)

            if self.choice_state < len(self.possible_values_list) - 1:
                button.paired_button.on_activate(instant=True)

        self.logger = logger
        self.column, self.row = column, row
        self.surface, self.batches, self.groups, self.current_locale = SURFACE, BATCHES, GROUPS, current_locale
        self.on_update_state_action = on_update_state_action
        self.screen_resolution = (1280, 720)
        self.anchor_center_point = (0, 0)
        self.height = 0
        self.description_key = None
        self.description_label = None
        self.temp_value_label = None
        self.choice_state = None
        self.possible_values_list = possible_values_list
        self.increment_button, self.decrement_button \
            = create_two_state_button(IncrementButton(on_click_action=on_increment),
                                      DecrementButton(on_click_action=on_decrement))
        self.buttons = [self.increment_button, self.decrement_button]
        self.is_activated = False
        self.opacity = 0

    def on_activate(self):
        """
        Activates the control, creates description label.
        """
        self.is_activated = True
        if self.description_label is None:
            self.description_label = Label(I18N_RESOURCES[self.description_key][self.current_locale],
                                           font_name='Arial', font_size=self.height // 5 * 2,
                                           color=(*WHITE_RGB, self.opacity),
                                           x=self.anchor_center_point[0], y=self.anchor_center_point[1],
                                           anchor_x='center', anchor_y='center',
                                           batch=self.batches['ui_batch'], group=self.groups['button_text'])

    def on_deactivate(self):
        """
        Deactivates the control, deletes all labels, deactivates all buttons.
        """
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_update_temp_value_label(self):
        """
        Updates temp value label based on individual rule set for each control.
        """
        pass

    def on_init_state(self, initial_state):
        """
        Activates button depending on initial state of the control.

        :param initial_state:                   index of initial value
        """
        self.choice_state = initial_state
        self.on_update_temp_value_label()
        if self.choice_state > 0:
            self.decrement_button.on_activate()
        else:
            self.decrement_button.on_deactivate(instant=True)

        if self.choice_state < len(self.possible_values_list) - 1:
            self.increment_button.on_activate()
        else:
            self.increment_button.on_deactivate(instant=True)

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
        self.anchor_center_point = (self.screen_resolution[0] // 2 + self.column * column_step,
                                    medium_line + self.row * row_step)
        if self.description_label is not None:
            self.description_label.x = self.anchor_center_point[0]
            self.description_label.y = self.anchor_center_point[1]
            self.description_label.font_size = self.height // 5 * 2

        if self.temp_value_label is not None:
            self.temp_value_label.x = self.anchor_center_point[0]
            self.temp_value_label.y = self.anchor_center_point[1] - row_step * 2
            self.temp_value_label.font_size = self.height // 5 * 2

        self.increment_button.on_size_changed((self.height, self.height))
        self.decrement_button.on_size_changed((self.height, self.height))
        self.increment_button.x_margin = self.anchor_center_point[0] + 3 * self.screen_resolution[0] // 32 \
                                         - self.height // 2
        self.increment_button.y_margin = self.anchor_center_point[1] - row_step * 2 - self.height // 2
        self.decrement_button.x_margin = self.anchor_center_point[0] - 3 * self.screen_resolution[0] // 32 \
                                         - self.height // 2
        self.decrement_button.y_margin = self.anchor_center_point[1] - row_step * 2 - self.height // 2

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.description_label is not None:
            self.description_label.text = I18N_RESOURCES[self.description_key][self.current_locale]

        if self.temp_value_label is not None:
            self.on_update_temp_value_label()

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
            self.description_label.delete()
            self.description_label = None
            self.temp_value_label.delete()
            self.temp_value_label = None
        else:
            self.description_label.color = (*WHITE_RGB, self.opacity)
            self.temp_value_label.color = (*WHITE_RGB, self.opacity)
