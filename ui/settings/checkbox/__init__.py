from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui import *
from ui.button import create_two_state_button
from ui.button.checked_checkbox_button import CheckedCheckboxButton
from ui.button.unchecked_checkbox_button import UncheckedCheckboxButton
from database import USER_DB_CURSOR


class Checkbox:
    """
    Implements base class for all checkboxes in the app.
    """
    def __init__(self, column, row, on_update_state_action, logger):
        """
        Button click handlers:
            on_check                            on_click handler for unchecked checkbox button
            on_uncheck                          on_click handler for checked checkbox button

        Properties:
            logger                              telemetry instance
            column                              number of settings column
            row                                 number of settings row
            on_update_state_action              method to call when checkbox state is being updated
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            current_locale                      current locale selected by player
            checked_checkbox_button             CheckedCheckboxButton object
            unchecked_checkbox_button           UncheckedCheckboxButton object
            buttons                             list of all buttons
            screen_resolution                   current game window resolution
            anchor_left_center_point            left center point of settings screen cell
            height                              settings cell height
            description_key                     resource key for checkbox description
            description_label                   text label for checkbox description
            is_activated                        indicates if checkbox is activated or not
            opacity                             current checkbox opacity

        :param column:                          number of settings column
        :param row:                             number of settings row
        :param on_update_state_action:          method to call when checkbox state is being updated
        :param logger:                          telemetry instance
        """
        def on_check(button):
            """
            Swaps the buttons.
            Calls on_update_state_action when player checks checkbox.

            :param button:                      button that was clicked
            """
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.on_update_state_action(True)

        def on_uncheck(button):
            """
            Swaps the buttons.
            Calls on_update_state_action when player unchecks checkbox.

            :param button:                      button that was clicked
            """
            button.paired_button.opacity = button.opacity
            button.on_deactivate(instant=True)
            button.paired_button.on_activate()
            self.on_update_state_action(False)

        self.logger = logger
        self.column, self.row = column, row
        self.surface, self.batches, self.groups = SURFACE, BATCHES, GROUPS
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_update_state_action = on_update_state_action
        self.checked_checkbox_button, self.unchecked_checkbox_button \
            = create_two_state_button(CheckedCheckboxButton(on_click_action=on_uncheck),
                                      UncheckedCheckboxButton(on_click_action=on_check))
        self.buttons = [self.checked_checkbox_button, self.unchecked_checkbox_button]
        self.screen_resolution = (1280, 720)
        self.anchor_left_center_point = (0, 0)
        self.height = 0
        self.description_key = None
        self.description_label = None
        self.is_activated = False
        self.opacity = 0

    def on_update_opacity(self, new_opacity):
        """
        Updates checkbox opacity with given value.

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
        else:
            self.description_label.color = (*WHITE_RGB, self.opacity)

    def on_activate(self):
        """
        Activates the checkbox, creates description label.
        """
        self.is_activated = True
        if self.description_label is None:
            self.description_label = Label(I18N_RESOURCES[self.description_key][self.current_locale],
                                           font_name='Arial', font_size=self.height // 5 * 2,
                                           color=(*WHITE_RGB, self.opacity),
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
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.screen_resolution = screen_resolution
        middle_line = self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4
        self.height = int(72 / 1280 * self.screen_resolution[0]) // 2
        row_step = 5 * self.height // 8
        column_step = self.screen_resolution[0] // 4
        self.anchor_left_center_point = (self.screen_resolution[0] // 4 + self.column * column_step,
                                         middle_line + self.row * row_step)
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
