from random import choice, seed

from model import *
from controller.train_controller import TrainController
from model.train_model import TrainModel
from view.train_view import TrainView
from car_skins import CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE


def create_train(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, map_controller,
                 train_id, cars, track, train_route, state, direction, new_direction,
                 current_direction, priority, boarding_time, exp, money, unlocked_car_collections):
    controller = TrainController(map_controller)
    controller.train_id = train_id
    model = TrainModel(user_db_connection, user_db_cursor, config_db_cursor)
    seed()
    model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                        priority, boarding_time, exp, money, choice(unlocked_car_collections))
    view = TrainView(user_db_cursor, config_db_cursor, surface, batches, groups)
    view.car_head_image = CAR_HEAD_IMAGE
    view.car_mid_image = CAR_MID_IMAGE
    view.car_tail_image = CAR_TAIL_IMAGE
    view.boarding_light_image = BOARDING_LIGHT_IMAGE
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


class MapModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]
        self.user_db_cursor.execute('SELECT unlocked_car_collections FROM game_progress')
        car_collections_string = self.user_db_cursor.fetchone()[0]
        self.unlocked_car_collections = car_collections_string.split(',')
        for i in range(len(self.unlocked_car_collections)):
            self.unlocked_car_collections[i] = int(self.unlocked_car_collections[i])

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()
        self.view.on_unlock_track(self.unlocked_tracks)

    @model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number
        self.view.on_unlock_track(track_number)

    def on_save_state(self):
        self.user_db_cursor.execute('UPDATE game_progress SET unlocked_tracks = ?', (self.unlocked_tracks, ))

    def on_clear_trains_info(self):
        self.user_db_cursor.execute('DELETE FROM trains')

    def on_create_train(self, train_id, cars, track, train_route, status, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money):
        return create_train(self.user_db_connection, self.user_db_cursor, self.config_db_cursor, self.view.surface,
                            self.view.batches, self.view.groups, self.controller, train_id, cars, track, train_route,
                            status, direction, new_direction, current_direction, priority, boarding_time, exp, money,
                            self.unlocked_car_collections)
