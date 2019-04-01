from ui import *
from i18n import I18N_RESOURCES, i18n_number_category


class TrackCell(ConstructorCell):
    """
    Implements Track cell class for constructor screen.
    For properties definition see base ConstructorCell class.
    """
    def __init__(self, column, row, config_db_cursor, surface, batches, groups, current_locale,
                 on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action):
        super().__init__(column, row, config_db_cursor, surface, batches, groups, current_locale,
                         on_buy_construction_action, on_set_money_target_action, on_reset_money_target_action)
        self.title_key = 'title_track_string'
        self.placeholder_key = 'no_more_tracks_available_placeholder_string'
        self.description_keys = {'UNDER_CONSTRUCTION':
                                     {'hours': 'under_construction_hours_minutes_description_string',
                                      'days': 'under_construction_days_description_string'},
                                 'UNLOCK_AVAILABLE': 'unlock_available_track_description_string',
                                 'UNLOCK_CONDITION_FROM_LEVEL': 'unlock_condition_from_level_track_description_string',
                                 'UNLOCK_CONDITION_FROM_PREVIOUS_TRACK':
                                     'unlock_condition_from_previous_track_track_description_string',
                                 'UNLOCK_CONDITION_FROM_ENVIRONMENT':
                                     'unlock_condition_from_environment_track_description_string'}

    def on_update_description_label(self):
        """
        Updates track cell description based on data.
        """
        if self.data[UNDER_CONSTRUCTION]:
            if self.data[CONSTRUCTION_TIME] >= FRAMES_IN_ONE_DAY:
                days_left = self.data[CONSTRUCTION_TIME] // FRAMES_IN_ONE_DAY
                text = I18N_RESOURCES[self.description_keys['UNDER_CONSTRUCTION']['days']][self.current_locale][
                    i18n_number_category(days_left, self.current_locale)
                ].format(days_left)
            else:
                text = I18N_RESOURCES[self.description_keys['UNDER_CONSTRUCTION']['hours']][self.current_locale]\
                    .format(self.data[CONSTRUCTION_TIME] // FRAMES_IN_ONE_HOUR,
                            (self.data[CONSTRUCTION_TIME] // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)

            if self.description_label.text != text:
                self.description_label.text = text
                self.description_label.color = ORANGE

        elif self.data[UNLOCK_AVAILABLE]:
            text = I18N_RESOURCES[self.description_keys['UNLOCK_AVAILABLE']][self.current_locale] \
                .format(self.data[PRICE]).replace(',', ' ')
            if self.description_label.text != text:
                self.description_label.text = text
                self.description_label.color = GREEN

        elif not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
            text = I18N_RESOURCES[self.description_keys['UNLOCK_CONDITION_FROM_LEVEL']][self.current_locale] \
                .format(self.data[LEVEL_REQUIRED])
            if self.description_label.text != text:
                self.description_label.text = text
                self.description_label.color = GREY

        elif not self.data[UNLOCK_CONDITION_FROM_ENVIRONMENT]:
            text = I18N_RESOURCES[self.description_keys['UNLOCK_CONDITION_FROM_ENVIRONMENT']][self.current_locale] \
                .format(self.data[ENVIRONMENT_REQUIRED])
            if self.description_label.text != text:
                self.description_label.text = text
                self.description_label.color = GREY

        elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
            text = I18N_RESOURCES[self.description_keys['UNLOCK_CONDITION_FROM_PREVIOUS_TRACK']][self.current_locale] \
                .format(self.entity_number - 1)
            if self.description_label.text != text:
                self.description_label.text = text
                self.description_label.color = GREY
