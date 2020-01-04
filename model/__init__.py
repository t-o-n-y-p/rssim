from typing import Final

from database import USER_DB_CURSOR


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
MAP_ENTRY_UNLOCK_CONDITIONS: Final = (((1, 0), (1, 0), (21, 0), (22, 0)),
                                      ((1, 2), (1, 2), (1, 2), (3, 3), (1, 2), (4, 3), (1, 2), (7, 3), (1, 2), (8, 3)))
JOINT_ENTRIES: Final = (((), (), (), ()),
                        ((2, 4, 6, 8), (), (0, 4, 6, 8), (), (0, 2, 6, 8), (), (0, 2, 4, 8), (), (0, 2, 4, 6), ()))
# track, environment and shop stage state matrix properties
LOCKED: Final = 0                                      # property #0 indicates if track/env. is locked
UNDER_CONSTRUCTION: Final = 1                          # property #1 indicates if track/env. is under construction
CONSTRUCTION_TIME: Final = 2                           # property #2 indicates construction time left
UNLOCK_CONDITION_FROM_LEVEL: Final = 3                 # property #3 indicates if unlock condition from level is met
UNLOCK_CONDITION_FROM_PREVIOUS_TRACK: Final = 4        # property #4 indicates if unlock previous track condition is met
UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT: Final = 4  # property #4 indicates if unlock previous env. condition is met
UNLOCK_CONDITION_FROM_PREVIOUS_STAGE: Final = 4        # property #4 indicates if unlock previous stage condition is met
UNLOCK_CONDITION_FROM_ENVIRONMENT: Final = 5           # indicates if unlock environment condition is met (tracks only)
UNLOCK_AVAILABLE: Final = 6                            # property #6 indicates if all unlock conditions are met
PRICE: Final = 7                                       # property #7 indicates track/env. price
MAX_CONSTRUCTION_TIME: Final = 8
LEVEL_REQUIRED: Final = 9                              # property #9 indicates required level for this track/env.
ENVIRONMENT_REQUIRED: Final = 10                       # property #10 indicates required environment tier (tracks only)
HOURLY_PROFIT: Final = 11
STORAGE_CAPACITY: Final = 12
EXP_BONUS: Final = 13
# track is selected from this list based on direction and new direction
PASSENGER_MAP_MAIN_PRIORITY_TRACKS: Final = (
                                                (
                                                    (20, 18, 16, 14, 12, 10, 8, 6, 4),      # 0 -> 0
                                                    (20, 18, 16, 14, 12, 10, 8, 6, 4),      # 0 -> 1 (not used)
                                                    (32, 30, 28, 26, 24, 22),               # 0 -> 2
                                                    (23, 21)                                # 0 -> 3
                                                ),
                                                (
                                                    (19, 17, 15, 13, 11, 9, 7, 5, 3),       # 1 -> 0 (not used)
                                                    (19, 17, 15, 13, 11, 9, 7, 5, 3),       # 1 -> 1
                                                    (24, 22),                               # 1 -> 2
                                                    (31, 29, 27, 25, 23, 21)                # 1 -> 3
                                                ),
                                                (
                                                    (31, 29, 27, 25, 23, 21),               # 2 -> 0
                                                    (23, 21),                               # 2 -> 1
                                                    (),                                     # 2 -> 2 (impossible)
                                                    (31, 29, 27, 25, 23, 21)                # 2 -> 3
                                                ),
                                                (
                                                    (24, 22),                               # 3 -> 0
                                                    (32, 30, 28, 26, 24, 22),               # 3 -> 1
                                                    (32, 30, 28, 26, 24, 22),               # 3 -> 2
                                                    ()                                      # 3 -> 3 (impossible)
                                                )
                                            )
FREIGHT_MAP_MAIN_PRIORITY_TRACKS = (
                                       (
                                           (2, 1),                                          # 0 -> 0
                                           (16, 15, 14, 13, 12, 11, 2, 1)                   # 0 -> 1
                                       ),
                                       (
                                           (2, 1),                                          # 1 -> 0
                                           (2, 1)                                           # 1 -> 1
                                       ),
                                       (
                                           (),                                              # 2 -> 0 (impossible)
                                           (),                                              # 2 -> 1 (not used)
                                           (5, 3)                                           # 2 -> 2
                                       ),
                                       (
                                           (),                                              # 3 -> 0 (impossible)
                                           (),                                              # 3 -> 1 (not used)
                                           (5, 3),                                          # 3 -> 2
                                           (5, 3)                                           # 3 -> 3
                                       ),
                                       (
                                           (),                                              # 4 -> 0 (impossible)
                                           (),                                              # 4 -> 1 (not used)
                                           (),                                              # 4 -> 2 (impossible)
                                           (),                                              # 4 -> 3 (not used)
                                           (6, 4)                                           # 4 -> 4
                                       ),
                                       (
                                           (),                                              # 5 -> 0 (impossible)
                                           (),                                              # 5 -> 1 (not used)
                                           (),                                              # 5 -> 2 (impossible)
                                           (),                                              # 5 -> 3 (not used)
                                           (6, 4),                                          # 5 -> 4
                                           (6, 4)                                           # 5 -> 5
                                       ),
                                       (
                                           (),                                              # 6 -> 0 (impossible)
                                           (),                                              # 6 -> 1 (not used)
                                           (),                                              # 6 -> 2 (impossible)
                                           (),                                              # 6 -> 3 (not used)
                                           (),                                              # 6 -> 4 (impossible)
                                           (),                                              # 6 -> 5 (not used)
                                           (9, 7)                                           # 6 -> 6
                                       ),
                                       (
                                           (),                                              # 7 -> 0 (impossible)
                                           (),                                              # 7 -> 1 (not used)
                                           (),                                              # 7 -> 2 (impossible)
                                           (),                                              # 7 -> 3 (not used)
                                           (),                                              # 7 -> 4 (impossible)
                                           (),                                              # 7 -> 5 (not used)
                                           (9, 7),                                          # 7 -> 6
                                           (9, 7)                                           # 7 -> 7
                                       ),
                                       (
                                           (),                                              # 8 -> 0 (impossible)
                                           (),                                              # 8 -> 1 (not used)
                                           (),                                              # 8 -> 2 (impossible)
                                           (),                                              # 8 -> 3 (not used)
                                           (),                                              # 8 -> 4 (impossible)
                                           (),                                              # 8 -> 5 (not used)
                                           (),                                              # 8 -> 6 (impossible)
                                           (),                                              # 8 -> 7 (not used)
                                           (10, 8)                                          # 8 -> 8
                                       ),
                                       (
                                           (),                                              # 9 -> 0 (impossible)
                                           (),                                              # 9 -> 1 (not used)
                                           (),                                              # 9 -> 2 (impossible)
                                           (),                                              # 9 -> 3 (not used)
                                           (),                                              # 9 -> 4 (impossible)
                                           (),                                              # 9 -> 5 (not used)
                                           (),                                              # 9 -> 6 (impossible)
                                           (),                                              # 9 -> 7 (not used)
                                           (10, 8),                                         # 9 -> 8
                                           (10, 8)                                          # 9 -> 9
                                       )
                                   )
# track is selected from this list based on direction and new direction
PASSENGER_MAP_PASS_THROUGH_PRIORITY_TRACKS: Final = ((2, 1),                                # 0 -> 0
                                                     (1, 2))                                # 1 -> 1
# base_schedule matrix properties
TRAIN_ID: Final = 0                            # property #0 indicates train identification number
ARRIVAL_TIME: Final = 1                        # property #1 indicates arrival time
DIRECTION: Final = 2                           # property #2 indicates direction
NEW_DIRECTION: Final = 3                       # property #3 indicates new direction
CARS: Final = 4                                # property #4 indicates number of cars
STOP_TIME: Final = 5                           # property #5 indicates how much stop time left
EXP: Final = 6                                 # property #6 indicates how much exp the train gives
MONEY: Final = 7                               # property #7 indicates how much money the train gives
SWITCH_DIRECTION_REQUIRED: Final = 8
# base route types
ENTRY_BASE_ROUTE: Final = (('left_entry_base_route', 'right_entry_base_route',
                            'left_side_entry_base_route', 'right_side_entry_base_route'),
                           ('left_entry_base_route', 'right_entry_base_route',
                            'left_entry_base_route', 'right_side_1_entry_base_route',
                            'left_entry_base_route', 'right_side_2_entry_base_route',
                            'left_entry_base_route', 'right_side_3_entry_base_route',
                            'left_entry_base_route', 'right_side_4_entry_base_route')
                           )
# train route types
ENTRY_TRAIN_ROUTE: Final = (('left_entry', 'right_entry', 'left_side_entry', 'right_side_entry'),
                            ('left_entry', 'right_entry', 'left_entry', 'right_side_1_entry',
                             'left_entry', 'right_side_2_entry', 'left_entry', 'right_side_3_entry',
                             'left_entry', 'right_side_4_entry'))
EXIT_TRAIN_ROUTE: Final = (('right_exit', 'left_exit', 'right_side_exit', 'left_side_exit'),
                           ('right_exit', 'left_exit', 'right_side_1_exit', 'left_exit',
                            'right_side_2_exit', 'left_exit', 'right_side_3_exit', 'left_exit',
                            'right_side_4_exit', 'left_exit'))
APPROACHING_TRAIN_ROUTE: Final = (('left_approaching', 'right_approaching',
                                   'left_side_approaching', 'right_side_approaching'),
                                  ('left_approaching', 'right_approaching',
                                   'left_side_1_approaching', 'right_side_1_approaching',
                                   'left_side_2_approaching', 'right_side_2_approaching',
                                   'left_side_3_approaching', 'right_side_3_approaching',
                                   'left_side_4_approaching', 'right_side_4_approaching')
                                  )
MAXIMUM_LEVEL: Final = 200              # maximum level the player can reach in the game
# track mask for entry base routes for all directions
ENTRY_TRACK_ID: Final = ((0, 0, 100, 100), (0, 0, 0, 100, 0, 200, 0, 300, 0, 400))
# schedule options matrix properties
ARRIVAL_TIME_MIN: Final = 0             # property #1 indicates min arrival time offset from the beginning of the cycle
ARRIVAL_TIME_MAX: Final = 1             # property #0 indicates max arrival time offset from the beginning of the cycle
# property #2 indicates direction
# property #3 indicates new direction
CARS_MIN: Final = 4                     # property #4 indicates min number of cars
CARS_MAX: Final = 5                     # property #5 indicates max number of cars
SWITCH_DIRECTION_FLAG = 6
# train acceleration matrix (numbers are offsets from the starting point), same is used to decelerate
PASSENGER_TRAIN_ACCELERATION_FACTOR: Final = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5,
                                              1.0, 1.0, 1.0, 1.0, 1.5, 1.5, 1.5, 2.0, 2.0, 2.5, 2.5, 3.0, 3.0, 3.5, 3.5,
                                              4.0, 4.0, 4.5, 4.5, 5.0, 5.5, 5.5, 6.0, 6.5, 6.5, 7.0, 7.5, 8.0, 8.0, 8.5,
                                              9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5,
                                              15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.5, 19.0, 19.5, 20.0, 21.0, 21.5,
                                              22.0, 23.0, 23.5, 24.0, 25.0, 25.5, 26.5, 27.0, 28.0, 28.5, 29.5, 30.0,
                                              31.0, 31.5, 32.5, 33.0, 34.0, 35.0, 35.5, 36.5, 37.5, 38.5, 39.0, 40.0,
                                              41.0, 42.0, 43.0, 43.5, 44.5, 45.5, 46.5, 47.5, 48.5, 49.5, 50.5, 51.5,
                                              52.5, 53.5, 54.5, 55.5, 56.5, 58.0, 59.0, 60.0, 61.0, 62.0, 63.5, 64.5,
                                              65.5, 66.5, 68.0, 69.0, 70.0, 71.5, 72.5, 74.0, 75.0, 76.5, 77.5, 79.0,
                                              80.0, 81.5, 82.5, 84.0, 85.0, 86.5, 88.0, 89.0, 90.5, 92.0, 93.0, 94.5,
                                              96.0, 97.5, 98.5, 100.0, 101.5, 103.0, 104.5, 106.0, 107.5, 109.0, 110.5,
                                              112.0, 113.5, 115.0, 116.5, 118.0, 119.5, 121.0, 122.5, 124.5, 126.0,
                                              127.5, 129.5, 131.0, 133.0, 134.5, 136.5, 138.0, 140.0, 142.0, 143.5,
                                              145.5, 147.5, 149.5, 151.5, 153.5, 155.5, 157.5, 159.5, 161.5, 163.5,
                                              165.5, 167.5, 169.5, 172.0, 174.0, 176.0, 178.5, 180.5, 183.0, 185.0,
                                              187.5, 189.5, 192.0, 194.5, 196.5, 199.0, 201.5, 204.0, 206.5, 209.0,
                                              211.5, 214.0, 216.5, 219.0, 221.5, 224.0, 226.5, 229.0, 232.0, 234.5,
                                              237.0, 240.0, 242.5, 245.5, 248.0, 251.0, 253.5, 256.5, 259.5, 262.0,
                                              265.0, 268.0, 271.0, 274.0, 277.0, 280.0, 283.0, 286.0, 289.0, 292.0,
                                              295.5, 298.5, 302.0, 305.0, 308.5, 312.0, 315.5, 319.0, 322.5, 326.5,
                                              330.0, 334.0, 337.5, 341.5, 345.5, 349.5, 353.5, 357.5, 361.5, 365.5,
                                              370.0, 374.0, 378.5, 382.5, 387.0, 391.5, 396.0, 400.5, 405.0, 410.0,
                                              414.5, 419.5, 424.0, 429.0, 434.0, 439.0, 444.0, 449.0, 454.0, 459.0,
                                              464.5, 469.5, 475.0, 480.0, 485.5, 491.0, 496.5, 502.0, 507.5, 513.5,
                                              519.0, 525.0, 530.5, 536.5, 542.5, 548.5, 554.5, 560.5, 566.5, 572.5,
                                              579.0, 585.0, 591.5, 597.5, 604.0, 610.5, 617.0, 623.5, 630.0, 637.0,
                                              643.5, 650.5, 657.0, 664.0, 671.0, 678.0, 685.0)
FREIGHT_TRAIN_ACCELERATION_FACTOR = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.25, 0.25, 0.25, 0.25, 0.25,
                                     0.5, 0.5, 0.5, 0.5, 0.75, 0.75, 0.75, 1.0, 1.0, 1.25, 1.25, 1.5, 1.5, 1.75, 1.75,
                                     2.0, 2.0, 2.25, 2.25, 2.5, 2.75, 2.75, 3.0, 3.25, 3.25, 3.5, 3.75, 4.0, 4.0, 4.25,
                                     4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0, 6.25, 6.5, 6.75, 7.0, 7.25, 7.5, 7.75, 8.0,
                                     8.25, 8.5, 8.75, 9.25, 9.5, 9.75, 10.0, 10.5, 10.75, 11.0, 11.5, 11.75, 12.0, 12.5,
                                     12.75, 13.25, 13.5, 14.0, 14.25, 14.75, 15.0, 15.5, 15.75, 16.25, 16.5, 17.0, 17.5,
                                     17.75, 18.25, 18.75, 19.25, 19.5, 20.0, 20.5, 21.0, 21.5, 21.75, 22.25, 22.75,
                                     23.25, 23.75, 24.25, 24.75, 25.25, 25.75, 26.25, 26.75, 27.25, 27.75, 28.25, 29.0,
                                     29.5, 30.0, 30.5, 31.0, 31.75, 32.25, 32.75, 33.25, 34.0, 34.5, 35.0, 35.75, 36.25,
                                     37.0, 37.5, 38.25, 38.75, 39.5, 40.0, 40.75, 41.25, 42.0, 42.5, 43.25, 44.0, 44.5,
                                     45.25, 46.0, 46.5, 47.25, 48.0, 48.75, 49.25, 50.0, 50.75, 51.5, 52.25, 53.0,
                                     53.75, 54.5, 55.25, 56.0, 56.75, 57.5, 58.25, 59.0, 59.75, 60.5, 61.25, 62.25,
                                     63.0, 63.75, 64.75, 65.5, 66.5, 67.25, 68.25, 69.0, 70.0, 71.0, 71.75, 72.75,
                                     73.75, 74.75, 75.75, 76.75, 77.75, 78.75, 79.75, 80.75, 81.75, 82.75, 83.75, 84.75,
                                     86.0, 87.0, 88.0, 89.25, 90.25, 91.5, 92.5, 93.75, 94.75, 96.0, 97.25, 98.25, 99.5,
                                     100.75, 102.0, 103.25, 104.5, 105.75, 107.0, 108.25, 109.5, 110.75, 112.0, 113.25,
                                     114.5, 116.0, 117.25, 118.5, 120.0, 121.25, 122.75, 124.0, 125.5, 126.75, 128.25,
                                     129.75, 131.0, 132.5, 134.0, 135.5, 137.0, 138.5, 140.0, 141.5, 143.0, 144.5,
                                     146.0, 147.75, 149.25, 151.0, 152.5, 154.25, 156.0, 157.75, 159.5, 161.25, 163.25,
                                     165.0, 167.0)
MONEY_LIMIT: Final = 9999999999.0               # max amount of money the player can have
TRAIN_ID_LIMIT: Final = 1000000                 # train ID is limited to 6 digits, 999999 is followed by 0
FULLSCREEN_MODE_TURNED_OFF: Final = 0           # database value for fullscreen mode turned on
FULLSCREEN_MODE_TURNED_ON: Final = 1            # database value for fullscreen mode turned off
MAXIMUM_TRACK_NUMBER: Final = (32, 16)          # player can have maximum of 32 tracks on map 0 and 16 tracks on map 1
MAXIMUM_ENVIRONMENT_TIER: Final = (6, 3)        # environment tier 6 is final for map 0, for map 1 we have 3 tiers
FRAMES_IN_ONE_MINUTE: Final = 240               # indicates how many frames fit in 1 in-game minute
FRAMES_IN_ONE_HOUR: Final = 14400               # indicates how many frames fit in one in-game hour
DEFAULT_PRIORITY: Final = 10000000              # default priority for any new train created
PASS_THROUGH_BOARDING_TIME: Final = 480         # default boarding time for pass-through trains
PASSENGER_CAR_LENGTH: Final = 251               # length of the passenger car in pixels
FREIGHT_HEAD_TAIL_CAR_LENGTH: Final = 251       # length of the head/tail freight car in pixels
FREIGHT_MID_CAR_LENGTH: Final = 151             # length of the middle freight car in pixels
# when any track from this list is unlocked, new car collection is added
CAR_COLLECTION_UNLOCK_TRACK_LIST: Final = ((6, 10, 14, 18, 21, 22, 26, 30), (4, 8, 12))
TRACKS: Final = 0                                      # matrix #0 stores tracks state
ENVIRONMENT: Final = 1                                 # matrix #1 stores environment tiers state
CONSTRUCTOR_VIEW_TRACK_CELLS: Final = 4                # number of cells for tracks on constructor screen
CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS: Final = 4          # number of cells for environment tiers on constructor screen
# bonus code matrix properties
CODE_TYPE: Final = 0
BONUS_VALUE: Final = 1
REQUIRED_LEVEL: Final = 2
MAXIMUM_BONUS_TIME: Final = 3
ACTIVATION_AVAILABLE: Final = 4
ACTIVATIONS_LEFT: Final = 5
IS_ACTIVATED: Final = 6
BONUS_TIME: Final = 7
# threshold for shop storage notification (0 - empty, 1 - full)
SHOP_STORAGE_ALMOST_FULL_THRESHOLD: Final = 0.9
# ------------------- END CONSTANTS -------------------


class AppBaseModel:
    def __init__(self, controller, view, logger):
        self.logger = logger
        self.view = view
        self.controller = controller

    def on_save_state(self):
        pass


class GameBaseModel(AppBaseModel):
    def __init__(self, controller, view, logger):
        super().__init__(controller, view, logger)
        USER_DB_CURSOR.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('''SELECT level, money, exp_bonus_multiplier, money_bonus_multiplier, 
                                  construction_time_bonus_multiplier FROM game_progress''')
        self.level, self.money, self.exp_bonus_multiplier, self.money_bonus_multiplier, \
            self.construction_time_bonus_multiplier = USER_DB_CURSOR.fetchone()

    def on_update_time(self):
        self.game_time += 1
        self.view.on_update_time()

    def on_level_up(self):
        self.level += 1
        self.view.on_level_up()

    def on_add_money(self, money):
        self.money += min(MONEY_LIMIT - self.money, money)
        self.view.on_update_money(self.money)

    def on_pay_money(self, money):
        self.money -= money
        self.view.on_update_money(self.money)

    def on_activate_exp_bonus_code(self, value):
        self.exp_bonus_multiplier = round(1.0 + value, 2)
        self.view.on_activate_exp_bonus_code(value)

    def on_deactivate_exp_bonus_code(self):
        self.exp_bonus_multiplier = 1.0
        self.view.on_deactivate_exp_bonus_code()

    def on_activate_money_bonus_code(self, value):
        self.money_bonus_multiplier = round(1.0 + value, 2)
        self.view.on_activate_money_bonus_code(value)

    def on_deactivate_money_bonus_code(self):
        self.money_bonus_multiplier = 1.0
        self.view.on_deactivate_money_bonus_code()

    def on_activate_construction_time_bonus_code(self, value):
        self.construction_time_bonus_multiplier = round(1.0 + value, 2)
        self.view.on_activate_construction_time_bonus_code(value)

    def on_deactivate_construction_time_bonus_code(self):
        self.construction_time_bonus_multiplier = 1.0
        self.view.on_deactivate_construction_time_bonus_code()


class MapBaseModel(GameBaseModel):
    def __init__(self, controller, view, logger):
        super().__init__(controller, view, logger)
        self.locked = True

    def on_unlock(self):
        self.locked = False
        self.view.on_unlock()
