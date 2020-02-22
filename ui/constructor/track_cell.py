from ui import *
from ui.constructor import ConstructorCell
from ui.label.track_cell_title_label import TrackCellTitleLabel
from ui.label.previous_track_required_label import PreviousTrackRequiredLabel
from ui.label.environment_required_label import EnvironmentRequiredLabel
from ui.label.track_unlock_available_label import TrackUnlockAvailableLabel


@final
class TrackCell(ConstructorCell):
    def __init__(self, column, row, on_buy_construction_action, on_set_money_target_action,
                 on_reset_money_target_action, parent_viewport):
        super().__init__(column, row, on_buy_construction_action, on_set_money_target_action,
                         on_reset_money_target_action, parent_viewport)
        self.title_label = TrackCellTitleLabel(parent_viewport=self.viewport)
        self.previous_entity_required_label = PreviousTrackRequiredLabel(parent_viewport=self.viewport)
        self.environment_required_label = EnvironmentRequiredLabel(parent_viewport=self.viewport)
        self.unlock_available_label = TrackUnlockAvailableLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend([
            self.title_label.on_window_resize, self.previous_entity_required_label.on_window_resize,
            self.environment_required_label.on_window_resize, self.unlock_available_label.on_window_resize
        ])

    def on_update_description_label(self):
        if self.data[UNDER_CONSTRUCTION]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            self.environment_required_label.delete()
            self.unlock_available_label.delete()
            if self.data[CONSTRUCTION_TIME] >= SECONDS_IN_ONE_DAY:
                self.under_construction_days_label.on_update_args(
                    (self.data[CONSTRUCTION_TIME] // SECONDS_IN_ONE_DAY, )
                )
                self.under_construction_days_label.create()
                self.under_construction_hours_minutes_label.delete()
            else:
                self.under_construction_hours_minutes_label\
                    .on_update_args((self.data[CONSTRUCTION_TIME] // SECONDS_IN_ONE_HOUR,
                                     (self.data[CONSTRUCTION_TIME] // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR))
                self.under_construction_hours_minutes_label.create()
                self.under_construction_days_label.delete()

        elif self.data[UNLOCK_AVAILABLE]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            self.environment_required_label.delete()
            self.unlock_available_label.create()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
            self.level_required_label.create()
            self.previous_entity_required_label.delete()
            self.environment_required_label.delete()
            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_ENVIRONMENT]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            self.environment_required_label.create()
            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
            self.level_required_label.delete()
            self.previous_entity_required_label.create()
            self.environment_required_label.delete()
            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
