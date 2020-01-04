from typing import final

from model.dispatcher_model import DispatcherModel
from model import FREIGHT_MAP_MAIN_PRIORITY_TRACKS
from database import FREIGHT_MAP


@final
class FreightMapDispatcherModel(DispatcherModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=FREIGHT_MAP)

    def get_track_priority_list(self, train):
        if train.model.state == 'approaching':
            return FREIGHT_MAP_MAIN_PRIORITY_TRACKS[train.model.direction][train.model.new_direction]
        else:
            return ()
