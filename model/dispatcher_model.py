from logging import getLogger

from model import *


class DispatcherModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.dispatcher.model'))
        self.trains = []
        self.supported_cars = [0, 0]
        self.user_db_cursor.execute('''SELECT unlocked_tracks, supported_cars_min, supported_cars_max 
                                       FROM game_progress''')
        self.unlocked_tracks, self.supported_cars[0], self.supported_cars[1] = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT busy FROM tracks')
        self.track_busy_status = [None, ]
        busy_status_parsed = self.user_db_cursor.fetchall()
        for i in busy_status_parsed:
            self.track_busy_status.append(bool(i[0]))

        self.supported_cars_by_track = [(0, 20), ]
        self.config_db_cursor.execute('SELECT supported_cars_min, supported_cars_max FROM track_config')
        self.supported_cars_by_track.extend(self.config_db_cursor.fetchall())

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_activate_view(self):
        self.view.on_activate()

    def on_update_time(self, game_time):
        for i in self.trains:
            track_priority_list = None
            if i.model.state == 'approaching':
                track_priority_list = MAIN_PRIORITY_TRACKS[i.model.direction][i.model.new_direction]
            elif i.model.state == 'approaching_pass_through':
                track_priority_list = PASS_THROUGH_PRIORITY_TRACKS[i.model.direction]

            for track in track_priority_list:
                if track <= self.unlocked_tracks and not self.track_busy_status[track] \
                        and i.model.cars in range(self.supported_cars_by_track[track][0],
                                                  self.supported_cars_by_track[track][1] + 1):
                    self.track_busy_status[track] = True
                    i.model.state = 'pending_boarding'
                    self.controller.parent_controller.on_close_train_route(i.model.track, i.model.train_route)
                    i.model.track = track
                    i.model.train_route = ENTRY_TRAIN_ROUTE[i.model.direction]
                    self.controller.parent_controller.on_open_train_route(track, ENTRY_TRAIN_ROUTE[i.model.direction],
                                                                          i.train_id, i.model.cars)
                    self.trains.remove(i)
                    break

    def on_save_state(self):
        for i in range(1, len(self.track_busy_status)):
            self.user_db_cursor.execute('''UPDATE tracks SET busy = ? WHERE track_number = ?''',
                                        (int(self.track_busy_status[i]), i))

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number

    def on_add_train(self, train_controller):
        self.trains.append(train_controller)

    def on_leave_track(self, track):
        self.track_busy_status[track] = False
