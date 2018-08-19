TRACKS_READY = 4
SCREEN_RESOLUTION = (1200, 600)
BACKGROUND_IMAGE = 'img/stones-background.jpg'
BACKGROUND_TILE_RESOLUTION = (1200, 1200)
NUMBER_OF_BACKGROUND_TILES = (7, 3)
MAP_RESOLUTION = (BACKGROUND_TILE_RESOLUTION[0] * NUMBER_OF_BACKGROUND_TILES[0],
                  BACKGROUND_TILE_RESOLUTION[1] * NUMBER_OF_BACKGROUND_TILES[1])
BASE_OFFSET_UPPER_LEFT_LIMIT = (SCREEN_RESOLUTION[0] - MAP_RESOLUTION[0],
                                SCREEN_RESOLUTION[1] - MAP_RESOLUTION[1])
BASE_OFFSET_LOWER_RIGHT_LIMIT = (0, 0)
BASE_OFFSET = (BASE_OFFSET_UPPER_LEFT_LIMIT[0] // 2, BASE_OFFSET_UPPER_LEFT_LIMIT[1] // 2)
BOTTOM_BAR_HEIGHT = 50
BOTTOM_BAR_WIDTH = 1000

FRAME_RATE = 60

LEFT_ENTRY_BASE_ROUTE = 'left_entry_base_route'
LEFT_EXIT_BASE_ROUTE = 'left_exit_base_route'
RIGHT_ENTRY_BASE_ROUTE = 'right_entry_base_route'
RIGHT_EXIT_BASE_ROUTE = 'right_exit_base_route'
LEFT_ENTRY_PLATFORM_BASE_ROUTE = 'left_entry_platform_base_route'
RIGHT_ENTRY_PLATFORM_BASE_ROUTE = 'right_entry_platform_base_route'
RIGHT_EXIT_PLATFORM_BASE_ROUTE = 'right_exit_platform_base_route'
LEFT_EXIT_PLATFORM_BASE_ROUTE = 'left_exit_platform_base_route'

LEFT = 0
RIGHT = 1
ENTRY_TRAIN_ROUTE = {LEFT: 'left_entry', RIGHT: 'right_entry'}
EXIT_TRAIN_ROUTE = {LEFT: 'right_exit', RIGHT: 'left_exit'}
APPROACHING_TRAIN_ROUTE = {LEFT: 'left_approaching', RIGHT: 'right_approaching'}

RED_SIGNAL = 'red'
GREEN_SIGNAL = 'green'
SIGNAL_IMAGE_BASE_PATH = 'img/signal_base.png'
SIGNAL_IMAGE_PATH = {RED_SIGNAL: 'img/signal_red.png', GREEN_SIGNAL: 'img/signal_green.png'}

TRAIN_CREATION_TIMEOUT = {LEFT: FRAME_RATE * 10, RIGHT: FRAME_RATE * 0}
TRAIN_CART_IMAGE_PATH = 'img/cart'
TRAIN_ACCELERATION_FACTOR = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7,
                             8, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18,
                             19, 19, 20, 20, 21, 21, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28, 29, 29, 30, 31, 31, 32,
                             33, 34, 34, 35, 36, 37, 37, 38, 39, 40, 41, 41, 42, 43, 44, 45, 46, 47, 47, 48, 49, 50,
                             51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
                             73, 74, 75, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89, 90, 92, 93, 94, 96, 97, 98, 100,
                             101, 103, 104, 105, 107, 108, 110, 111, 113, 114, 116, 117, 119, 120, 122, 124, 125, 127,
                             128, 130, 132, 133, 135, 137, 138, 140, 142, 144, 145, 147, 149, 151, 153, 154, 156, 158,
                             160, 162, 164, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193,
                             195, 198, 200, 202, 204, 206, 209, 211, 213, 215, 218, 220, 222, 225, 227, 230, 232, 235,
                             237, 240, 242, 245, 247, 250, 252, 255, 258, 260, 263, 266, 268, 271, 274, 277, 279, 282,
                             285, 288, 291, 294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330, 334, 337,
                             340, 344, 347, 350, 354, 357, 361, 364, 368, 371, 375, 379, 382, 386, 390, 394, 397, 401,
                             405, 409, 413, 417, 421, 425, 429, 433, 438, 442, 446, 450, 455, 459, 464, 468, 473, 478,
                             482, 487, 492, 497, 502, 507, 512, 517)

TRAIN_ACCELERATION_FACTOR_LENGTH = len(TRAIN_ACCELERATION_FACTOR)
TRAIN_MAXIMUM_SPEED = TRAIN_ACCELERATION_FACTOR[TRAIN_ACCELERATION_FACTOR_LENGTH - 1] - \
                      TRAIN_ACCELERATION_FACTOR[TRAIN_ACCELERATION_FACTOR_LENGTH - 2]
TRAIN_BRAKING_DISTANCE = TRAIN_ACCELERATION_FACTOR[TRAIN_ACCELERATION_FACTOR_LENGTH - 1]

FIRST_PRIORITY_TRACKS = ((TRACKS_READY - (TRACKS_READY % 2), 2, -2), (TRACKS_READY + (TRACKS_READY % 2) - 1, 1, -2))
SECOND_PRIORITY_TRACKS = ((TRACKS_READY + (TRACKS_READY % 2) - 1, 1, -2), (TRACKS_READY - (TRACKS_READY % 2), 2, -2))
PASS_THROUGH_PRIORITY_TRACKS = ((2, 0, -1), (1, 3, 1))

MOVE = 'normal'
ACCELERATE = 'accelerate'
DECELERATE = 'decelerate'
STOP = 'stop'

PASS_THROUGH = 'pass-through'
APPROACHING = 'approaching'
APPROACHING_PASS_THROUGH = 'approaching_pass_through'
PENDING_BOARDING = 'pending_boarding'
BOARDING_IN_PROGRESS = 'boarding_in_progress'
BOARDING_COMPLETE = 'boarding_complete'

LEFT_ENTRY_RAILROAD_SWITCH = 'left_entry_railroad_switch'
LEFT_EXIT_RAILROAD_SWITCH = 'left_exit_railroad_switch'
RIGHT_ENTRY_RAILROAD_SWITCH = 'right_entry_railroad_switch'
RIGHT_EXIT_RAILROAD_SWITCH = 'right_exit_railroad_switch'

LEFT_ENTRY_CROSSOVER = 'left_entry_crossover'
LEFT_EXIT_CROSSOVER = 'left_exit_crossover'
RIGHT_ENTRY_CROSSOVER = 'right_entry_crossover'
RIGHT_EXIT_CROSSOVER = 'right_exit_crossover'

FONT_NAME = 'Arial'
BUTTON_FONT_SIZE = 20
DAY_FONT_SIZE = 18

BUTTON_TEXT_COLOR = (255, 255, 255)
BOTTOM_BAR_COLOR = (0, 0, 0, 191)
DAY_FONT_COLOR = (205, 0, 0)