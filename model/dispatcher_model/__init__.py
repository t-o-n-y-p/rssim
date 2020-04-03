from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class DispatcherModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.model'))
        self.trains = []
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('SELECT busy FROM tracks WHERE map_id = ?', (self.map_id, ))
        self.track_busy_status = [TRUE, *[t[0] for t in USER_DB_CURSOR.fetchall()]]
        CONFIG_DB_CURSOR.execute(
            '''SELECT supported_cars_min, supported_cars_max FROM track_config WHERE map_id = ?''', (self.map_id, )
        )
        self.supported_cars_by_track = ((0, 20), *CONFIG_DB_CURSOR.fetchall())

    @final
    def on_save_state(self):
        for i in range(1, len(self.track_busy_status)):
            USER_DB_CURSOR.execute(
                'UPDATE tracks SET busy = ? WHERE track_number = ? AND map_id = ?',
                (self.track_busy_status[i], i, self.map_id)
            )

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        for t in self.trains:
            for track in self.get_track_priority_list(t):
                if track <= self.unlocked_tracks and not self.track_busy_status[track] \
                        and t.model.cars in range(self.supported_cars_by_track[track][0],
                                                  self.supported_cars_by_track[track][1] + 1):
                    self.track_busy_status[track] = TRUE
                    if t.model.state == 'approaching':
                        self.controller.parent_controller.on_announcement_add(
                            announcement_time=self.game_time, announcement_type=ARRIVAL_ANNOUNCEMENT,
                            train_id=t.train_id, track_number=track
                        )
                    else:
                        self.controller.parent_controller.on_announcement_add(
                            announcement_time=self.game_time, announcement_type=PASS_THROUGH_ANNOUNCEMENT,
                            train_id=None, track_number=track
                        )

                    t.model.state = 'pending_boarding'
                    self.controller.parent_controller.on_close_train_route(t.model.track, t.model.train_route)
                    t.model.track = track
                    t.model.train_route = ENTRY_TRAIN_ROUTE[self.map_id][t.model.direction]
                    self.controller.parent_controller.on_open_train_route(
                        track, ENTRY_TRAIN_ROUTE[self.map_id][t.model.direction], t.train_id, t.model.cars
                    )
                    self.trains.remove(t)
                    break

    @final
    def on_unlock_track(self, track):
        self.unlocked_tracks = track

    @final
    def on_add_train(self, train_controller):
        self.trains.append(train_controller)

    @final
    def on_leave_track(self, track):
        self.track_busy_status[track] = FALSE

    @abstractmethod
    def get_track_priority_list(self, train):
        pass
