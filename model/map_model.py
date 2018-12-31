from pyglet.image import load
from random import choice

from .model_base import Model
from ctrl import TrainController
from .train_model import TrainModel
from view import TrainView

car_head_image = [
    # collection 0
    [load('img/cars/0/car_head_0.png'), load('img/cars/0/car_head_1.png'),
     load('img/cars/0/car_head_2.png'), load('img/cars/0/car_head_3.png')],
]
for i in range(len(car_head_image)):
    for j in range(4):
        car_head_image[i][j].anchor_x = car_head_image[i][j].width // 2
        car_head_image[i][j].anchor_y = car_head_image[i][j].height // 2

car_mid_image = [
    # collection 0
    [load('img/cars/0/car_mid_0.png'), load('img/cars/0/car_mid_1.png'),
     load('img/cars/0/car_mid_2.png'), load('img/cars/0/car_mid_3.png')],
]
for i in range(len(car_mid_image)):
    for j in range(4):
        car_mid_image[i][j].anchor_x = car_mid_image[i][j].width // 2
        car_mid_image[i][j].anchor_y = car_mid_image[i][j].height // 2

car_tail_image = [
    # collection 0
    [load('img/cars/0/car_tail_0.png'), load('img/cars/0/car_tail_1.png'),
     load('img/cars/0/car_tail_2.png'), load('img/cars/0/car_tail_3.png')],
]
for i in range(len(car_tail_image)):
    for j in range(4):
        car_tail_image[i][j].anchor_x = car_tail_image[i][j].width // 2
        car_tail_image[i][j].anchor_y = car_tail_image[i][j].height // 2

boarding_light_image = [
    # collection 0
    load('img/cars/0/boarding_lights.png'),
]
for i in range(len(boarding_light_image)):
    boarding_light_image[i].anchor_x = boarding_light_image[i].width // 2
    boarding_light_image[i].anchor_y = boarding_light_image[i].height // 2


def create_train(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, groups, map_controller,
                 train_id, cars=None, track=None, train_route=None, state=None, direction=None, new_direction=None,
                 current_direction=None, priority=None, boarding_time=None, exp=None, money=None,
                 created_by='database'):
    controller = TrainController(map_controller)
    controller.train_id = train_id
    model = TrainModel(user_db_connection, user_db_cursor, config_db_cursor)
    if created_by == 'dispatcher':
        model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                            priority, boarding_time, exp, money, choice([0, 0]))
    else:
        model.on_train_setup(train_id)

    view = TrainView(user_db_cursor, config_db_cursor, surface, batch, groups)
    view.car_head_image = car_head_image
    view.car_mid_image = car_mid_image
    view.car_tail_image = car_tail_image
    view.boarding_light_image = boarding_light_image
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
                            self.view.batch, self.view.groups, self.controller, train_id, cars, track, train_route,
                            status, direction, new_direction, current_direction, priority, boarding_time, exp, money,
                            created_by='dispatcher')
