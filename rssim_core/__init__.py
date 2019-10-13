from controller.app_controller import AppController
from controller.main_menu_controller import MainMenuController
from controller.license_controller import LicenseController
from controller.onboarding_controller import OnboardingController
from controller.game_controller import GameController
from controller.map_controller.passenger_map_controller import PassengerMapController
from controller.settings_controller import SettingsController
from controller.fps_controller import FPSController
from controller.scheduler_controller.passenger_map_scheduler_controller import PassengerMapSchedulerController
from controller.signal_controller.passenger_map_signal_controller import PassengerMapSignalController
from controller.train_route_controller.passenger_train_route_controller import PassengerTrainRouteController
from controller.railroad_switch_controller.passenger_map_railroad_switch_controller \
    import PassengerMapRailroadSwitchController
from controller.crossover_controller.passenger_map_crossover_controller import PassengerMapCrossoverController
from controller.train_controller.passenger_train_controller import PassengerTrainController
from controller.dispatcher_controller.passenger_map_dispatcher_controller import PassengerMapDispatcherController
from controller.constructor_controller.passenger_map_constructor_controller import PassengerMapConstructorController
from controller.shop_controller.passenger_map_shop_controller import PassengerMapShopController
from controller.shop_placeholder_controller.passenger_map_shop_placeholder_controller \
    import PassengerMapShopPlaceholderController
from controller.shop_constructor_controller.passenger_map_constructor_controller \
    import PassengerMapShopConstructorController
from controller.bonus_code_controller import BonusCodeController
from model.app_model import AppModel
from model.main_menu_model import MainMenuModel
from model.license_model import LicenseModel
from model.onboarding_model import OnboardingModel
from model.game_model import GameModel
from model.map_model.passenger_map_model import PassengerMapModel
from model.settings_model import SettingsModel
from model.fps_model import FPSModel
from model.scheduler_model.passenger_map_scheduler_model import PassengerMapSchedulerModel
from model.signal_model.passenger_map_signal_model import PassengerMapSignalModel
from model.train_route_model.passenger_train_route_model import PassengerTrainRouteModel
from model.railroad_switch_model.passenger_map_railroad_switch_model import PassengerMapRailroadSwitchModel
from model.crossover_model.passenger_map_crossover_model import PassengerMapCrossoverModel
from model.train_model.passenger_train_model import PassengerTrainModel
from model.dispatcher_model.passenger_map_dispatcher_model import PassengerMapDispatcherModel
from model.constructor_model.passenger_map_constructor_model import PassengerMapConstructorModel
from model.shop_model.passenger_map_shop_model import PassengerMapShopModel
from model.shop_placeholder_model.passenger_map_shop_placeholder_model import PassengerMapShopPlaceholderModel
from model.shop_constructor_model.passenger_map_shop_constructor_model import PassengerMapShopConstructorModel
from model.bonus_code_model import BonusCodeModel
from view.app_view import AppView
from view.main_menu_view import MainMenuView
from view.license_view import LicenseView
from view.onboarding_view import OnboardingView
from view.game_view import GameView
from view.map_view.passenger_map_view import PassengerMapView
from view.settings_view import SettingsView
from view.fps_view import FPSView
from view.scheduler_view.passenger_map_scheduler_view import PassengerMapSchedulerView
from view.signal_view.passenger_map_signal_view import PassengerMapSignalView
from view.train_route_view.passenger_train_route_view import PassengerTrainRouteView
from view.railroad_switch_view.passenger_map_railroad_switch_view import PassengerMapRailroadSwitchView
from view.crossover_view.passenger_map_crossover_view import PassengerMapCrossoverView
from view.train_view.passenger_train_view import PassengerTrainView
from view.dispatcher_view.passenger_map_dispatcher_view import PassengerMapDispatcherView
from view.constructor_view.passenger_map_constructor_view import PassengerMapConstructorView
from view.shop_view.passenger_map_shop_view import PassengerMapShopView
from view.shop_placeholder_view.passenger_map_shop_placeholder_view import PassengerMapShopPlaceholderView
from view.shop_constructor_view.passenger_map_shop_constructor_view import PassengerMapShopConstructorView
from view.bonus_code_view import BonusCodeView
from ui.transition_animation import TransitionAnimation
from ui.fade_animation.fade_in_animation.app_fade_in_animation import AppFadeInAnimation
from ui.fade_animation.fade_in_animation.constructor_fade_in_animation import ConstructorFadeInAnimation
from ui.fade_animation.fade_in_animation.crossover_fade_in_animation import CrossoverFadeInAnimation
from ui.fade_animation.fade_in_animation.dispatcher_fade_in_animation import DispatcherFadeInAnimation
from ui.fade_animation.fade_in_animation.fps_fade_in_animation import FPSFadeInAnimation
from ui.fade_animation.fade_in_animation.game_fade_in_animation import GameFadeInAnimation
from ui.fade_animation.fade_in_animation.license_fade_in_animation import LicenseFadeInAnimation
from ui.fade_animation.fade_in_animation.main_menu_fade_in_animation import MainMenuFadeInAnimation
from ui.fade_animation.fade_in_animation.map_fade_in_animation import MapFadeInAnimation
from ui.fade_animation.fade_in_animation.onboarding_fade_in_animation import OnboardingFadeInAnimation
from ui.fade_animation.fade_in_animation.railroad_switch_fade_in_animation import RailroadSwitchFadeInAnimation
from ui.fade_animation.fade_in_animation.scheduler_fade_in_animation import SchedulerFadeInAnimation
from ui.fade_animation.fade_in_animation.settings_fade_in_animation import SettingsFadeInAnimation
from ui.fade_animation.fade_in_animation.signal_fade_in_animation import SignalFadeInAnimation
from ui.fade_animation.fade_in_animation.train_fade_in_animation import TrainFadeInAnimation
from ui.fade_animation.fade_in_animation.train_route_fade_in_animation import TrainRouteFadeInAnimation
from ui.fade_animation.fade_in_animation.shop_fade_in_animation import ShopFadeInAnimation
from ui.fade_animation.fade_in_animation.shop_placeholder_fade_in_animation import ShopPlaceholderFadeInAnimation
from ui.fade_animation.fade_in_animation.shop_constructor_fade_in_animation import ShopConstructorFadeInAnimation
from ui.fade_animation.fade_in_animation.bonus_code_fade_in_animation import BonusCodeFadeInAnimation
from ui.fade_animation.fade_out_animation.app_fade_out_animation import AppFadeOutAnimation
from ui.fade_animation.fade_out_animation.constructor_fade_out_animation import ConstructorFadeOutAnimation
from ui.fade_animation.fade_out_animation.crossover_fade_out_animation import CrossoverFadeOutAnimation
from ui.fade_animation.fade_out_animation.dispatcher_fade_out_animation import DispatcherFadeOutAnimation
from ui.fade_animation.fade_out_animation.fps_fade_out_animation import FPSFadeOutAnimation
from ui.fade_animation.fade_out_animation.game_fade_out_animation import GameFadeOutAnimation
from ui.fade_animation.fade_out_animation.license_fade_out_animation import LicenseFadeOutAnimation
from ui.fade_animation.fade_out_animation.main_menu_fade_out_animation import MainMenuFadeOutAnimation
from ui.fade_animation.fade_out_animation.map_fade_out_animation import MapFadeOutAnimation
from ui.fade_animation.fade_out_animation.onboarding_fade_out_animation import OnboardingFadeOutAnimation
from ui.fade_animation.fade_out_animation.railroad_switch_fade_out_animation import RailroadSwitchFadeOutAnimation
from ui.fade_animation.fade_out_animation.scheduler_fade_out_animation import SchedulerFadeOutAnimation
from ui.fade_animation.fade_out_animation.settings_fade_out_animation import SettingsFadeOutAnimation
from ui.fade_animation.fade_out_animation.signal_fade_out_animation import SignalFadeOutAnimation
from ui.fade_animation.fade_out_animation.train_fade_out_animation import TrainFadeOutAnimation
from ui.fade_animation.fade_out_animation.train_route_fade_out_animation import TrainRouteFadeOutAnimation
from ui.fade_animation.fade_out_animation.shop_fade_out_animation import ShopFadeOutAnimation
from ui.fade_animation.fade_out_animation.shop_placeholder_fade_out_animation import ShopPlaceholderFadeOutAnimation
from ui.fade_animation.fade_out_animation.shop_constructor_fade_out_animation import ShopConstructorFadeOutAnimation
from ui.fade_animation.fade_out_animation.bonus_code_fade_out_animation import BonusCodeFadeOutAnimation
from database import CONFIG_DB_CURSOR, USER_DB_CURSOR


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION = (0, 9, 8)                     # current app version
MIN_UPDATE_COMPATIBLE_VERSION = (0, 9, 8)       # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE = 8192                    # maximum texture resolution presented in the app
FPS_INTERVAL = 0.2                              # interval between FPS update
LOG_LEVEL_OFF = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG = 10                            # integer log level which includes all possible logs
DATABASE_SHA512 = 'ed7d4ee40b1244e394b1ec5ab305ba7f1d80d93b847867eaa583cd7ad576ca405aaf3bdd5e00c66a5a1e5e941b438706cbe7982faa062b76127d4a766d8b6b57'
MAXIMUM_DRAW_EVENTS_PER_FRAME = 1
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME = 1
# app version tuple members
MAJOR = 0
MINOR = 1
PATCH = 2
# ------------------- END CONSTANTS -------------------


def create_app(loader):
    controller = AppController(loader)
    controller.fade_in_animation = AppFadeInAnimation(controller)
    controller.fade_out_animation = AppFadeOutAnimation(controller)
    model = AppModel()
    view = AppView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    controller.main_menu = _create_main_menu(controller)
    controller.license = _create_license(controller)
    controller.onboarding = _create_onboarding(controller)
    controller.game = _create_game(controller)
    controller.settings = _create_settings(controller)
    controller.fps = _create_fps(controller)
    controller.bonus_code = _create_bonus_code(controller)
    controller.main_menu_to_game_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.main_menu.fade_out_animation,
                              fade_in_animation=controller.game.fade_in_animation)
    controller.game_to_main_menu_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.game.fade_out_animation,
                              fade_in_animation=controller.main_menu.fade_in_animation)
    controller.main_menu_to_license_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.main_menu.fade_out_animation,
                              fade_in_animation=controller.license.fade_in_animation)
    controller.license_to_main_menu_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.license.fade_out_animation,
                              fade_in_animation=controller.main_menu.fade_in_animation)
    controller.game_to_settings_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.game.fade_out_animation,
                              fade_in_animation=controller.settings.fade_in_animation)
    controller.settings_to_game_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.settings.fade_out_animation,
                              fade_in_animation=controller.game.fade_in_animation)
    controller.main_menu_to_onboarding_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.main_menu.fade_out_animation,
                              fade_in_animation=controller.onboarding.fade_in_animation)
    controller.onboarding_to_game_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.onboarding.fade_out_animation,
                              fade_in_animation=controller.game.fade_in_animation)
    controller.main_menu_to_settings_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.main_menu.fade_out_animation,
                              fade_in_animation=controller.settings.fade_in_animation)
    controller.settings_to_main_menu_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.settings.fade_out_animation,
                              fade_in_animation=controller.main_menu.fade_in_animation)
    controller.main_menu_to_bonus_code_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.main_menu.fade_out_animation,
                              fade_in_animation=controller.bonus_code.fade_in_animation)
    controller.bonus_code_to_main_menu_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.bonus_code.fade_out_animation,
                              fade_in_animation=controller.main_menu.fade_in_animation)
    controller.fade_in_animation.main_menu_fade_in_animation = controller.main_menu.fade_in_animation
    controller.fade_in_animation.license_fade_in_animation = controller.license.fade_in_animation
    controller.fade_in_animation.onboarding_fade_in_animation = controller.onboarding.fade_in_animation
    controller.fade_in_animation.game_fade_in_animation = controller.game.fade_in_animation
    controller.fade_in_animation.settings_fade_in_animation = controller.settings.fade_in_animation
    controller.fade_in_animation.fps_fade_in_animation = controller.fps.fade_in_animation
    controller.fade_out_animation.main_menu_fade_out_animation = controller.main_menu.fade_out_animation
    controller.fade_out_animation.license_fade_out_animation = controller.license.fade_out_animation
    controller.fade_out_animation.onboarding_fade_out_animation = controller.onboarding.fade_out_animation
    controller.fade_out_animation.game_fade_out_animation = controller.game.fade_out_animation
    controller.fade_out_animation.settings_fade_out_animation = controller.settings.fade_out_animation
    controller.fade_out_animation.fps_fade_out_animation = controller.fps.fade_out_animation
    return controller


def _create_game(app):
    controller = GameController(app)
    controller.fade_in_animation = GameFadeInAnimation(controller)
    controller.fade_out_animation = GameFadeOutAnimation(controller)
    model = GameModel()
    view = GameView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    controller.maps.append(_create_passenger_map(controller))
    for map_ in controller.maps:
        controller.fade_in_animation.map_fade_in_animations.append(map_.fade_in_animation)
        controller.fade_out_animation.map_fade_out_animations.append(map_.fade_out_animation)

    return controller


def _create_passenger_map(game):
    controller = PassengerMapController(game)
    controller.fade_in_animation = MapFadeInAnimation(controller)
    controller.fade_out_animation = MapFadeOutAnimation(controller)
    controller.scheduler = _create_passenger_map_scheduler(controller)
    controller.dispatcher = _create_passenger_map_dispatcher(controller)
    controller.constructor = _create_passenger_map_constructor(controller)
    # read train IDs from database, create trains and append them to both dictionary and list
    USER_DB_CURSOR.execute('SELECT train_id FROM trains WHERE map_id = 0')
    train_ids = USER_DB_CURSOR.fetchall()
    if train_ids is not None:
        for i in train_ids:
            controller.trains[i[0]] = _create_passenger_train(controller, i[0])
            controller.trains_list.append(controller.trains[i[0]])
            if controller.trains[i[0]].model.state in ('approaching', 'approaching_pass_through'):
                controller.dispatcher.on_add_train(controller.trains[i[0]])

    # read signal tracks and base routes from database, create signals and append them to both dictionary and list
    CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM signal_config WHERE map_id = 0''')
    signal_index = CONFIG_DB_CURSOR.fetchall()
    for i in signal_index:
        controller.signals[i[0]] = {}

    CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config WHERE map_id = 0''')
    signal_ids = CONFIG_DB_CURSOR.fetchall()
    for i in signal_ids:
        controller.signals[i[0]][i[1]] \
            = _create_passenger_map_signal(controller, i[0], i[1])
        controller.signals_list.append(controller.signals[i[0]][i[1]])
    # read train route tracks and types from database, create train routes and append them to both dictionary and list
    CONFIG_DB_CURSOR.execute('''SELECT DISTINCT track FROM train_route_config WHERE map_id = 0''')
    train_route_index = CONFIG_DB_CURSOR.fetchall()
    for i in train_route_index:
        controller.train_routes[i[0]] = {}

    CONFIG_DB_CURSOR.execute('''SELECT track, train_route FROM train_route_config WHERE map_id = 0''')
    train_route_ids = CONFIG_DB_CURSOR.fetchall()
    for i in train_route_ids:
        controller.train_routes[i[0]][i[1]] \
            = _create_passenger_train_route(controller, i[0], i[1])
        controller.train_routes_sorted_list.append(controller.train_routes[i[0]][i[1]])
    # read switches tracks from database, create switches and append them to both dictionary and list
    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM switches WHERE map_id = 0''')
    switch_track_param_1 = USER_DB_CURSOR.fetchall()
    for i in switch_track_param_1:
        controller.switches[i[0]] = {}

    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM switches WHERE map_id = 0''')
    switch_track_param_2 = USER_DB_CURSOR.fetchall()
    for i in switch_track_param_2:
        controller.switches[i[0]][i[1]] = {}

    USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches WHERE map_id = 0''')
    switch_types = USER_DB_CURSOR.fetchall()
    for i in switch_types:
        controller.switches[i[0]][i[1]][i[2]] \
            = _create_passenger_map_railroad_switch(controller, i[0], i[1], i[2])
        controller.switches_list.append(controller.switches[i[0]][i[1]][i[2]])
    # read crossovers tracks from database, create crossovers and append them to both dictionary and list
    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1 FROM crossovers WHERE map_id = 0''')
    crossovers_track_param_1 = USER_DB_CURSOR.fetchall()
    for i in crossovers_track_param_1:
        controller.crossovers[i[0]] = {}

    USER_DB_CURSOR.execute('''SELECT DISTINCT track_param_1, track_param_2 FROM crossovers WHERE map_id = 0''')
    crossovers_track_param_2 = USER_DB_CURSOR.fetchall()
    for i in crossovers_track_param_2:
        controller.crossovers[i[0]][i[1]] = {}

    USER_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, crossover_type FROM crossovers WHERE map_id = 0''')
    crossovers_types = USER_DB_CURSOR.fetchall()
    for i in crossovers_types:
        controller.crossovers[i[0]][i[1]][i[2]] \
            = _create_passenger_map_crossover(controller, i[0], i[1], i[2])
        controller.crossovers_list.append(controller.crossovers[i[0]][i[1]][i[2]])

    CONFIG_DB_CURSOR.execute('''SELECT COUNT(*) FROM shops_config WHERE map_id = 0''')
    number_of_shops = CONFIG_DB_CURSOR.fetchone()[0]
    for i in range(number_of_shops):
        controller.shops.append(_create_passenger_map_shop(controller, i))

    model = PassengerMapModel()
    view = PassengerMapView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    controller.fade_in_animation.constructor_fade_in_animation = controller.constructor.fade_in_animation
    controller.fade_in_animation.scheduler_fade_in_animation = controller.scheduler.fade_in_animation
    controller.fade_in_animation.dispatcher_fade_in_animation = controller.dispatcher.fade_in_animation
    controller.fade_out_animation.constructor_fade_out_animation = controller.constructor.fade_out_animation
    controller.fade_out_animation.scheduler_fade_out_animation = controller.scheduler.fade_out_animation
    controller.fade_out_animation.dispatcher_fade_out_animation = controller.dispatcher.fade_out_animation
    for signal in controller.signals_list:
        controller.fade_in_animation.signal_fade_in_animations.append(signal.fade_in_animation)
        controller.fade_out_animation.signal_fade_out_animations.append(signal.fade_out_animation)

    for switch in controller.switches_list:
        controller.fade_in_animation.railroad_switch_fade_in_animations.append(switch.fade_in_animation)
        controller.fade_out_animation.railroad_switch_fade_out_animations.append(switch.fade_out_animation)

    for crossover in controller.crossovers_list:
        controller.fade_in_animation.crossover_fade_in_animations.append(crossover.fade_in_animation)
        controller.fade_out_animation.crossover_fade_out_animations.append(crossover.fade_out_animation)

    for train in controller.trains_list:
        controller.fade_in_animation.train_fade_in_animations.append(train.fade_in_animation)
        controller.fade_out_animation.train_fade_out_animations.append(train.fade_out_animation)

    for train_route in controller.train_routes_sorted_list:
        controller.fade_in_animation.train_route_fade_in_animations.append(train_route.fade_in_animation)
        controller.fade_out_animation.train_route_fade_out_animations.append(train_route.fade_out_animation)

    for shop in controller.shops:
        controller.fade_in_animation.shop_fade_in_animations.append(shop.fade_in_animation)
        controller.fade_out_animation.shop_fade_out_animations.append(shop.fade_out_animation)

    return controller


def _create_settings(app):
    controller = SettingsController(app)
    controller.fade_in_animation = SettingsFadeInAnimation(controller)
    controller.fade_out_animation = SettingsFadeOutAnimation(controller)
    model = SettingsModel()
    view = SettingsView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_fps(app):
    controller = FPSController(app)
    controller.fade_in_animation = FPSFadeInAnimation(controller)
    controller.fade_out_animation = FPSFadeOutAnimation(controller)
    model = FPSModel()
    view = FPSView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_scheduler(map_controller):
    controller = PassengerMapSchedulerController(map_controller)
    controller.fade_in_animation = SchedulerFadeInAnimation(controller)
    controller.fade_out_animation = SchedulerFadeOutAnimation(controller)
    model = PassengerMapSchedulerModel()
    view = PassengerMapSchedulerView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.base_schedule = model.base_schedule
    view.on_init_content()
    return controller


def _create_passenger_map_signal(map_controller, track, base_route):
    controller = PassengerMapSignalController(map_controller, track, base_route)
    controller.fade_in_animation = SignalFadeInAnimation(controller)
    controller.fade_out_animation = SignalFadeOutAnimation(controller)
    model = PassengerMapSignalModel(track, base_route)
    view = PassengerMapSignalView(track, base_route)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_train_route(map_controller, track, train_route):
    controller = PassengerTrainRouteController(map_controller, track, train_route)
    controller.fade_in_animation = TrainRouteFadeInAnimation(controller)
    controller.fade_out_animation = TrainRouteFadeOutAnimation(controller)
    model = PassengerTrainRouteModel(track, train_route)
    if model.opened:
        controller.parent_controller.on_set_trail_points(model.last_opened_by,
                                                         model.trail_points_v2_head_tail, model.trail_points_v2_mid)

    view = PassengerTrainRouteView(track, train_route)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_railroad_switch(map_controller, track_param_1, track_param_2, switch_type):
    controller = PassengerMapRailroadSwitchController(map_controller, track_param_1, track_param_2, switch_type)
    controller.fade_in_animation = RailroadSwitchFadeInAnimation(controller)
    controller.fade_out_animation = RailroadSwitchFadeOutAnimation(controller)
    model = PassengerMapRailroadSwitchModel(track_param_1, track_param_2, switch_type)
    view = PassengerMapRailroadSwitchView(track_param_1, track_param_2, switch_type)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_crossover(map_controller, track_param_1, track_param_2, crossover_type):
    controller = PassengerMapCrossoverController(map_controller, track_param_1, track_param_2, crossover_type)
    controller.fade_in_animation = CrossoverFadeInAnimation(controller)
    controller.fade_out_animation = CrossoverFadeOutAnimation(controller)
    model = PassengerMapCrossoverModel(track_param_1, track_param_2, crossover_type)
    view = PassengerMapCrossoverView(track_param_1, track_param_2, crossover_type)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_train(map_controller, train_id):
    controller = PassengerTrainController(map_controller, train_id)
    controller.fade_in_animation = TrainFadeInAnimation(controller)
    controller.fade_out_animation = TrainFadeOutAnimation(controller)
    model = PassengerTrainModel(train_id)
    model.on_train_setup(train_id)
    view = PassengerTrainView(train_id)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_dispatcher(map_controller):
    controller = PassengerMapDispatcherController(map_controller)
    controller.fade_in_animation = DispatcherFadeInAnimation(controller)
    controller.fade_out_animation = DispatcherFadeOutAnimation(controller)
    model = PassengerMapDispatcherModel()
    view = PassengerMapDispatcherView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_constructor(map_controller):
    controller = PassengerMapConstructorController(map_controller)
    controller.fade_in_animation = ConstructorFadeInAnimation(controller)
    controller.fade_out_animation = ConstructorFadeOutAnimation(controller)
    model = PassengerMapConstructorModel()
    view = PassengerMapConstructorView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.construction_state_matrix = model.construction_state_matrix
    view.on_init_content()
    return controller


def _create_main_menu(app):
    controller = MainMenuController(app)
    controller.fade_in_animation = MainMenuFadeInAnimation(controller)
    controller.fade_out_animation = MainMenuFadeOutAnimation(controller)
    model = MainMenuModel()
    view = MainMenuView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_license(app):
    controller = LicenseController(app)
    controller.fade_in_animation = LicenseFadeInAnimation(controller)
    controller.fade_out_animation = LicenseFadeOutAnimation(controller)
    model = LicenseModel()
    view = LicenseView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_onboarding(app):
    controller = OnboardingController(app)
    controller.fade_in_animation = OnboardingFadeInAnimation(controller)
    controller.fade_out_animation = OnboardingFadeOutAnimation(controller)
    model = OnboardingModel()
    view = OnboardingView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_shop(map_controller, shop_id):
    controller = PassengerMapShopController(map_controller, shop_id)
    controller.fade_in_animation = ShopFadeInAnimation(controller)
    controller.fade_out_animation = ShopFadeOutAnimation(controller)
    controller.placeholder = _create_passenger_map_shop_placeholder(controller, shop_id)
    controller.shop_constructor = _create_passenger_map_shop_constructor(controller, shop_id)
    controller.placeholder_to_shop_constructor_transition_animation \
        = TransitionAnimation(fade_out_animation=controller.placeholder.fade_out_animation,
                              fade_in_animation=controller.shop_constructor.fade_in_animation)
    model = PassengerMapShopModel(shop_id)
    view = PassengerMapShopView(shop_id)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    controller.fade_in_animation.shop_placeholder_fade_in_animation = controller.placeholder.fade_in_animation
    controller.fade_in_animation.shop_constructor_fade_in_animation = controller.shop_constructor.fade_in_animation
    controller.fade_out_animation.shop_placeholder_fade_out_animation = controller.placeholder.fade_out_animation
    controller.fade_out_animation.shop_constructor_fade_out_animation = controller.shop_constructor.fade_out_animation
    return controller


def _create_passenger_map_shop_placeholder(shop_controller, shop_id):
    controller = PassengerMapShopPlaceholderController(shop_controller, shop_id)
    controller.fade_in_animation = ShopPlaceholderFadeInAnimation(controller)
    controller.fade_out_animation = ShopPlaceholderFadeOutAnimation(controller)
    model = PassengerMapShopPlaceholderModel(shop_id)
    view = PassengerMapShopPlaceholderView(shop_id)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.on_init_content()
    return controller


def _create_passenger_map_shop_constructor(shop_controller, shop_id):
    controller = PassengerMapShopConstructorController(shop_controller, shop_id)
    controller.fade_in_animation = ShopConstructorFadeInAnimation(controller)
    controller.fade_out_animation = ShopConstructorFadeOutAnimation(controller)
    model = PassengerMapShopConstructorModel(shop_id)
    view = PassengerMapShopConstructorView(shop_id)
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.shop_stages_state_matrix = model.shop_stages_state_matrix
    for i in range(1, 5):
        view.shop_stage_cells[i].data = view.shop_stages_state_matrix[i]

    view.on_init_content()
    return controller


def _create_bonus_code(app):
    controller = BonusCodeController(app)
    controller.fade_in_animation = BonusCodeFadeInAnimation(controller)
    controller.fade_out_animation = BonusCodeFadeOutAnimation(controller)
    model = BonusCodeModel()
    view = BonusCodeView()
    controller.model = model
    model.controller = controller
    controller.view = view
    view.on_assign_controller(controller)
    model.view = view
    view.bonus_code_matrix = model.bonus_code_matrix
    view.on_init_content()
    return controller
