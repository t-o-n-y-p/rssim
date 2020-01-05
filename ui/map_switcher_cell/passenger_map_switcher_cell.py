from logging import getLogger

from ui.map_switcher_cell import MapSwitcherCell
from database import PASSENGER_MAP
from ui.label.passenger_map_cell_title_label import PassengerMapCellTitleLabel
from ui.label.passenger_map_cell_icon_0_label import PassengerMapCellIcon0Label
from ui.label.passenger_map_cell_icon_1_label import PassengerMapCellIcon1Label


class PassengerMapSwitcherCell(MapSwitcherCell):
    def __init__(self, on_buy_map_action, on_set_money_target_action, on_reset_money_target_action, parent_viewport):
        super().__init__(map_id=PASSENGER_MAP, on_buy_map_action=on_buy_map_action,
                         on_set_money_target_action=on_set_money_target_action,
                         on_reset_money_target_action=on_reset_money_target_action, parent_viewport=parent_viewport,
                         logger=getLogger('root.passenger_map_switcher_cell'))
        self.title_label = PassengerMapCellTitleLabel(parent_viewport=self.viewport)
        self.icon_labels = [PassengerMapCellIcon0Label(parent_viewport=self.viewport),
                            PassengerMapCellIcon1Label(parent_viewport=self.viewport)]
