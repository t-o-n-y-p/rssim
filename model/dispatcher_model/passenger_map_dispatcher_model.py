from model.dispatcher_model import DispatcherModel
from model import PASSENGER_MAP_MAIN_PRIORITY_TRACKS, PASSENGER_MAP_PASS_THROUGH_PRIORITY_TRACKS


class PassengerMapDispatcherModel(DispatcherModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=0)

    def get_track_priority_list(self, train):
        if train.model.state == 'approaching':
            return PASSENGER_MAP_MAIN_PRIORITY_TRACKS[train.model.direction][train.model.new_direction]
        elif train.model.state == 'approaching_pass_through':
            return PASSENGER_MAP_PASS_THROUGH_PRIORITY_TRACKS[train.model.direction]
        else:
            return ()
