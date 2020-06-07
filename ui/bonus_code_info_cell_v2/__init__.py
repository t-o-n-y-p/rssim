from typing import final

from database import CONSTRUCTION_SPEED_BONUS_CODE, MONEY_BONUS_CODE, EXP_BONUS_CODE, \
    ACTIVATIONS_LEFT, BONUS_CODE_MATRIX, BONUS_VALUE, CODE_TYPE
from ui import window_size_has_changed, get_top_bar_height, get_bottom_bar_height, UIObject, localizable, is_active, \
    default_object, optional_object
from ui.label_v2.activations_title_label_v2 import ActivationsTitleLabelV2
from ui.label_v2.activations_value_label_v2 import ActivationsValueLabelV2
from ui.label_v2.bonus_info_cell_construction_speed_bonus_value_label_v2 import \
    BonusInfoCellConstructionSpeedBonusValueLabelV2
from ui.label_v2.bonus_info_cell_exp_bonus_value_label_v2 import BonusInfoCellExpBonusValueLabelV2
from ui.label_v2.bonus_info_cell_money_bonus_value_label_v2 import BonusInfoCellMoneyBonusValueLabelV2
from ui.label_v2.bonus_title_label_v2 import BonusTitleLabelV2


@final
class BonusCodeInfoCellV2(UIObject):
    @localizable
    @default_object(BonusTitleLabelV2)
    @default_object(ActivationsTitleLabelV2)
    @default_object(ActivationsValueLabelV2)
    @optional_object(BonusInfoCellExpBonusValueLabelV2)
    @optional_object(BonusInfoCellMoneyBonusValueLabelV2)
    @optional_object(BonusInfoCellConstructionSpeedBonusValueLabelV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.bonus_type = None
        self.bonus_value = None
        self.activations_left = None

    @is_active
    def on_deactivate(self):
        self.is_activated = False
        if self.bonus_type == EXP_BONUS_CODE:
            self.fade_in_animation.child_animations.remove(
                self.bonus_info_cell_exp_bonus_value_label_v2.fade_in_animation                                 # noqa
            )
        elif self.bonus_type == MONEY_BONUS_CODE:
            self.fade_in_animation.child_animations.remove(
                self.bonus_info_cell_money_bonus_value_label_v2.fade_in_animation                               # noqa
            )
        elif self.bonus_type == CONSTRUCTION_SPEED_BONUS_CODE:
            self.fade_in_animation.child_animations.remove(
                self.bonus_info_cell_construction_speed_bonus_value_label_v2.fade_in_animation                  # noqa
            )

    def on_assign_data(self, user_input_hash):
        self.bonus_type = BONUS_CODE_MATRIX[user_input_hash][CODE_TYPE]
        self.bonus_value = round((BONUS_CODE_MATRIX[user_input_hash][BONUS_VALUE] - 1) * 100)
        self.activations_left = BONUS_CODE_MATRIX[user_input_hash][ACTIVATIONS_LEFT]
        self.activations_value_label_v2.on_activations_left_update(self.activations_left)                       # noqa
        if self.bonus_type == EXP_BONUS_CODE:
            self.bonus_info_cell_exp_bonus_value_label_v2.on_bonus_value_update(self.bonus_value)               # noqa
            self.fade_in_animation.child_animations.append(
                self.bonus_info_cell_exp_bonus_value_label_v2.fade_in_animation                                 # noqa
            )
        elif self.bonus_type == MONEY_BONUS_CODE:
            self.bonus_info_cell_money_bonus_value_label_v2.on_bonus_value_update(self.bonus_value)             # noqa
            self.fade_in_animation.child_animations.append(
                self.bonus_info_cell_money_bonus_value_label_v2.fade_in_animation                               # noqa
            )
        elif self.bonus_type == CONSTRUCTION_SPEED_BONUS_CODE:
            self.bonus_info_cell_construction_speed_bonus_value_label_v2.on_bonus_value_update(self.bonus_value)# noqa
            self.fade_in_animation.child_animations.append(
                self.bonus_info_cell_construction_speed_bonus_value_label_v2.fade_in_animation                  # noqa
            )

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 = (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 \
            - 5 * get_top_bar_height(self.screen_resolution)
        self.viewport.x2 = (self.parent_viewport.x1 + self.parent_viewport.x2) // 2 \
            + 5 * get_top_bar_height(self.screen_resolution)
        self.viewport.y1 = (
                self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
            ) // 2 - 5 * get_bottom_bar_height(self.screen_resolution) // 8 \
            - get_bottom_bar_height(self.screen_resolution) // 2
        self.viewport.y2 = (
                self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
                + self.parent_viewport.y2 - get_top_bar_height(self.screen_resolution)
            ) // 2 - 5 * get_bottom_bar_height(self.screen_resolution) // 8 \
            + get_bottom_bar_height(self.screen_resolution) // 2
