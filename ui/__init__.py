from ctypes import windll

from pyglet.window.win32 import Win32Window
from pyglet.graphics import Batch, OrderedGroup

from database import *
from camera.map_camera import MapCamera
from camera.ui_camera import UICamera


def window_size_has_changed(fn):
    def _update_sprites_if_window_size_has_changed(*args, **kwargs):
        if args[1:] != args[0].screen_resolution:
            fn(*args, **kwargs)

    return _update_sprites_if_window_size_has_changed


class Window(Win32Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.on_mouse_scroll_handlers = []
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.on_window_resize_handlers = []
        self.on_window_activate_handlers = []
        self.on_window_show_handlers = []
        self.on_window_deactivate_handlers = []
        self.on_window_hide_handlers = []
        self.on_mouse_motion_event_counter = 0
        self.on_mouse_motion_cached_movement = [0, 0]
        self.on_mouse_drag_event_counter = 0
        self.on_mouse_drag_cached_movement = [0, 0]
        self.on_mouse_scroll_event_counter = 0
        self.on_mouse_scroll_cached_movement = [0, 0]
        self.fullscreen_resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = USER_DB_CURSOR.fetchone()


def _create_window():
    Window.register_event_type('on_fullscreen')
    Window.register_event_type('on_restore')
    CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
    screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
    monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
    if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
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
MAP_ZOOM_STEP = 0.5
MAP_WIDTH: Final = 8192                                # full-size map width
MAP_HEIGHT: Final = 4096                               # full-size map height
MIN_RESOLUTION_WIDTH: Final = 1280                     # minimum screen resolution width supported by the app UI
MIN_RESOLUTION_HEIGHT: Final = 720                     # minimum screen resolution height supported by the app UI
SCHEDULE_ROWS: Final = 12                              # number of schedule rows on schedule screen
SCHEDULE_COLUMNS: Final = 2                            # number of schedule columns on schedule screen
SHOP_DETAILS_BUTTON_NORMAL_SIZE = (250, 40)
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
# ------------------- END CONSTANTS -------------------


def get_top_bar_height(screen_resolution):
    return int(72 / 1280 * screen_resolution[0]) // 2


def get_bottom_bar_height(screen_resolution):
    return int(72 / 1280 * screen_resolution[0])


def get_inner_area_rect(screen_resolution):
    bottom_bar_height = get_bottom_bar_height(screen_resolution)
    inner_area_size = ((int(6.875 * bottom_bar_height) * 2 + bottom_bar_height // 4,
                        19 * bottom_bar_height // 4))
    inner_area_position = ((screen_resolution[0] - inner_area_size[0]) // 2,
                           (screen_resolution[1] - inner_area_size[1] - 3 * bottom_bar_height // 2) // 2
                           + bottom_bar_height)
    return *inner_area_position, *inner_area_size


def get_mini_map_position(screen_resolution):
    return (screen_resolution[0] - get_mini_map_width(screen_resolution) - 8,
            screen_resolution[1] - get_top_bar_height(screen_resolution) - 6 - get_mini_map_height(screen_resolution))


def get_mini_map_width(screen_resolution):
    return screen_resolution[0] // 4


def get_mini_map_height(screen_resolution):
    return round(get_mini_map_width(screen_resolution) / 2)


@final
class Viewport:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
