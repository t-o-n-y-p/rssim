from random import choice, seed
from logging import getLogger

from model import *
from controller.train_controller import TrainController
from model.train_model import TrainModel
from view.train_view import TrainView
from textures import CAR_COLLECTIONS, CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE


def _create_train(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, map_controller,
                  train_id, cars, track, train_route, state, direction, new_direction,
                  current_direction, priority, boarding_time, exp, money, unlocked_car_collections):
    """
    Creates controller, model and view for Train object from the dispatcher.
    It is responsible for properties, UI and events related to the train.

    :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
    :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
    :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
    :param surface:                         surface to draw all UI objects on
    :param batches:                         batches to group all labels and sprites
    :param groups:                          defines drawing layers (some labels and sprites behind others)
    :param map_controller:                  Map controller pointer
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
    :param unlocked_car_collections:        list of car collections which can be used for this train
    :return:                                Train object controller
    """
    controller = TrainController(map_controller, train_id)
    model = TrainModel(user_db_connection, user_db_cursor, config_db_cursor, train_id)
    # car collection is chosen randomly from available options, seed() initializes PRNG
    seed()
    model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                        priority, boarding_time, exp, money, choice(unlocked_car_collections))
    view = TrainView(user_db_cursor, config_db_cursor, surface, batches, groups, train_id,
                     CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


class MapModel(Model):
    """
    Implements Map model.
    Map object is responsible for properties, UI and events related to the map.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        """
        Properties:
            unlocked_tracks                     number of tracks available for player and trains
            unlocked_car_collections            list of car collections which can be used for new trains

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger('root.app.game.map.model'))
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('SELECT unlocked_car_collections FROM game_progress')
        self.unlocked_car_collections = list(map(int, self.user_db_cursor.fetchone()[0].split(',')))

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        """
        Activates the view.
        """
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_unlock_track(self, track):
        """
        Updates number of unlocked tracks. Adds new car collection if required.
        Notifies the view about number of unlocked tracks update.

        :param track:                   track number
        """
        self.unlocked_tracks = track
        if self.unlocked_tracks in CAR_COLLECTION_UNLOCK_TRACK_LIST:
            self.on_add_new_car_collection()

        self.view.on_unlock_track(track)

    def on_save_state(self):
        """
        Saves map state to user progress database.
        """
        self.user_db_cursor.execute('UPDATE game_progress SET unlocked_tracks = ?, unlocked_car_collections = ?',
                                    (self.unlocked_tracks, ','.join(list(map(str, self.unlocked_car_collections)))))

    def on_clear_trains_info(self):
        """
        Clears currently stores trains info from the database.
        """
        self.user_db_cursor.execute('DELETE FROM trains')

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        """
        Creates new train via _create_train function.

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
        return _create_train(self.user_db_connection, self.user_db_cursor, self.config_db_cursor, self.view.surface,
                             self.view.batches, self.view.groups, self.controller, train_id, cars, track, train_route,
                             state, direction, new_direction, current_direction, priority, boarding_time, exp, money,
                             self.unlocked_car_collections)

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
