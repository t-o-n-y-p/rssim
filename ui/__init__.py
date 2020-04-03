from ctypes import windll

from pyglet import resource
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup

from database import *
from camera.map_camera import MapCamera
from camera.ui_camera import UICamera
from midi_player import MIDIPlayer
from speaker import Speaker


def window_size_has_changed(fn):
    def _update_sprites_if_window_size_has_changed(*args, **kwargs):
        if args[1:] != args[0].screen_resolution:
            fn(*args, **kwargs)

    return _update_sprites_if_window_size_has_changed


def _create_window():
    CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
    screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
    monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
    if USER_DB_CURSOR.fetchone()[0] and monitor_resolution_config in screen_resolution_config:
        window = Window(width=monitor_resolution_config[0], height=monitor_resolution_config[1],
                        caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)
        window.set_fullscreen(True)
        return window

    USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
    screen_resolution = USER_DB_CURSOR.fetchone()
    return Window(width=screen_resolution[0], height=screen_resolution[1],
                  caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)


# --------------------- CONSTANTS ---------------------
MAP_CAMERA: Final = MapCamera()
UI_CAMERA: Final = UICamera()
MIDI_PLAYER: Final = MIDIPlayer()
SPEAKER: Final = Speaker()
MAP_ZOOM_STEP: Final = 0.5
MAP_WIDTH: Final = 8192                                # full-size map width
MAP_HEIGHT: Final = 4096                               # full-size map height
MIN_RESOLUTION_WIDTH: Final = 1280                     # minimum screen resolution width supported by the app UI
MIN_RESOLUTION_HEIGHT: Final = 720                     # minimum screen resolution height supported by the app UI
SCHEDULE_ROWS: Final = 12                              # number of schedule rows on schedule screen
SCHEDULE_COLUMNS: Final = 2                            # number of schedule columns on schedule screen
SHOP_DETAILS_BUTTON_NORMAL_SIZE: Final = (250, 40)
# colors
YELLOW_RGB: Final = (255, 255, 96)                     # yellow UI color
YELLOW_GREY_RGB: Final = (112, 112, 42)
ORANGE_RGB: Final = (255, 127, 0)                      # orange UI color
ORANGE_GREY_RGB: Final = (112, 56, 0)
GREEN_RGB: Final = (0, 192, 0)                         # green UI color
GREEN_GREY_RGB: Final = (0, 84, 0)
RED_RGB: Final = (255, 0, 0)                           # red UI color
RED_GREY_RGB: Final = (112, 0, 0)
WHITE_RGB: Final = (255, 255, 255)                     # white UI color
GREY_RGB: Final = (112, 112, 112)                      # grey UI color
SCHEDULE_ARRIVAL_TIME_THRESHOLD: Final = [SECONDS_IN_ONE_HOUR, SECONDS_IN_ONE_HOUR * 10]
# main surface which harbors all the app
WINDOW: Final = _create_window()
# flip the surface so user knows game has launched and is loading now
WINDOW.flip()
# large portions of sprites which can be drawn together
BATCHES: Final = {'main_batch': Batch(),
                  'mini_map_batch': Batch(),
                  'main_frame': Batch(),
                  'ui_batch': Batch()}
# groups are layers of OpenGL scene
GROUPS: Final = {'environment': OrderedGroup(0),
                 'main_map': OrderedGroup(1),
                 'signal': OrderedGroup(2),
                 'train': OrderedGroup(2),
                 'environment_2': OrderedGroup(3),
                 'twilight': OrderedGroup(4),
                 'mini_environment': OrderedGroup(5),
                 'mini_map': OrderedGroup(6),
                 'mini_environment_2': OrderedGroup(7),
                 'main_frame': OrderedGroup(8),
                 'button_background': OrderedGroup(9),
                 'exp_money_time': OrderedGroup(9),
                 'button_text': OrderedGroup(10)}
# mouse cursor shapes
HAND_CURSOR: Final = WINDOW.get_system_mouse_cursor(WINDOW.CURSOR_HAND)
DEFAULT_CURSOR: Final = WINDOW.get_system_mouse_cursor(WINDOW.CURSOR_DEFAULT)

_car_collections_implemented = [12, 10]
MAXIMUM_CAR_COLLECTIONS: Final = [12, 6]
resource.path = ['font', 'img', 'img/textures.zip']
resource.reindex()
_cars_texture = resource.texture('cars_in_one.dds')
resource.add_font('perfo-bold.ttf')

# CAR_HEAD_IMAGE includes all textures for leading carriage
PASSENGER_CAR_HEAD_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_CAR_HEAD_IMAGE.append([])
    for j in range(4):
        PASSENGER_CAR_HEAD_IMAGE[i].append(_cars_texture.get_region((j % 2) * 251, i * 47 + 3, 251, 41))

FREIGHT_CAR_HEAD_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_CAR_HEAD_IMAGE.append([])
    FREIGHT_CAR_HEAD_IMAGE[i].append(_cars_texture.get_region(6 * 251, i * 94 + 3, 251, 41))
    for j in range(1, 6):
        FREIGHT_CAR_HEAD_IMAGE[i].append(_cars_texture.get_region(6 * 251, i * 94 + 50, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_HEAD_IMAGE)):
    for j in range(4):
        PASSENGER_CAR_HEAD_IMAGE[i][j].anchor_x = PASSENGER_CAR_HEAD_IMAGE[i][j].width // 2
        PASSENGER_CAR_HEAD_IMAGE[i][j].anchor_y = PASSENGER_CAR_HEAD_IMAGE[i][j].height // 2

for i in range(len(FREIGHT_CAR_HEAD_IMAGE)):
    for j in range(6):
        FREIGHT_CAR_HEAD_IMAGE[i][j].anchor_x = FREIGHT_CAR_HEAD_IMAGE[i][j].width // 2
        FREIGHT_CAR_HEAD_IMAGE[i][j].anchor_y = FREIGHT_CAR_HEAD_IMAGE[i][j].height // 2

# CAR_MID_IMAGE includes all textures for middle carriage
PASSENGER_CAR_MID_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_CAR_MID_IMAGE.append(_cars_texture.get_region(2 * 251, i * 47 + 3, 251, 41))

FREIGHT_CAR_MID_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_CAR_MID_IMAGE.append(_cars_texture.get_region(6 * 251, 20 * 47 + 3, 151, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_MID_IMAGE)):
    PASSENGER_CAR_MID_IMAGE[i].anchor_x = PASSENGER_CAR_MID_IMAGE[i].width // 2
    PASSENGER_CAR_MID_IMAGE[i].anchor_y = PASSENGER_CAR_MID_IMAGE[i].height // 2

for i in range(len(FREIGHT_CAR_MID_IMAGE)):
    FREIGHT_CAR_MID_IMAGE[i].anchor_x = FREIGHT_CAR_MID_IMAGE[i].width // 2
    FREIGHT_CAR_MID_IMAGE[i].anchor_y = FREIGHT_CAR_MID_IMAGE[i].height // 2

# CAR_TAIL_IMAGE includes all textures for trailing carriage
PASSENGER_CAR_TAIL_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_CAR_TAIL_IMAGE.append([])
    for j in range(4):
        PASSENGER_CAR_TAIL_IMAGE[i].append(_cars_texture.get_region((j % 2 + 3) * 251, i * 47 + 3, 251, 41))

FREIGHT_CAR_TAIL_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_CAR_TAIL_IMAGE.append([])
    FREIGHT_CAR_TAIL_IMAGE[i].append(_cars_texture.get_region(7 * 251, i * 94 + 3, 251, 41))
    for j in range(1, 6):
        FREIGHT_CAR_TAIL_IMAGE[i].append(_cars_texture.get_region(7 * 251, i * 94 + 50, 251, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_TAIL_IMAGE)):
    for j in range(4):
        PASSENGER_CAR_TAIL_IMAGE[i][j].anchor_x = PASSENGER_CAR_TAIL_IMAGE[i][j].width // 2
        PASSENGER_CAR_TAIL_IMAGE[i][j].anchor_y = PASSENGER_CAR_TAIL_IMAGE[i][j].height // 2

for i in range(len(FREIGHT_CAR_TAIL_IMAGE)):
    for j in range(6):
        FREIGHT_CAR_TAIL_IMAGE[i][j].anchor_x = FREIGHT_CAR_TAIL_IMAGE[i][j].width // 2
        FREIGHT_CAR_TAIL_IMAGE[i][j].anchor_y = FREIGHT_CAR_TAIL_IMAGE[i][j].height // 2

# BOARDING_LIGHT_IMAGE includes all textures for boarding lights - they are enabled if boarding is in progress
PASSENGER_BOARDING_LIGHT_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_BOARDING_LIGHT_IMAGE.append(_cars_texture.get_region(5 * 251, i * 47 + 3, 251, 41))

FREIGHT_BOARDING_LIGHT_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_BOARDING_LIGHT_IMAGE.append(_cars_texture.get_region(6 * 251, 20 * 47 + 3, 151, 41))

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_BOARDING_LIGHT_IMAGE)):
    PASSENGER_BOARDING_LIGHT_IMAGE[i].anchor_x = PASSENGER_BOARDING_LIGHT_IMAGE[i].width // 2
    PASSENGER_BOARDING_LIGHT_IMAGE[i].anchor_y = PASSENGER_BOARDING_LIGHT_IMAGE[i].height // 2

for i in range(len(FREIGHT_BOARDING_LIGHT_IMAGE)):
    FREIGHT_BOARDING_LIGHT_IMAGE[i].anchor_x = FREIGHT_BOARDING_LIGHT_IMAGE[i].width // 2
    FREIGHT_BOARDING_LIGHT_IMAGE[i].anchor_y = FREIGHT_BOARDING_LIGHT_IMAGE[i].height // 2

# signal images
GREEN_SIGNAL: Final = 'green_signal'
RED_SIGNAL: Final = 'red_signal'
RED_SIGNAL_IMAGE: Final = resource.texture('signals.dds').get_region(0, 0, 7, 9)
GREEN_SIGNAL_IMAGE: Final = resource.texture('signals.dds').get_region(8, 0, 7, 9)
# anchor is set to the middle point
RED_SIGNAL_IMAGE.anchor_x = 3
RED_SIGNAL_IMAGE.anchor_y = 4
GREEN_SIGNAL_IMAGE.anchor_x = 3
GREEN_SIGNAL_IMAGE.anchor_y = 4

# textures for localization buttons in the top left corner
_flags = resource.texture('flags.dds')
FLAG_US: Final = _flags.get_region(0, 0, 128, 128)
FLAG_RU: Final = _flags.get_region(128, 0, 128, 128)
FLAG_US.anchor_x = FLAG_US.width // 2
FLAG_US.anchor_y = FLAG_US.height // 2
FLAG_RU.anchor_x = FLAG_RU.width // 2
FLAG_RU.anchor_y = FLAG_RU.height // 2

# textures for switches in crossovers in straight and diverging state
SWITCHES_STRAIGHT: Final = resource.texture('switches_straight.dds')
SWITCHES_DIVERGING: Final = resource.texture('switches_diverging.dds')
# ------------------- END CONSTANTS -------------------


def get_top_bar_height(screen_resolution):
    return int(72 / 1280 * screen_resolution[0]) // 2


def get_bottom_bar_height(screen_resolution):
    return int(72 / 1280 * screen_resolution[0])


def get_inner_area_rect(screen_resolution):
    bottom_bar_height = get_bottom_bar_height(screen_resolution)
    inner_area_size = (
        (int(6.875 * bottom_bar_height) * 2 + bottom_bar_height // 4,
        19 * bottom_bar_height // 4)
    )
    inner_area_position = (
        (screen_resolution[0] - inner_area_size[0]) // 2,
        (screen_resolution[1] - inner_area_size[1] - 3 * bottom_bar_height // 2) // 2 + bottom_bar_height
    )
    return *inner_area_position, *inner_area_size


def get_mini_map_position(screen_resolution):
    return (
        screen_resolution[0] - get_mini_map_width(screen_resolution) - 8,
        screen_resolution[1] - get_top_bar_height(screen_resolution) - 6 - get_mini_map_height(screen_resolution)
    )


def get_mini_map_width(screen_resolution):
    return screen_resolution[0] // 4


def get_mini_map_height(screen_resolution):
    return round(get_mini_map_width(screen_resolution) / 2)


def get_map_tracks(map_id, tracks):
    return resource.texture(f'tracks_m{map_id}t{tracks}.dds')


def get_map_environment_primary(map_id, tiers):
    return resource.texture(f'primary_m{map_id}e{tiers}.dds')


@final
class Viewport:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
