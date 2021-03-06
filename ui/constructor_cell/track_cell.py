from typing import final

from database import UNDER_CONSTRUCTION, CONSTRUCTION_TIME, SECONDS_IN_ONE_DAY, SECONDS_IN_ONE_MINUTE, \
    MINUTES_IN_ONE_HOUR, SECONDS_IN_ONE_HOUR, UNLOCK_AVAILABLE, UNLOCK_CONDITION_FROM_LEVEL, \
    UNLOCK_CONDITION_FROM_ENVIRONMENT, UNLOCK_CONDITION_FROM_PREVIOUS_TRACK, MAX_CONSTRUCTION_TIME
from ui.constructor_cell import ConstructorCell
from ui.label.track_cell_title_label import TrackCellTitleLabel
from ui.label.previous_track_required_label import PreviousTrackRequiredLabel
from ui.label.environment_required_label import EnvironmentRequiredLabel
from ui.label.track_unlock_available_label import TrackUnlockAvailableLabel


@final
class TrackCell(ConstructorCell):
    def __init__(
            self, column, row, on_buy_construction_action, on_set_money_target_action,
            on_reset_money_target_action, parent_viewport
    ):
        super().__init__(
            column, row, on_buy_construction_action, on_set_money_target_action,
            on_reset_money_target_action, parent_viewport
        )
        self.title_label = TrackCellTitleLabel(parent_viewport=self.viewport)
        self.previous_entity_required_label = PreviousTrackRequiredLabel(parent_viewport=self.viewport)
        self.environment_required_label = EnvironmentRequiredLabel(parent_viewport=self.viewport)
        self.unlock_available_label = TrackUnlockAvailableLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend(
            [
                self.title_label.on_window_resize, self.previous_entity_required_label.on_window_resize,
                self.environment_required_label.on_window_resize, self.unlock_available_label.on_window_resize
            ]
        )

    def on_update_description_label(self):
        if self.data[UNDER_CONSTRUCTION]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            self.environment_required_label.delete()
            self.unlock_available_label.delete()
            self.under_construction_description_label.on_update_args(
                (int(self.data[CONSTRUCTION_TIME] / self.data[MAX_CONSTRUCTION_TIME] * 100), )
            )
            self.under_construction_description_label.create()

        elif self.data[UNLOCK_AVAILABLE]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            self.environment_required_label.delete()
            self.unlock_available_label.create()
            self.under_construction_description_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
            self.level_required_label.create()
            self.previous_entity_required_label.delete()
            self.environment_required_label.delete()
            self.unlock_available_label.delete()
            self.under_construction_description_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_ENVIRONMENT]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
            self.environment_required_label.create()
            self.unlock_available_label.delete()
            self.under_construction_description_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
            self.level_required_label.delete()
            self.previous_entity_required_label.create()
            self.environment_required_label.delete()
            self.unlock_available_label.delete()
            self.under_construction_description_label.delete()
