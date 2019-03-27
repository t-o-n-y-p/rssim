from ui import *
from i18n import I18N_RESOURCES


class TrackCell(ConstructorCell):
    def __init__(self, column, row, config_db_cursor, surface, batches, groups, current_locale,
                 on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action):
        super().__init__(column, row, config_db_cursor, surface, batches, groups, current_locale,
                         on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action)
        self.title_key = 'title_track_string'
        self.placeholder_key = 'no_more_tracks_available_placeholder_string'
        self.description_keys = {'UNDER_CONSTRUCTION': 'under_construction_track_description_string',
                                 'UNLOCK_AVAILABLE': 'unlock_available_track_description_string',
                                 'UNLOCK_CONDITION_FROM_LEVEL': 'unlock_condition_from_level_track_description_string',
                                 'UNLOCK_CONDITION_FROM_PREVIOUS_TRACK':
                                     'unlock_condition_from_previous_track_track_description_string',
                                 'UNLOCK_CONDITION_FROM_ENVIRONMENT':
                                     'unlock_condition_from_environment_track_description_string'}

    def on_update_description_label(self):
        if self.data[UNDER_CONSTRUCTION]:
            construction_time = self.data[CONSTRUCTION_TIME]
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNDER_CONSTRUCTION']][self.current_locale]\
                .format(construction_time // FRAMES_IN_ONE_HOUR,
                        (construction_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
        elif self.data[UNLOCK_AVAILABLE]:
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNLOCK_AVAILABLE']][self.current_locale]\
                .format(self.data[PRICE]).replace(',', ' ')
        elif not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNLOCK_CONDITION_FROM_LEVEL']][self.current_locale]\
                .format(self.data[LEVEL_REQUIRED])
        elif not self.data[UNLOCK_CONDITION_FROM_ENVIRONMENT]:
            self.description_label.text \
                = I18N_RESOURCES[self.description_keys['UNLOCK_CONDITION_FROM_ENVIRONMENT']][self.current_locale]\
                .format(self.data[ENVIRONMENT_REQUIRED])
        elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
            self.description_label.text \
                = I18N_RESOURCES[
                    self.description_keys['UNLOCK_CONDITION_FROM_PREVIOUS_TRACK']][self.current_locale]\
                .format(self.entity_number - 1)
