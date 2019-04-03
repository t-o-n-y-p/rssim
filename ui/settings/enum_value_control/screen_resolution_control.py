from logging import getLogger

from ui.settings.enum_value_control import *


class ScreenResolutionControl(EnumValueControl):
    def __init__(self, column, row, surface, batches, groups, current_locale,
                 possible_values_list, on_update_state_action):
        super().__init__(column, row, surface, batches, groups, current_locale,
                         possible_values_list, on_update_state_action,
                         logger=getLogger('root.app.settings.view.enum_value_control.screen_resolution_control'))
        self.description_key = 'windowed_resolution_description_string'

    def on_update_temp_value_label(self):
        text = '{}x{}'.format(self.possible_values_list[self.choice_state][0],
                              self.possible_values_list[self.choice_state][1])
        if self.temp_value_label is None:
            self.temp_value_label = Label(text, font_name='Arial', font_size=self.height // 5 * 2,
                                          x=self.anchor_center_point[0],
                                          y=self.anchor_center_point[1] - 10 * self.height // 8,
                                          anchor_x='center', anchor_y='center',
                                          batch=self.batches['ui_batch'], group=self.groups['button_text'])
        else:
            self.temp_value_label.text = text
