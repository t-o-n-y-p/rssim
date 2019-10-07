from model.scheduler_model import SchedulerModel
from model import PASSENGER_MAP_ENTRY_UNLOCK_CONDITIONS


class PassengerMapSchedulerModel(SchedulerModel):
    def __init__(self):
        super().__init__(map_id=0)

    def on_unlock_entry(self):
        directions_to_unlock = [d for d, condition_value in enumerate(PASSENGER_MAP_ENTRY_UNLOCK_CONDITIONS)
                                if condition_value == self.unlocked_tracks]
        for d in directions_to_unlock:
            self.entry_locked_state[d] = False
