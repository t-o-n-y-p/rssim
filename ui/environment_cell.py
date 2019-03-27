from ui import *
from i18n import I18N_RESOURCES, i18n_number_category


class EnvironmentCell(ConstructorCell):
    def __init__(self, column, row, config_db_cursor, surface, batches, groups, current_locale,
                 on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action):
        super().__init__(column, row, config_db_cursor, surface, batches, groups, current_locale,
                         on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action)
        self.title_key = 'title_environment_string'
        self.placeholder_key = 'no_more_tiers_available_placeholder_string'
        self.description_keys = {'UNDER_CONSTRUCTION': 'under_construction_environment_description_string',
                                 'UNLOCK_AVAILABLE': 'unlock_available_environment_description_string',
                                 'UNLOCK_CONDITION_FROM_LEVEL':
                                     'unlock_condition_from_level_environment_description_string',
                                 'UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT':
                                     'unlock_condition_from_previous_environment_environment_description_string'}

    def on_update_description_label(self):
        if self.data[UNDER_CONSTRUCTION]:
            days_left = self.data[CONSTRUCTION_TIME] // FRAMES_IN_ONE_DAY
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNDER_CONSTRUCTION']][self.current_locale][
                    i18n_number_category(days_left, self.current_locale)
                ].format(days_left)
        elif self.data[UNLOCK_AVAILABLE]:
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNLOCK_AVAILABLE']][self.current_locale]\
                .format(self.data[PRICE]).replace(',', ' ')
        elif not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNLOCK_CONDITION_FROM_LEVEL']][self.current_locale]\
                .format(self.data[LEVEL_REQUIRED])
        elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT]:
            self.description_label.text \
                = I18N_RESOURCES[
                    self.description_keys['UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT']][self.current_locale]\
                .format(self.entity_number - 1)
