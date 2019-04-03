from pyglet.text import Label

from i18n import I18N_RESOURCES
from ui.button import create_two_state_button
from ui.button.increment_button import IncrementButton
from ui.button.decrement_button import DecrementButton


class EnumValueControl:
    def __init__(self, column, row, surface, batches, groups, current_locale, possible_values_list,
                 on_update_state_action, logger):
        def on_increment(button):
            self.choice_state += 1
            self.on_update_temp_value_label()
            self.on_update_state_action(self.choice_state)
            if self.choice_state >= len(self.possible_values_list) - 1:
                button.on_deactivate()

            if self.choice_state > 0:
                button.paired_button.on_activate()

        def on_decrement(button):
            self.choice_state -= 1
            self.on_update_temp_value_label()
            self.on_update_state_action(self.choice_state)
            if self.choice_state <= 0:
                button.on_deactivate()

            if self.choice_state < len(self.possible_values_list) - 1:
                button.paired_button.on_activate()

        self.logger = logger
        self.column, self.row = column, row
        self.surface, self.batches, self.groups, self.current_locale = surface, batches, groups, current_locale
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
            = create_two_state_button(IncrementButton(surface=self.surface,
                                                      batch=self.batches['ui_batch'], groups=self.groups,
                                                      on_click_action=on_increment),
                                      DecrementButton(surface=self.surface,
                                                      batch=self.batches['ui_batch'], groups=self.groups,
                                                      on_click_action=on_decrement))
        self.buttons = [self.increment_button, self.decrement_button]
        self.is_activated = False

    def on_activate(self):
        self.is_activated = True
        self.description_label = Label(I18N_RESOURCES[self.description_key][self.current_locale],
                                       font_name='Arial', font_size=self.height // 5 * 2,
                                       x=self.anchor_center_point[0], y=self.anchor_center_point[1],
                                       anchor_x='left', anchor_y='center',
                                       batch=self.batches['ui_batch'], group=self.groups['button_text'])

    def on_deactivate(self):
        self.is_activated = False
        self.description_label.delete()
        self.description_label = None
        self.temp_value_label.delete()
        self.temp_value_label = None
        for b in self.buttons:
            b.on_deactivate()

    def on_update_temp_value_label(self):
        pass

    def on_init_state(self, choice_state):
        self.choice_state = choice_state
        self.on_update_temp_value_label()
        if self.choice_state > 0:
            self.decrement_button.on_activate()

        if self.choice_state < len(self.possible_values_list) - 1:
            self.increment_button.on_activate()

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
        self.anchor_center_point = (self.screen_resolution[0] // 4 + self.column * column_step,
                                    medium_line + self.row * row_step)
        if self.description_label is not None:
            self.description_label.x = self.anchor_center_point[0]
            self.description_label.y = self.anchor_center_point[1]
            self.description_label.font_size = self.height // 5 * 2

        if self.temp_value_label is not None:
            self.description_label.x = self.anchor_center_point[0]
            self.description_label.y = self.anchor_center_point[1] - row_step * 2
            self.description_label.font_size = self.height // 5 * 2

        self.increment_button.on_size_changed((self.height, self.height))
        self.decrement_button.on_size_changed((self.height, self.height))
        self.increment_button.x_margin = self.anchor_center_point[0] - 3 * self.screen_resolution[0] // 32 \
                                         - self.height // 2
        self.increment_button.y_margin = self.anchor_center_point[1] - row_step * 2 - self.height // 2
        self.decrement_button.x_margin = self.anchor_center_point[0] + 3 * self.screen_resolution[0] // 32 \
                                         - self.height // 2
        self.decrement_button.y_margin = self.anchor_center_point[1] - row_step * 2 - self.height // 2

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.on_update_temp_value_label()
        if self.description_label is not None:
            self.description_label.text = I18N_RESOURCES[self.description_key][self.current_locale]
