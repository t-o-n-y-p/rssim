from random import choice, seed
from logging import getLogger

from model import *
from textures import CAR_COLLECTIONS


class MapModel(Model):
    """
    Implements Map model.
    Map object is responsible for properties, UI and events related to the map.
    """
    def __init__(self, map_id):
        """
        Properties:
            map_id                              ID of the map
            unlocked_tracks                     number of tracks available for player and trains
            unlocked_environment                environment tier available for player
            unlocked_car_collections            list of car collections which can be used for new trains
            last_known_base_offset              base offset which is saved after each map drag gesture
            zoom_out_activated                  indicates if map is zoomed out or not

        :param map_id:                          ID of the map
        """
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.model'))
        self.map_id = map_id
        self.user_db_cursor.execute('''SELECT unlocked_tracks, unlocked_environment 
                                       FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks, self.unlocked_environment = self.user_db_cursor.fetchone()
        self.user_db_cursor.execute('''SELECT unlocked_car_collections FROM map_progress WHERE map_id = ?''',
                                    (self.map_id, ))
        self.unlocked_car_collections = list(map(int, self.user_db_cursor.fetchone()[0].split(',')))
        self.user_db_cursor.execute('SELECT last_known_base_offset FROM graphics WHERE map_id = ?', (self.map_id, ))
        self.last_known_base_offset = list(map(int, self.user_db_cursor.fetchone()[0].split(',')))
        self.user_db_cursor.execute('SELECT zoom_out_activated FROM graphics WHERE map_id = ?', (self.map_id, ))
        self.zoom_out_activated = bool(self.user_db_cursor.fetchone()[0])

    def on_activate_view(self):
        """
        Activates the view if this map matches the map which was opened last.
        """
        self.user_db_cursor.execute('SELECT map_id FROM graphics')
        if self.map_id == self.user_db_cursor.fetchone()[0]:
            self.view.on_activate()

    def on_unlock_track(self, track):
        """
        Updates number of unlocked tracks. Adds new car collection if required.
        Notifies the view about number of unlocked tracks update.

        :param track:                   track number
        """
        self.unlocked_tracks = track
        if self.unlocked_tracks in PASSENGER_CAR_COLLECTION_UNLOCK_TRACK_LIST:
            self.on_add_new_car_collection()

        self.view.on_unlock_track(track)

    def on_unlock_environment(self, tier):
        """
        Updates number of unlocked environment tiers.
        Notifies the view about number of unlocked environment tiers update.

        :param tier:                    environment tier number
        """
        self.unlocked_environment = tier
        self.view.on_unlock_environment(tier)

    def on_save_state(self):
        """
        Saves map state to user progress database.
        """
        self.user_db_cursor.execute('''UPDATE map_progress SET unlocked_tracks = ?, unlocked_environment = ?, 
                                       unlocked_car_collections = ? WHERE map_id = ?''',
                                    (self.unlocked_tracks, self.unlocked_environment,
                                     ','.join(list(map(str, self.unlocked_car_collections))), self.map_id))

    def on_save_and_commit_last_known_base_offset(self, base_offset):
        """
        Saves and commits last known base offset to the database.

        :param base_offset:             last known base offset
        """
        self.last_known_base_offset = base_offset
        self.user_db_cursor.execute('UPDATE graphics SET last_known_base_offset = ? WHERE map_id = ?',
                                    (','.join(list(map(str, self.last_known_base_offset))), self.map_id))
        self.user_db_connection.commit()

    def on_save_and_commit_zoom_out_activated(self, zoom_out_activated):
        """
        Saves and commits zoom_out_activated flag value to the database.

        :param zoom_out_activated:      indicates if map is zoomed out or not
        """
        self.zoom_out_activated = zoom_out_activated
        self.user_db_cursor.execute('UPDATE graphics SET zoom_out_activated = ? WHERE map_id = ?',
                                    (int(zoom_out_activated), self.map_id))
        self.user_db_connection.commit()

    def on_clear_trains_info(self):
        """
        Clears currently stores trains info from the database.
        """
        self.user_db_cursor.execute('DELETE FROM trains WHERE map_id = ?', (self.map_id, ))

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        """
        Creates new train similar to _create_train function.

        :param train_id:                        train identification number
        :param cars:                            number of cars in the train
        :param track:                           track number (0 for regular entry and 100 for side entry)
        :param train_route:                     train route type (left/right approaching or side_approaching)
        :param state:                           train state: approaching or approaching_pass_through
        :param direction:                       train arrival direction
        :param new_direction:                   train departure direction
        :param current_direction:               train current direction
        :param priority:                        train priority in the queue
        :param boarding_time:                   amount of boarding time left for this train
        :param exp:                             exp gained when boarding finishes
        :param money:                           money gained when boarding finishes
        :return:                                Train object controller
        """
        pass

    def on_add_new_car_collection(self):
        """
        Adds new car collection, randomly selected from available collections.
        """
        all_collections_set = set(range(CAR_COLLECTIONS))
        available_car_collections = list(all_collections_set.difference(set(self.unlocked_car_collections)))
        if len(available_car_collections) > 0:
            seed()
            selected_collection = choice(available_car_collections)
            self.unlocked_car_collections.append(selected_collection)

    def get_signals_to_unlock_with_track(self, track):
        """
        Returns list of signal identifiers for signals which should be unlocked with given track.

        :param track:                           track which is unlocked
        :return:                                list of (track_param, base_route) pairs
        """
        self.config_db_cursor.execute('''SELECT track, base_route FROM signal_config 
                                         WHERE track_unlocked_with = ? AND map_id = ?''',
                                      (track, self.map_id))
        return self.config_db_cursor.fetchall()

    def get_switches_to_unlock_with_track(self, track):
        """
        Returns list of switches identifiers for switches which should be unlocked with given track.

        :param track:                           track which is unlocked
        :return:                                list of (track_param_1, track_param_2, switch_type) groups of three
        """
        self.config_db_cursor.execute('''SELECT track_param_1, track_param_2, switch_type 
                                         FROM switches_config WHERE track_unlocked_with = ? AND map_id = ?''',
                                      (track, self.map_id))
        return self.config_db_cursor.fetchall()

    def get_crossovers_to_unlock_with_track(self, track):
        """
        Returns list of crossovers identifiers for crossovers which should be unlocked with given track.

        :param track:                           track which is unlocked
        :return:                                list of (track_param_1, track_param_2, crossover_type) groups of three
        """
        self.config_db_cursor.execute('''SELECT track_param_1, track_param_2, crossover_type 
                                         FROM crossovers_config WHERE track_unlocked_with = ? AND map_id = ?''',
                                      (track, self.map_id))
        return self.config_db_cursor.fetchall()

    def get_shops_to_unlock_with_track(self, track):
        self.config_db_cursor.execute('''SELECT shop_id FROM shops_config WHERE map_id = ? AND track_required = ?''',
                                      (self.map_id, track))
        return self.config_db_cursor.fetchall()
