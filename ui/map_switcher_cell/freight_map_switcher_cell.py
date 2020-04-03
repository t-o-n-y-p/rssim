from logging import getLogger

from ui.map_switcher_cell import MapSwitcherCell
from database import FREIGHT_MAP
from ui.label.freight_map_cell_title_label import FreightMapCellTitleLabel
from ui.label.freight_map_cell_icon_0_label import FreightMapCellIcon0Label
from ui.label.freight_map_cell_icon_1_label import FreightMapCellIcon1Label


class FreightMapSwitcherCell(MapSwitcherCell):
    def __init__(
            self, on_buy_map_action, on_switch_map_action, on_set_money_target_action, on_reset_money_target_action,
            parent_viewport
    ):
        super().__init__(
            map_id=FREIGHT_MAP, on_buy_map_action=on_buy_map_action, on_switch_map_action=on_switch_map_action,
            on_set_money_target_action=on_set_money_target_action,
            on_reset_money_target_action=on_reset_money_target_action, parent_viewport=parent_viewport,
            logger=getLogger('root.passenger_map_switcher_cell')
        )
        self.title_label = FreightMapCellTitleLabel(parent_viewport=self.viewport)
        self.icon_labels = [
            FreightMapCellIcon0Label(parent_viewport=self.viewport),
            FreightMapCellIcon1Label(parent_viewport=self.viewport)
        ]
        self.on_window_resize_handlers.append(self.title_label.on_window_resize)
        for label in self.icon_labels:
            self.on_window_resize_handlers.append(label.on_window_resize)
