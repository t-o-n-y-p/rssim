from abc import ABC, abstractmethod
from math import log

import numpy

from database import *


def fullscreen_mode_available(fn):
    def _turn_fullscreen_mode_on_if_available(*args, **kwargs):
        if args[0].fullscreen_mode_available:
            fn(*args, **kwargs)

    return _turn_fullscreen_mode_on_if_available


def maximum_money_not_reached(fn):
    def _add_money_if_maximum_money_is_not_reached(*args, **kwargs):
        if args[0].money < MONEY_LIMIT:
            fn(*args, **kwargs)

    return _add_money_if_maximum_money_is_not_reached


def maximum_level_not_reached(fn):
    def _add_exp_if_max_level_not_reached(*args, **kwargs):
        if args[0].level < MAXIMUM_LEVEL:
            fn(*args, **kwargs)

    return _add_exp_if_max_level_not_reached


def money_target_exists(fn):
    def _update_money_progress_if_money_target_exists(*args, **kwargs):
        if args[0].money_target > 0:
            fn(*args, **kwargs)

    return _update_money_progress_if_money_target_exists


def train_has_passed_train_route_section(fn):
    def _allow_other_trains_to_pass_if_train_has_passed_train_route_section(*args, **kwargs):
        if args[1] >= args[0].checkpoints_v2[args[0].current_checkpoint]:
            fn(*args, **kwargs)

    return _allow_other_trains_to_pass_if_train_has_passed_train_route_section


def display_fps_enabled(fn):
    def _execute_if_display_fps_enabled(*args, **kwargs):
        if args[0].display_fps:
            fn(*args, **kwargs)

    return _execute_if_display_fps_enabled


# --------------------- CONSTANTS ---------------------
MAP_ENTRY_UNLOCK_CONDITIONS: Final = (
    ((1, 0), (1, 0), (21, 0), (22, 0)),
    ((1, 0), (1, 2), (1, 3), (3, 3), (1, 3), (4, 3), (1, 3), (7, 3), (1, 3), (8, 3))
)
JOINT_ENTRIES: Final = (
    ((), (), (), ()),
    ((2, 4, 6, 8), (), (0, 4, 6, 8), (), (0, 2, 6, 8), (), (0, 2, 4, 8), (), (0, 2, 4, 6), ())
)
# track is selected from this list based on direction and new direction
PASSENGER_MAP_MAIN_PRIORITY_TRACKS: Final = (
    (
        (20, 18, 16, 14, 12, 10, 8, 6, 4),  # 0 -> 0
        (20, 18, 16, 14, 12, 10, 8, 6, 4),  # 0 -> 1 (not used)
        (32, 30, 28, 26, 24, 22),  # 0 -> 2
        (23, 21)  # 0 -> 3
    ),
    (
        (19, 17, 15, 13, 11, 9, 7, 5, 3),  # 1 -> 0 (not used)
        (19, 17, 15, 13, 11, 9, 7, 5, 3),  # 1 -> 1
        (24, 22),  # 1 -> 2
        (31, 29, 27, 25, 23, 21)  # 1 -> 3
    ),
    (
        (31, 29, 27, 25, 23, 21),  # 2 -> 0
        (23, 21),  # 2 -> 1
        (),  # 2 -> 2 (impossible)
        (31, 29, 27, 25, 23, 21)  # 2 -> 3
    ),
    (
        (24, 22),  # 3 -> 0
        (32, 30, 28, 26, 24, 22),  # 3 -> 1
        (32, 30, 28, 26, 24, 22),  # 3 -> 2
        ()  # 3 -> 3 (impossible)
    )
)
FREIGHT_MAP_MAIN_PRIORITY_TRACKS: Final = (
    (
        (2, 1),  # 0 -> 0
        (16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1)  # 0 -> 1
    ),
    (
        (1, 2),  # 1 -> 0
        (1, 2)  # 1 -> 1
    ),
    (
        (),  # 2 -> 0 (impossible)
        (),  # 2 -> 1 (not used)
        (3, 5)  # 2 -> 2
    ),
    (
        (),  # 3 -> 0 (impossible)
        (),  # 3 -> 1 (not used)
        (5, 3),  # 3 -> 2
        (5, 3)  # 3 -> 3
    ),
    (
        (),  # 4 -> 0 (impossible)
        (),  # 4 -> 1 (not used)
        (),  # 4 -> 2 (impossible)
        (),  # 4 -> 3 (not used)
        (6, 4)  # 4 -> 4
    ),
    (
        (),  # 5 -> 0 (impossible)
        (),  # 5 -> 1 (not used)
        (),  # 5 -> 2 (impossible)
        (),  # 5 -> 3 (not used)
        (4, 6),  # 5 -> 4
        (4, 6)  # 5 -> 5
    ),
    (
        (),  # 6 -> 0 (impossible)
        (),  # 6 -> 1 (not used)
        (),  # 6 -> 2 (impossible)
        (),  # 6 -> 3 (not used)
        (),  # 6 -> 4 (impossible)
        (),  # 6 -> 5 (not used)
        (7, 9)  # 6 -> 6
    ),
    (
        (),  # 7 -> 0 (impossible)
        (),  # 7 -> 1 (not used)
        (),  # 7 -> 2 (impossible)
        (),  # 7 -> 3 (not used)
        (),  # 7 -> 4 (impossible)
        (),  # 7 -> 5 (not used)
        (9, 7),  # 7 -> 6
        (9, 7)  # 7 -> 7
    ),
    (
        (),  # 8 -> 0 (impossible)
        (),  # 8 -> 1 (not used)
        (),  # 8 -> 2 (impossible)
        (),  # 8 -> 3 (not used)
        (),  # 8 -> 4 (impossible)
        (),  # 8 -> 5 (not used)
        (),  # 8 -> 6 (impossible)
        (),  # 8 -> 7 (not used)
        (10, 8)  # 8 -> 8
    ),
    (
        (),  # 9 -> 0 (impossible)
        (),  # 9 -> 1 (not used)
        (),  # 9 -> 2 (impossible)
        (),  # 9 -> 3 (not used)
        (),  # 9 -> 4 (impossible)
        (),  # 9 -> 5 (not used)
        (),  # 9 -> 6 (impossible)
        (),  # 9 -> 7 (not used)
        (8, 10),  # 9 -> 8
        (8, 10)  # 9 -> 9
    )
)
# track is selected from this list based on direction and new direction
PASSENGER_MAP_PASS_THROUGH_PRIORITY_TRACKS: Final = (
    (2, 1),
    (1, 2)
)
# base route types
ENTRY_BASE_ROUTE: Final = (
    ('left_entry_base_route', 'right_entry_base_route', 'left_side_entry_base_route', 'right_side_entry_base_route'),
    ('left_entry_base_route', 'right_entry_base_route',
     'left_entry_base_route', 'right_side_1_entry_base_route',
     'left_entry_base_route', 'right_side_2_entry_base_route',
     'left_entry_base_route', 'right_side_3_entry_base_route',
     'left_entry_base_route', 'right_side_4_entry_base_route')
)
# train route types
ENTRY_TRAIN_ROUTE: Final = (
    ('left_entry', 'right_entry', 'left_side_entry', 'right_side_entry'),
    ('left_entry', 'right_entry', 'left_entry', 'right_side_1_entry', 'left_entry', 'right_side_2_entry',
     'left_entry', 'right_side_3_entry', 'left_entry', 'right_side_4_entry')
)
EXIT_TRAIN_ROUTE: Final = (
    ('right_exit', 'left_exit', 'right_side_exit', 'left_side_exit'),
    ('right_exit', 'left_exit', 'right_side_1_exit', 'left_exit', 'right_side_2_exit', 'left_exit',
     'right_side_3_exit', 'left_exit', 'right_side_4_exit', 'left_exit')
)
APPROACHING_TRAIN_ROUTE: Final = (
    ('left_approaching', 'right_approaching', 'left_side_approaching', 'right_side_approaching'),
    ('left_approaching', 'right_approaching',
     'left_side_1_approaching', 'right_side_1_approaching',
     'left_side_2_approaching', 'right_side_2_approaching',
     'left_side_3_approaching', 'right_side_3_approaching',
     'left_side_4_approaching', 'right_side_4_approaching')
)
MAXIMUM_LEVEL: Final = 200  # maximum level the player can reach in the game
# track mask for entry base routes for all directions
ENTRY_TRACK_ID: Final = ((0, 0, 100, 100), (0, 0, 0, 100, 0, 200, 0, 300, 0, 400))
TRAIN_MAXIMUM_SPEED: Final = (84, 24)
TRAIN_VELOCITY_BASE: Final = 1.03
TRAIN_VELOCITY_INTEGRATION_STEPS: Final = 10000
MONEY_LIMIT: Final = 9999999999.0  # max amount of money the player can have
TRAIN_ID_LIMIT: Final = 1000000  # train ID is limited to 6 digits, 999999 is followed by 0
FULLSCREEN_MODE_TURNED_OFF: Final = 0  # database value for fullscreen mode turned on
FULLSCREEN_MODE_TURNED_ON: Final = 1  # database value for fullscreen mode turned off
MAXIMUM_TRACK_NUMBER: Final = (32, 16)  # player can have maximum of 32 tracks on map 0 and 16 tracks on map 1
MAXIMUM_ENVIRONMENT_TIER: Final = (6, 3)  # environment tier 6 is final for map 0, for map 1 we have 3 tiers
DEFAULT_PRIORITY: Final = 10000000  # default priority for any new train created
PASS_THROUGH_BOARDING_TIME: Final = SECONDS_IN_ONE_MINUTE * 2  # default boarding time for pass-through trains
PASSENGER_CAR_LENGTH: Final = 251  # length of the passenger car in pixels
FREIGHT_HEAD_TAIL_CAR_LENGTH: Final = 251  # length of the head/tail freight car in pixels
FREIGHT_MID_CAR_LENGTH: Final = 151  # length of the middle freight car in pixels
# when any track from this list is unlocked, new car collection is added
CAR_COLLECTION_UNLOCK_TRACK_LIST: Final = ((6, 10, 14, 18, 21, 22, 26, 30), (4, 8, 12, 16))
# threshold for shop storage notification (0 - empty, 1 - full)
SHOP_STORAGE_ALMOST_FULL_THRESHOLD: Final = 0.9
ALLOWED_BONUS_CODE_INPUT: Final = 100
# ------------------- END CONSTANTS -------------------


def integrate(f, a, b, n=TRAIN_VELOCITY_INTEGRATION_STEPS):
    x = numpy.linspace(a + (b - a) / (2 * n), b - (b - a) / (2 * n), n)
    fx = f(x)
    area = numpy.sum(fx) * (b - a) / n
    return area


def train_speed_formula(t):
    return pow(TRAIN_VELOCITY_BASE, t) - 1


def get_braking_distance(t):
    return integrate(train_speed_formula, 0, t)


def get_distance(t1, t2):
    return integrate(train_speed_formula, t1, t2)


def get_speed_state_time(s, map_id):
    if s > get_braking_distance(log(TRAIN_MAXIMUM_SPEED[map_id] + 1, TRAIN_VELOCITY_BASE)) - 0.000001:
        return log(TRAIN_MAXIMUM_SPEED[map_id] + 1, TRAIN_VELOCITY_BASE)

    t1 = 0
    t2 = log(TRAIN_MAXIMUM_SPEED[map_id] + 1, TRAIN_VELOCITY_BASE)
    current_t = (t1 + t2) / 2
    while abs(get_braking_distance(current_t) - s) > 0.000001:
        if get_braking_distance(current_t) > s:
            t2 = current_t
        else:
            t1 = current_t

        current_t = (t1 + t2) / 2

    return current_t


def get_announcement_types_enabled(dt_multiplier):
    if dt_multiplier >= 10.0:
        return ARRIVAL_ANNOUNCEMENT, DEPARTURE_ANNOUNCEMENT, PASS_THROUGH_ANNOUNCEMENT
    else:
        return get_announcement_types_enabled(16.0) + (ARRIVAL_FINISHED_ANNOUNCEMENT, )


def get_announcement_types_diff(dt_multiplier_1, dt_multiplier_2):
    return [announcement for announcement in get_announcement_types_enabled(min(dt_multiplier_1, dt_multiplier_2))
            if a not in get_announcement_types_enabled(max(dt_multiplier_1, dt_multiplier_2))]


class AppBaseModel(ABC):
    def __init__(self, controller, view, logger):
        self.logger = logger
        self.view = view
        self.controller = controller

    @abstractmethod
    def on_save_state(self):
        pass


class GameBaseModel(AppBaseModel, ABC):
    def __init__(self, controller, view, logger):
        super().__init__(controller, view, logger)
        USER_DB_CURSOR.execute('SELECT * FROM epoch_timestamp')
        self.game_time, self.game_time_fraction, self.dt_multiplier = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT level, money, exp_bonus_multiplier, money_bonus_multiplier, 
                                  construction_time_bonus_multiplier FROM game_progress''')
        self.level, self.money, self.exp_bonus_multiplier, self.money_bonus_multiplier, \
            self.construction_time_bonus_multiplier = USER_DB_CURSOR.fetchone()

    def on_update_time(self, dt):
        self.game_time_fraction += dt * self.dt_multiplier
        self.game_time += int(self.game_time_fraction)
        self.game_time_fraction %= 1
        self.view.on_update_time(dt)

    def on_level_up(self):
        self.level += 1
        self.view.on_level_up()

    def on_add_money(self, money):
        self.money += min(MONEY_LIMIT - self.money, money)
        self.view.on_update_money(self.money)

    def on_deactivate_exp_bonus_code(self):
        self.exp_bonus_multiplier = 1.0
        self.view.on_deactivate_exp_bonus_code()

    def on_deactivate_money_bonus_code(self):
        self.money_bonus_multiplier = 1.0
        self.view.on_deactivate_money_bonus_code()

    def on_deactivate_construction_time_bonus_code(self):
        self.construction_time_bonus_multiplier = 1.0
        self.view.on_deactivate_construction_time_bonus_code()

    def on_dt_multiplier_update(self, dt_multiplier):
        self.dt_multiplier = dt_multiplier
        self.view.on_dt_multiplier_update(dt_multiplier)

    @final
    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money)

    @final
    def on_activate_exp_bonus_code(self, value):
        self.exp_bonus_multiplier = round(1.0 + value, 2)
        self.view.on_activate_exp_bonus_code(value)

    @final
    def on_activate_money_bonus_code(self, value):
        self.money_bonus_multiplier = round(1.0 + value, 2)
        self.view.on_activate_money_bonus_code(value)

    @final
    def on_activate_construction_time_bonus_code(self, value):
        self.construction_time_bonus_multiplier = round(1.0 + value, 2)
        self.view.on_activate_construction_time_bonus_code(value)


class MapBaseModel(GameBaseModel, ABC):
    def __init__(self, controller, view, map_id, logger):
        super().__init__(controller, view, logger)
        self.locked = True
        self.map_id = map_id

    def on_unlock(self):
        self.locked = False
        self.view.on_unlock()
