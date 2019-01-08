from pyglet.image import load
from random import choice, seed

from ctrl import AppController, GameController, MapController, SettingsController, FPSController, SchedulerController, \
                 SignalController, TrainRouteController, RailroadSwitchController, CrossoverController, \
                 TrainController, DispatcherController, ConstructorController
from model import AppModel, GameModel, MapModel, SettingsModel, FPSModel, SchedulerModel, SignalModel, TrainRouteModel,\
                  RailroadSwitchModel, CrossoverModel, TrainModel, DispatcherModel, ConstructorModel
from view import AppView, GameView, MapView, SettingsView, FPSView, SchedulerView, SignalView, TrainRouteView, \
                 RailroadSwitchView, CrossoverView, TrainView, DispatcherView, ConstructorView

car_collections = 4

car_head_image = []
for i in range(car_collections):
    car_head_image.append([])
    for j in range(4):
        car_head_image[i].append(load(f'img/cars/{i}/car_head_{j}.png'))

for i in range(len(car_head_image)):
    for j in range(4):
        car_head_image[i][j].anchor_x = car_head_image[i][j].width // 2
        car_head_image[i][j].anchor_y = car_head_image[i][j].height // 2

car_mid_image = []
for i in range(car_collections):
    car_mid_image.append([])
    for j in range(4):
        car_mid_image[i].append(load(f'img/cars/{i}/car_mid_{j}.png'))

for i in range(len(car_mid_image)):
    for j in range(4):
        car_mid_image[i][j].anchor_x = car_mid_image[i][j].width // 2
        car_mid_image[i][j].anchor_y = car_mid_image[i][j].height // 2

car_tail_image = []
for i in range(car_collections):
    car_tail_image.append([])
    for j in range(4):
        car_tail_image[i].append(load(f'img/cars/{i}/car_tail_{j}.png'))

for i in range(len(car_tail_image)):
    for j in range(4):
        car_tail_image[i][j].anchor_x = car_tail_image[i][j].width // 2
        car_tail_image[i][j].anchor_y = car_tail_image[i][j].height // 2

boarding_light_image = []
for i in range(car_collections):
    boarding_light_image.append(load(f'img/cars/{i}/boarding_lights.png'))

for i in range(len(boarding_light_image)):
    boarding_light_image[i].anchor_x = boarding_light_image[i].width // 2
    boarding_light_image[i].anchor_y = boarding_light_image[i].height // 2


def create_app(user_db_connection, user_db_cursor, config_db_cursor, surface,
               batch, main_frame_batch, ui_batch, groups):
    controller = AppController()
    model = AppModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = AppView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.game = create_game(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                  batch, main_frame_batch, ui_batch, groups, controller)
    controller.settings = create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                          batch, main_frame_batch, ui_batch, groups, controller)
    controller.fps = create_fps(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                batch, main_frame_batch, ui_batch, groups, controller)
    return controller


def create_game(user_db_connection, user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch,
                groups, app):
    controller = GameController(app)
    app.game = controller
    model = GameModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = GameView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    controller.map = create_map(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                batch, main_frame_batch, ui_batch, groups, controller)
    return controller


def create_map(user_db_connection, user_db_cursor, config_db_cursor, surface,
               batch, main_frame_batch, ui_batch, groups, game):
    controller = MapController(game)
    game.map = controller
    controller.scheduler = create_scheduler(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                            batch, main_frame_batch, ui_batch, groups, controller)
    controller.dispatcher = create_dispatcher(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                              batch, main_frame_batch, ui_batch, groups, controller)
    controller.constructor = create_constructor(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                                batch, main_frame_batch, ui_batch, groups, controller)
    user_db_cursor.execute('SELECT train_id FROM trains')
    train_ids = user_db_cursor.fetchall()
    if train_ids is not None:
        for i in train_ids:
            controller.trains[i[0]] = create_train(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                                   batch, main_frame_batch, ui_batch, groups, controller, i[0])

    config_db_cursor.execute('''SELECT DISTINCT track FROM signal_config''')
    signal_index = config_db_cursor.fetchall()
    for i in signal_index:
        controller.signals[i[0]] = {}

    config_db_cursor.execute('''SELECT track, base_route FROM signal_config''')
    signal_ids = config_db_cursor.fetchall()
    for i in signal_ids:
        controller.signals[i[0]][i[1]] \
            = create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface,
                            batch, main_frame_batch, ui_batch, groups, controller, i[0], i[1])
        controller.signals_list.append(controller.signals[i[0]][i[1]])

    config_db_cursor.execute('''SELECT DISTINCT track FROM train_route_config''')
    train_route_index = config_db_cursor.fetchall()
    for i in train_route_index:
        controller.train_routes[i[0]] = {}

    config_db_cursor.execute('''SELECT track, train_route FROM train_route_config''')
    train_route_ids = config_db_cursor.fetchall()
    for i in train_route_ids:
        controller.train_routes[i[0]][i[1]] \
            = create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                 batch, main_frame_batch, ui_batch, groups, controller, i[0], i[1])
        controller.train_routes_sorted_list.append(controller.train_routes[i[0]][i[1]])

    user_db_cursor.execute('''SELECT DISTINCT track_param_1 FROM switches''')
    switch_track_param_1 = user_db_cursor.fetchall()
    for i in switch_track_param_1:
        controller.switches[i[0]] = {}

    user_db_cursor.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM switches''')
    switch_track_param_2 = user_db_cursor.fetchall()
    for i in switch_track_param_2:
        controller.switches[i[0]][i[1]] = {}

    user_db_cursor.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches''')
    switch_types = user_db_cursor.fetchall()
    for i in switch_types:
        controller.switches[i[0]][i[1]][i[2]] \
            = create_railroad_switch(user_db_connection, user_db_cursor, config_db_cursor, surface,
                                     batch, main_frame_batch, ui_batch, groups, controller, i[0], i[1], i[2])
        controller.switches_list.append(controller.switches[i[0]][i[1]][i[2]])

    user_db_cursor.execute('''SELECT DISTINCT track_param_1 FROM crossovers''')
    crossovers_track_param_1 = user_db_cursor.fetchall()
    for i in crossovers_track_param_1:
        controller.crossovers[i[0]] = {}

    user_db_cursor.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers''')
    crossovers_track_param_2 = user_db_cursor.fetchall()
    for i in crossovers_track_param_2:
        controller.crossovers[i[0]][i[1]] = {}

    user_db_cursor.execute('''SELECT track_param_1, track_param_2, crossover_type FROM crossovers''')
    crossovers_types = user_db_cursor.fetchall()
    for i in crossovers_types:
        controller.crossovers[i[0]][i[1]][i[2]] \
            = create_crossover(user_db_connection, user_db_cursor, config_db_cursor, surface,
                               batch, main_frame_batch, ui_batch, groups, controller, i[0], i[1], i[2])
        controller.crossovers_list.append(controller.crossovers[i[0]][i[1]][i[2]])

    model = MapModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = MapView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_settings(user_db_connection, user_db_cursor, config_db_cursor, surface,
                    batch, main_frame_batch, ui_batch, groups, app):
    controller = SettingsController(app)
    app.settings = controller
    model = SettingsModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SettingsView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_fps(user_db_connection, user_db_cursor, config_db_cursor, surface,
               batch, main_frame_batch, ui_batch, groups, app):
    controller = FPSController(app)
    app.fps = controller
    model = FPSModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = FPSView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_scheduler(user_db_connection, user_db_cursor, config_db_cursor, surface,
                     batch, main_frame_batch, ui_batch, groups, map_controller):
    controller = SchedulerController(map_controller)
    model = SchedulerModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = SchedulerView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_signal(user_db_connection, user_db_cursor, config_db_cursor, surface,
                  batch, main_frame_batch, ui_batch, groups, map_controller, track, base_route):
    controller = SignalController(map_controller)
    controller.track = track
    controller.base_route = base_route
    model = SignalModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_signal_setup(track, base_route)
    view = SignalView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_train_route(user_db_connection, user_db_cursor, config_db_cursor, surface,
                       batch, main_frame_batch, ui_batch, groups, map_controller, track, train_route):
    controller = TrainRouteController(map_controller)
    controller.track = track
    controller.train_route = train_route
    model = TrainRouteModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_train_route_setup(track, train_route)
    if model.opened:
        controller.parent_controller.on_set_trail_points(model.last_opened_by, model.trail_points_v2)

    view = TrainRouteView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_railroad_switch(user_db_connection, user_db_cursor, config_db_cursor, surface,
                           batch, main_frame_batch, ui_batch, groups, map_controller,
                           track_param_1, track_param_2, switch_type):
    controller = RailroadSwitchController(map_controller)
    controller.track_param_1 = track_param_1
    controller.track_param_2 = track_param_2
    controller.switch_type = switch_type
    model = RailroadSwitchModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_railroad_switch_setup(track_param_1, track_param_2, switch_type)
    view = RailroadSwitchView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_crossover(user_db_connection, user_db_cursor, config_db_cursor, surface,
                     batch, main_frame_batch, ui_batch, groups, map_controller,
                     track_param_1, track_param_2, crossover_type):
    controller = CrossoverController(map_controller)
    controller.track_param_1 = track_param_1
    controller.track_param_2 = track_param_2
    controller.crossover_type = crossover_type
    model = CrossoverModel(user_db_connection, user_db_cursor, config_db_cursor)
    model.on_crossover_setup(track_param_1, track_param_2, crossover_type)
    view = CrossoverView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_train(user_db_connection, user_db_cursor, config_db_cursor, surface,
                 batch, main_frame_batch, ui_batch, groups, map_controller,
                 train_id, cars=None, track=None, train_route=None, state=None, direction=None, new_direction=None,
                 current_direction=None, priority=None, boarding_time=None, exp=None, money=None,
                 created_by='database'):
    controller = TrainController(map_controller)
    controller.train_id = train_id
    model = TrainModel(user_db_connection, user_db_cursor, config_db_cursor)
    if created_by == 'dispatcher':
        seed()
        model.on_train_init(cars, track, train_route, state, direction, new_direction, current_direction,
                            priority, boarding_time, exp, money, choice(list(range(car_collections))))
    else:
        model.on_train_setup(train_id)

    view = TrainView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
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


def create_dispatcher(user_db_connection, user_db_cursor, config_db_cursor, surface,
                      batch, main_frame_batch, ui_batch, groups, map_controller):
    controller = DispatcherController(map_controller)
    model = DispatcherModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = DispatcherView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller


def create_constructor(user_db_connection, user_db_cursor, config_db_cursor, surface,
                       batch, main_frame_batch, ui_batch, groups, map_controller):
    controller = ConstructorController(map_controller)
    model = ConstructorModel(user_db_connection, user_db_cursor, config_db_cursor)
    view = ConstructorView(user_db_cursor, config_db_cursor, surface, batch, main_frame_batch, ui_batch, groups)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    return controller
