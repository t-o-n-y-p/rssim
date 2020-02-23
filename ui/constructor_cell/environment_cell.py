from ui import *
from ui.constructor_cell import ConstructorCell
from ui.label.environment_cell_title_label import EnvironmentCellTitleLabel
from ui.label.previous_environment_required_label import PreviousEnvironmentRequiredLabel
from ui.label.environment_unlock_available_label import EnvironmentUnlockAvailableLabel


@final
class EnvironmentCell(ConstructorCell):
    def __init__(self, column, row, on_buy_construction_action, on_set_money_target_action,
                 on_reset_money_target_action, parent_viewport):
        super().__init__(column, row, on_buy_construction_action, on_set_money_target_action,
                         on_reset_money_target_action, parent_viewport)
        self.title_label = EnvironmentCellTitleLabel(parent_viewport=self.viewport)
        self.previous_entity_required_label = PreviousEnvironmentRequiredLabel(parent_viewport=self.viewport)
        self.unlock_available_label = EnvironmentUnlockAvailableLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.extend([
            self.title_label.on_window_resize, self.previous_entity_required_label.on_window_resize,
            self.unlock_available_label.on_window_resize
        ])

    def on_update_description_label(self):
        if self.data[UNDER_CONSTRUCTION]:
            self.level_required_label.delete()
            self.previous_entity_required_label.delete()
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
            self.unlock_available_label.create()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_LEVEL]:
            self.level_required_label.create()
            self.previous_entity_required_label.delete()
            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
        elif not self.data[UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT]:
            self.level_required_label.delete()
            self.previous_entity_required_label.create()
            self.unlock_available_label.delete()
            self.under_construction_days_label.delete()
            self.under_construction_hours_minutes_label.delete()
