from abc import ABC

from ui import *
from ui.button import create_two_state_button
from ui.button.increment_button import IncrementButton
from ui.button.decrement_button import DecrementButton
from database import USER_DB_CURSOR


class EnumValueControl(ABC):
    def __init__(self, column, row, possible_values_list, on_update_state_action, parent_viewport, logger):
        def on_increment(button):
            self.choice_state += 1
            self.temp_value_label.on_update_args(self.possible_values_list[self.choice_state])
            self.on_update_state_action(self.choice_state)
            if self.choice_state >= len(self.possible_values_list) - 1:
                button.on_deactivate(instant=True)

            if self.choice_state > 0:
                button.paired_button.on_activate(instant=True)

        def on_decrement(button):
            self.choice_state -= 1
            self.temp_value_label.on_update_args(self.possible_values_list[self.choice_state])
            self.on_update_state_action(self.choice_state)
            if self.choice_state <= 0:
                button.on_deactivate(instant=True)

            if self.choice_state < len(self.possible_values_list) - 1:
                button.paired_button.on_activate(instant=True)

        self.logger = logger
        self.column, self.row = column, row
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.on_update_state_action = on_update_state_action
        self.screen_resolution = (1280, 720)
        self.description_label = None
        self.temp_value_label = None
        self.choice_state = None
        self.possible_values_list = possible_values_list
        self.increment_button, self.decrement_button \
            = create_two_state_button(IncrementButton(on_click_action=on_increment, parent_viewport=self.viewport),
                                      DecrementButton(on_click_action=on_decrement, parent_viewport=self.viewport))
        self.buttons = [self.increment_button, self.decrement_button]
        self.is_activated = False
        self.opacity = 0

    @final
    def on_activate(self):
        self.is_activated = True
        self.description_label.create()

    @final
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    @final
    def on_init_state(self, initial_state):
        self.choice_state = initial_state
        self.temp_value_label.on_update_args(self.possible_values_list[self.choice_state])
        self.temp_value_label.create()
        if self.choice_state > 0:
            self.decrement_button.on_activate()
        else:
            self.decrement_button.on_deactivate(instant=True)
            self.decrement_button.state = 'normal'

        if self.choice_state < len(self.possible_values_list) - 1:
            self.increment_button.on_activate()
        else:
            self.increment_button.on_deactivate(instant=True)
            self.decrement_button.state = 'normal'

    @final
    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1 = self.parent_viewport.x1 \
                           + (self.column + 1) * (self.parent_viewport.x2 - self.parent_viewport.x1) // 4
        self.viewport.x2 = self.viewport.x1 + (self.parent_viewport.x2 - self.parent_viewport.x1) // 2
        mid_line = (self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                    + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)) // 2
        self.viewport.y1 = mid_line + (self.row - 2) * (5 * get_top_bar_height(self.screen_resolution) // 8) \
                           - get_top_bar_height(self.screen_resolution) // 2
        self.viewport.y2 = mid_line + self.row * (5 * get_top_bar_height(self.screen_resolution) // 8) \
                           + get_top_bar_height(self.screen_resolution) // 2
        self.description_label.on_change_screen_resolution(self.screen_resolution)
        self.temp_value_label.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.description_label.on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.description_label.on_update_opacity(self.opacity)
        self.temp_value_label.on_update_opacity(self.opacity)
