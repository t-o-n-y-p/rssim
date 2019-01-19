from random import choice, seed

from .model_base import Model
from ctrl import TrainController
from .train_model import TrainModel
from view import TrainView
from car_skins import CAR_HEAD_IMAGE, CAR_MID_IMAGE, CAR_TAIL_IMAGE, BOARDING_LIGHT_IMAGE, CAR_COLLECTIONS


def create_train(user_db_connection, user_db_cursor, config_db_cursor, surface, batches, groups, map_controller,
                 train_id, cars, track, train_route, state, direction, new_direction,
                 current_direction, priority, boarding_time, exp, money):
    controller = TrainController(map_controller)
    controller.train_id = train_id
    model = TrainModel(user_db_connection, user_db_cursor, config_db_cursor)
    seed()
    model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                        priority, boarding_time, exp, money, choice(list(range(CAR_COLLECTIONS))))
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


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class MapModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()
        self.view.on_unlock_track(self.unlocked_tracks)

    @_model_is_active
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
                            status, direction, new_direction, current_direction, priority, boarding_time, exp, money)
