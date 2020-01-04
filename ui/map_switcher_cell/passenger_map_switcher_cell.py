from logging import getLogger

from ui.map_switcher_cell import MapSwitcherCell
from database import PASSENGER_MAP


class PassengerMapSwitcherCell(MapSwitcherCell):
    def __init__(self, on_buy_map_action, on_set_money_target_action, on_reset_money_target_action, parent_viewport):
        super().__init__(map_id=PASSENGER_MAP, on_buy_map_action=on_buy_map_action,
                         on_set_money_target_action=on_set_money_target_action,
                         on_reset_money_target_action=on_reset_money_target_action, parent_viewport=parent_viewport,
                         logger=getLogger('root.passenger_map_switcher_cell'))
