def model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


def fullscreen_mode_available(fn):
    def _turn_fullscren_mode_on_if_available(*args, **kwargs):
        if args[0].fullscreen_mode_available:
            fn(*args, **kwargs)

    return _turn_fullscren_mode_on_if_available


def maximum_money_not_reached(fn):
    def _add_money_if_maximum_money_is_not_reached(*args, **kwargs):
        if args[0].money < 99999999.0:
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


def train_route_is_opened(fn):
    def _handle_if_train_route_is_opened(*args, **kwargs):
        if args[0].opened:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_opened


def not_approaching_route(fn):
    def _handle_if_train_route_is_not_approaching_route(*args, **kwargs):
        if len(args[0].train_route_sections) > 1:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_not_approaching_route


# --------------------- CONSTANTS ---------------------
LOCKED = 0
UNDER_CONSTRUCTION = 1
CONSTRUCTION_TIME = 2
UNLOCK_CONDITION_FROM_LEVEL = 3
UNLOCK_CONDITION_FROM_PREVIOUS_TRACK = 4
UNLOCK_CONDITION_FROM_ENVIRONMENT = 5
UNLOCK_AVAILABLE = 6
PRICE = 7
LEVEL_REQUIRED = 8
DIRECTION_FROM_LEFT_TO_RIGHT = 0
DIRECTION_FROM_RIGHT_TO_LEFT = 1
DIRECTION_FROM_LEFT_TO_RIGHT_SIDE = 2
DIRECTION_FROM_RIGHT_TO_LEFT_SIDE = 3
MAIN_PRIORITY_TRACKS = (((20, 18, 16, 14, 12, 10, 8, 6, 4), (20, 18, 16, 14, 12, 10, 8, 6, 4),
                         (32, 30, 28, 26, 24, 22), (23, 21)),
                        ((19, 17, 15, 13, 11, 9, 7, 5, 3), (19, 17, 15, 13, 11, 9, 7, 5, 3),
                         (24, 22), (31, 29, 27, 25, 23, 21)),
                        ((31, 29, 27, 25, 23, 21), (23, 21), (0,), (31, 29, 27, 25, 23, 21)),
                        ((24, 22), (32, 30, 28, 26, 24, 22), (32, 30, 28, 26, 24, 22), (0,)))
PASS_THROUGH_PRIORITY_TRACKS = ((2, 1), (1, 2))
TRAIN_ID = 0
ARRIVAL_TIME = 1
DIRECTION = 2
NEW_DIRECTION = 3
CARS = 4
STOP_TIME = 5
EXP = 6
MONEY = 7
ENTRY_TRAIN_ROUTE = ('left_entry', 'right_entry', 'left_side_entry', 'right_side_entry')
EXIT_TRAIN_ROUTE = ('right_exit', 'left_exit', 'right_side_exit', 'left_side_exit')
APPROACHING_TRAIN_ROUTE = ('left_approaching', 'right_approaching', 'left_side_approaching', 'right_side_approaching')
MAXIMUM_LEVEL = 100
ENTRY_TRACK = [0, 0, 100, 100]
ARRIVAL_TIME_MIN = 0
ARRIVAL_TIME_MAX = 1
CARS_MIN = 4
CARS_MAX = 5
TRAIN_ACCELERATION_FACTOR = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
# ------------------- END CONSTANTS -------------------


class Model:
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor, logger):
        self.logger = logger
        self.view = None
        self.controller = None
        self.is_activated = False
        self.user_db_connection = user_db_connection
        self.user_db_cursor = user_db_cursor
        self.config_db_cursor = config_db_cursor

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_save_state(self):
        pass
