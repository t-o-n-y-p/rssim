from database import USER_DB_CONNECTION, USER_DB_CURSOR, CONFIG_DB_CURSOR


def fullscreen_mode_available(fn):
    """
    Use this decorator within App model to execute function only if fullscreen mode is enabled.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _turn_fullscreen_mode_on_if_available(*args, **kwargs):
        if args[0].fullscreen_mode_available:
            fn(*args, **kwargs)

    return _turn_fullscreen_mode_on_if_available


def maximum_money_not_reached(fn):
    """
    Use this decorator within Game or Constructor model to execute function
    only if money limit is not reached.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _add_money_if_maximum_money_is_not_reached(*args, **kwargs):
        if args[0].money < MONEY_LIMIT:
            fn(*args, **kwargs)

    return _add_money_if_maximum_money_is_not_reached


def maximum_level_not_reached(fn):
    """
    Use this decorator within Game model to execute function
    only if maximum level is not reached.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _add_exp_if_max_level_not_reached(*args, **kwargs):
        if args[0].level < MAXIMUM_LEVEL:
            fn(*args, **kwargs)

    return _add_exp_if_max_level_not_reached


def money_target_exists(fn):
    """
    Reserved for future use.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _update_money_progress_if_money_target_exists(*args, **kwargs):
        if args[0].money_target > 0:
            fn(*args, **kwargs)

    return _update_money_progress_if_money_target_exists


def train_has_passed_train_route_section(fn):
    """
    Use this decorator within Train route model to execute function
    only if train has just passed railroad switch, crossover or signal.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _allow_other_trains_to_pass_if_train_has_passed_train_route_section(*args, **kwargs):
        if args[1] >= args[0].checkpoints_v2[args[0].current_checkpoint]:
            fn(*args, **kwargs)

    return _allow_other_trains_to_pass_if_train_has_passed_train_route_section


def train_route_is_opened(fn):
    """
    Use this decorator within Train route model to execute function
    only if train route is opened.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_train_route_is_opened(*args, **kwargs):
        if args[0].opened:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_opened


def not_approaching_route(fn):
    """
    Use this decorator within Train route model to execute function
    only if route type is not "approaching".

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_train_route_is_not_approaching_route(*args, **kwargs):
        if len(args[0].train_route_sections) > 1:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_not_approaching_route


def display_fps_enabled(fn):
    """
    Use this decorator within FPS model to execute function
    only if display_fps flag is enabled.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _execute_if_display_fps_enabled(*args, **kwargs):
        if args[0].display_fps:
            fn(*args, **kwargs)

    return _execute_if_display_fps_enabled


# --------------------- CONSTANTS ---------------------
LEFT_SIDE_ENTRY_FIRST_TRACK = 21        # first available track for left side route is 21st
RIGHT_SIDE_ENTRY_FIRST_TRACK = 22       # first available track for right side route is 22nd
# track, environment and shop stage state matrix properties
LOCKED = 0                                      # property #0 indicates if track/env. is locked
UNDER_CONSTRUCTION = 1                          # property #1 indicates if track/env. is under construction
CONSTRUCTION_TIME = 2                           # property #2 indicates construction time left
UNLOCK_CONDITION_FROM_LEVEL = 3                 # property #3 indicates if unlock condition from level is met
UNLOCK_CONDITION_FROM_PREVIOUS_TRACK = 4        # property #4 indicates if unlock condition from previous track is met
UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT = 4  # property #4 indicates if unlock condition from previous env. is met
UNLOCK_CONDITION_FROM_PREVIOUS_STAGE = 4        # property #4 indicates if unlock condition from previous stage is met
UNLOCK_CONDITION_FROM_ENVIRONMENT = 5           # indicates if unlock condition from environment is met (tracks only)
UNLOCK_AVAILABLE = 6                            # property #6 indicates if all unlock conditions are met
PRICE = 7                                       # property #7 indicates track/env. price
LEVEL_REQUIRED = 8                              # property #8 indicates required level for this track/env.
ENVIRONMENT_REQUIRED = 9                        # property #9 indicates required environment tier (tracks only)
HOURLY_PROFIT = 10
STORAGE_CAPACITY = 11
EXP_BONUS = 12
# train direction codes
DIRECTION_FROM_LEFT_TO_RIGHT = 0        # train comes from the left entry or goes away through the right exit
DIRECTION_FROM_RIGHT_TO_LEFT = 1        # train comes from the right entry or goes away through the left exit
DIRECTION_FROM_LEFT_TO_RIGHT_SIDE = 2   # train comes from the left side entry or goes away through the right side exit
DIRECTION_FROM_RIGHT_TO_LEFT_SIDE = 3   # train comes from the right side entry or goes away through the left side exit
# track is selected from this list based on direction and new direction
MAIN_PRIORITY_TRACKS = (((20, 18, 16, 14, 12, 10, 8, 6, 4),         # 0 -> 0
                         (20, 18, 16, 14, 12, 10, 8, 6, 4),         # 0 -> 1 (not used)
                         (32, 30, 28, 26, 24, 22),                  # 0 -> 2
                         (23, 21)),                                 # 0 -> 3
                        ((19, 17, 15, 13, 11, 9, 7, 5, 3),          # 1 -> 0 (not used)
                         (19, 17, 15, 13, 11, 9, 7, 5, 3),          # 1 -> 1
                         (24, 22),                                  # 1 -> 2
                         (31, 29, 27, 25, 23, 21)),                 # 1 -> 3
                        ((31, 29, 27, 25, 23, 21),                  # 2 -> 0
                         (23, 21),                                  # 2 -> 1
                         (0,),                                      # 2 -> 2 (impossible)
                         (31, 29, 27, 25, 23, 21)),                 # 2 -> 3
                        ((24, 22),                                  # 3 -> 0
                         (32, 30, 28, 26, 24, 22),                  # 3 -> 1
                         (32, 30, 28, 26, 24, 22),                  # 3 -> 2
                         (0,)))                                     # 3 -> 3 (impossible)
# track is selected from this list based on direction and new direction
PASS_THROUGH_PRIORITY_TRACKS = ((2, 1),                             # 0 -> 0
                                (1, 2))                             # 1 -> 1
# base_schedule matrix properties
TRAIN_ID = 0                            # property #0 indicates train identification number
ARRIVAL_TIME = 1                        # property #1 indicates arrival time
DIRECTION = 2                           # property #2 indicates direction
NEW_DIRECTION = 3                       # property #3 indicates new direction
CARS = 4                                # property #4 indicates number of cars
STOP_TIME = 5                           # property #5 indicates how much stop time left
EXP = 6                                 # property #6 indicates how much exp the train gives
MONEY = 7                               # property #7 indicates how much money the train gives
# train route types
ENTRY_TRAIN_ROUTE = ('left_entry', 'right_entry',                   # entry train route types, directions 0 and 1
                     'left_side_entry', 'right_side_entry')         # entry train route types, directions 2 and 3
EXIT_TRAIN_ROUTE = ('right_exit', 'left_exit',                      # exit train route types, directions 0 and 1
                    'right_side_exit', 'left_side_exit')            # exit train route types, directions 2 and 3
APPROACHING_TRAIN_ROUTE = ('left_approaching',                      # approaching train route types, direction 0
                           'right_approaching',                     # approaching train route types, direction 1
                           'left_side_approaching',                 # approaching train route types, direction 2
                           'right_side_approaching')                # approaching train route types, direction 3
MAXIMUM_LEVEL = 200                     # maximum level the player can reach in the game
ENTRY_TRACK = (0, 0, 100, 100)          # track mask for entry base routes for directions 0-3
# schedule options matrix properties
ARRIVAL_TIME_MIN = 0                    # property #1 indicates min arrival time offset from the beginning of the cycle
ARRIVAL_TIME_MAX = 1                    # property #0 indicates max arrival time offset from the beginning of the cycle
# property #2 indicates direction
# property #3 indicates new direction
CARS_MIN = 4                            # property #4 indicates min number of cars
CARS_MAX = 5                            # property #5 indicates max number of cars
# train acceleration matrix (numbers are offsets from the starting point), same is used to decelerate
PASSENGER_TRAIN_ACCELERATION_FACTOR = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6,
                                       7, 7, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16,
                                       17, 17, 18, 18, 19, 20, 20, 21, 21, 22, 23, 23, 24, 25, 26, 26, 27, 28,
                                       29, 29, 30, 31, 32, 32, 33, 34, 35, 36, 37, 37, 38, 39, 40, 41, 42, 43, 44,
                                       45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
                                       64, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76, 78, 79, 80, 81, 83, 84, 85, 86,
                                       88, 89, 90, 92, 93, 95, 96, 97, 99, 100, 102, 103, 104, 106, 107, 109, 110,
                                       112, 113, 115, 116, 118, 119, 121, 123, 124, 126, 128, 129, 131, 133, 135,
                                       136, 138, 140, 142, 144, 146, 147, 149, 151, 153, 155, 157, 159, 161, 163,
                                       165, 168, 170, 172, 174, 176, 178, 181, 183, 185, 187, 190, 192, 194, 197,
                                       199, 201, 204, 206, 209, 211, 214, 216, 219, 221, 224, 227, 229, 232, 234,
                                       237, 240, 243, 245, 248, 251, 254, 256, 259, 262, 265, 268, 271, 274, 277,
                                       280, 283, 286, 289, 292, 295, 299, 302, 305, 309, 312, 316, 319, 323, 326,
                                       330, 334, 338, 341, 345, 349, 353, 357, 361, 366, 370, 374, 378, 383, 387,
                                       392, 396, 401, 405, 410, 415, 419, 424, 429, 434, 439, 444, 449, 454, 459,
                                       464, 470, 475, 480, 486, 491, 497, 502, 508, 513, 519, 525, 531, 536, 542,
                                       548, 554, 560, 566, 573, 579, 585, 591, 598, 604, 611, 617, 624, 630, 637,
                                       644, 650, 657, 664, 671, 678, 685)
MONEY_LIMIT = 9999999999.0              # max amount of money the player can have
TRAIN_ID_LIMIT = 1000000                # train ID is limited to 6 digits, 999999 is followed by 0
FULLSCREEN_MODE_TURNED_OFF = 0          # database value for fullscreen mode turned on
FULLSCREEN_MODE_TURNED_ON = 1           # database value for fullscreen mode turned off
MAXIMUM_TRACK_NUMBER = 32               # player can have maximum of 32 tracks
MAXIMUM_ENVIRONMENT_TIER = 6            # player can have environment tier 6 at most
FRAMES_IN_ONE_MINUTE = 240              # indicates how many frames fit in 1 in-game minute
FRAMES_IN_ONE_HOUR = 14400              # indicates how many frames fit in one in-game hour
DEFAULT_PRIORITY = 10000000             # default priority for any new train created
PASS_THROUGH_BOARDING_TIME = 480        # default boarding time for pass-through trains
PASSENGER_CAR_LENGTH = 251              # length of the passenger car in pixels
# when any track from this list is unlocked, new car collection is added
PASSENGER_CAR_COLLECTION_UNLOCK_TRACK_LIST = (6, 10, 14, 18, 21, 22, 26, 30)
TRACKS = 0                                      # matrix #0 stores tracks state
ENVIRONMENT = 1                                 # matrix #1 stores environment tiers state
CONSTRUCTOR_VIEW_TRACK_CELLS = 4                # number of cells for tracks on constructor screen
CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS = 4          # number of cells for environment tiers on constructor screen
# ------------------- END CONSTANTS -------------------


class Model:
    """
    Base class for all models in the app.
    """
    def __init__(self, logger):
        """
        Properties:
            logger                              telemetry instance
            view                                object view
            controller                          object controller
            is_activated                        indicates if model is active
            user_db_connection                  connection to the user DB (stores game state and user-defined settings)
            user_db_cursor                      user DB cursor (is used to execute user DB queries)
            config_db_cursor                    configuration DB cursor (is used to execute configuration DB queries)

        :param logger:                          telemetry instance
        """
        self.logger = logger
        self.view = None
        self.controller = None
        self.is_activated = False
        self.user_db_connection = USER_DB_CONNECTION
        self.user_db_cursor = USER_DB_CURSOR
        self.config_db_cursor = CONFIG_DB_CURSOR

    def on_activate_view(self):
        pass

    def on_save_state(self):
        """
        Saves model state to user progress database.
        """
        pass
