from typing import final

from model.scheduler_model import SchedulerModel
from model import FREIGHT_MAP_MAIN_PRIORITY_TRACKS
from database import FREIGHT_MAP, CONFIG_DB_CURSOR


@final
class FreightMapSchedulerModel(SchedulerModel):
    def __init__(self, controller, view):
        super().__init__(controller, view, map_id=FREIGHT_MAP)

    def on_update_min_supported_cars_by_direction(self):
        CONFIG_DB_CURSOR.execute('''SELECT supported_cars_min FROM track_config 
                                    WHERE track_number = ? AND map_id = ?''', (self.unlocked_tracks, self.map_id))
        min_supported_cars_for_track = CONFIG_DB_CURSOR.fetchone()[0]
        for direction in range(len(FREIGHT_MAP_MAIN_PRIORITY_TRACKS)):
            for new_direction in range(len(FREIGHT_MAP_MAIN_PRIORITY_TRACKS[direction])):
                if self.unlocked_tracks in FREIGHT_MAP_MAIN_PRIORITY_TRACKS[direction][new_direction] \
                        and min_supported_cars_for_track \
                        < self.min_supported_cars_by_direction[direction][new_direction]:
                    self.min_supported_cars_by_direction[direction][new_direction] = min_supported_cars_for_track
