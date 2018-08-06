import colors

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
base_route_flags = (LEFT_ENTRY_BASE_ROUTE, 'left_exit_base_route', 'right_entry_base_route', 'right_exit_base_route',
                    'left_entry_platform_base_route', 'right_entry_platform_base_route',
                    'right_exit_platform_base_route', 'left_exit_platform_base_route')
train_route_flags = ('left_entry', 'right_exit',
                     'right_entry', 'left_exit',
                     'left_approaching', 'right_approaching', 'boarding')
signal_flags = ('red', 'green')
signal_image_path = ('img/signal_red.png', 'img/signal_green.png')

train_creation_timeout = frame_rate*10
train_cart_image_path = ('img/cart_red.png', 'img/cart_green.png', 'img/cart_blue.png')
train_maximum_speed = 5
train_deceleration_factor = 50
train_acceleration_factor = 8
train_state_flags = ('pass-through', 'approaching',
                     'pending_boarding', 'boarding_in_progress', 'boarding_complete')
left_to_right_direction = 0
right_to_left_direction = 1


text_color = colors.YELLOW1

font_name = 'Arial'
font_size = 20

button_text_color = colors.WHITE,
button_normal_back_color = colors.INDIANRED1
button_hover_back_color = colors.INDIANRED2
button_pressed_back_color = colors.INDIANRED3
