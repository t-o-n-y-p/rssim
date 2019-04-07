from logging import getLogger

from model import *


class DispatcherModel(Model):
    """
    Implements Dispatcher model.
    Dispatcher object is responsible for assigning routes to approaching trains.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            trains                              list of trains still to be dispatched
            supported_cars                      trains with this number of cars can stop, others must pass through
            unlocked_tracks                     indicates how much tracks are available at the moment
            track_busy_status                   indicates which tracks are busy and which are not
            supported_cars_by_track             indicates number of cars each track can handle

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.dispatcher.model'))
        self.trains = []
        self.supported_cars = [0, 0]
        self.user_db_cursor.execute('''SELECT unlocked_tracks, supported_cars_min, supported_cars_max 
                                       FROM map_progress''')
        self.unlocked_tracks, self.supported_cars[0], self.supported_cars[1] = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('SELECT busy FROM tracks')
        self.track_busy_status = [True, ]
        busy_status_parsed = self.user_db_cursor.fetchall()
        for i in busy_status_parsed:
            self.track_busy_status.append(bool(i[0]))

        self.supported_cars_by_track = [(0, 20), ]
        self.config_db_cursor.execute('SELECT supported_cars_min, supported_cars_max FROM track_config')
        self.supported_cars_by_track.extend(self.config_db_cursor.fetchall())

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model. Does not activate the view
        because dispatcher does not have any visual representation actually.
        """
        self.is_activated = True

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_update_time(self, game_time):
        """
        Tries to dispatch all trains in queue.

        :param game_time:               current in-game time
        """
        for i in self.trains:
            # get track priority list based on train state, direction and new direction
            track_priority_list = []
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
        """
        Saves dispatcher state to user progress database.
        """
        for i in range(1, len(self.track_busy_status)):
            self.user_db_cursor.execute('''UPDATE tracks SET busy = ? WHERE track_number = ?''',
                                        (int(self.track_busy_status[i]), i))

    def on_unlock_track(self, track):
        """
        Updates number of unlocked tracks after new track was unlocked.

        :param track:                   track number
        """
        self.unlocked_tracks = track

    def on_add_train(self, train_controller):
        """
        Adds approaching train to the queue.
        After train is created, it needs to be dispatched to the most suitable track.

        :param train_controller:        controller of the train to be added
        """
        self.trains.append(train_controller)

    def on_leave_track(self, track):
        """
        Clears the track for any of the next trains.

        :param track:                   track number
        """
        self.track_busy_status[track] = False
