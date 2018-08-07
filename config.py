import colors


tracks_ready = 3
screen_resolution = (1200, 600)
background_image = 'img/green-grass-background.jpg'
background_tile_resolution = (1200, 1200)
number_of_background_tiles = (7, 3)
map_resolution = (background_tile_resolution[0] * number_of_background_tiles[0],
                  background_tile_resolution[1] * number_of_background_tiles[1])
base_offset_upper_left_limit = (screen_resolution[0] - map_resolution[0],
                                screen_resolution[1] - map_resolution[1])
base_offset_lower_right_limit = (0, 0)
base_offset = (base_offset_upper_left_limit[0] // 2, base_offset_upper_left_limit[1] // 2)
bottom_bar_height = 50

frame_rate = 60

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
signal_image_path = {RED_SIGNAL: 'img/signal_red.png', GREEN_SIGNAL: 'img/signal_green.png'}

train_creation_timeout = {LEFT: frame_rate*30, RIGHT: frame_rate*0}
train_cart_image_path = ('img/cart_red.png', 'img/cart_green.png', 'img/cart_blue.png')
train_acceleration_factor = (0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7,
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

train_acceleration_factor_length = len(train_acceleration_factor)
train_maximum_speed = train_acceleration_factor[train_acceleration_factor_length - 1] - \
                      train_acceleration_factor[train_acceleration_factor_length - 2]
train_braking_distance = train_acceleration_factor[train_acceleration_factor_length - 1]

first_priority_tracks = ((tracks_ready - (tracks_ready % 2), 0, -2), (tracks_ready + (tracks_ready % 2) - 1, 0, -2))
second_priority_tracks = ((tracks_ready + (tracks_ready % 2) - 1, 0, -2), (tracks_ready - (tracks_ready % 2), 0, -2))

MOVE = 'normal'
ACCELERATE = 'accelerate'
DECELERATE = 'decelerate'
STOP = 'stop'

PASS_THROUGH = 'pass-through'
APPROACHING = 'approaching'
PENDING_BOARDING = 'pending_boarding'
BOARDING_IN_PROGRESS = 'boarding_in_progress'
BOARDING_COMPLETE = 'boarding_complete'

# keys below are not used at the moment

text_color = colors.YELLOW1

font_name = 'Arial'
font_size = 20

button_text_color = colors.WHITE,
button_normal_back_color = colors.INDIANRED1
button_hover_back_color = colors.INDIANRED2
button_pressed_back_color = colors.INDIANRED3
