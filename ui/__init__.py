from fractions import Fraction
from typing import Final, final

from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup
from pyglet.gl import glScalef, glTranslatef


@final
class Viewport:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0


@final
class Camera:
    """ A simple 2D camera that contains the speed and offset."""

    def __init__(self, scroll_speed=1, min_zoom=1, max_zoom=4):
        assert min_zoom <= max_zoom, "Minimum zoom must not be greater than maximum zoom"
        self.scroll_speed = scroll_speed
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.offset_x = 0
        self.offset_y = 0
        self._zoom = max(min(1, self.max_zoom), self.min_zoom)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        """ Here we set zoom, clamp value to minimum of min_zoom and max of max_zoom."""
        self._zoom = max(min(value, self.max_zoom), self.min_zoom)

    @property
    def position(self):
        """Query the current offset."""
        return self.offset_x, self.offset_y

    @position.setter
    def position(self, value):
        """Set the scroll offset directly."""
        self.offset_x, self.offset_y = value

    def move(self, axis_x, axis_y):
        """ Move axis direction with scroll_speed.
            Example: Move left -> move(-1, 0)
         """
        self.offset_x += self.scroll_speed * axis_x
        self.offset_y += self.scroll_speed * axis_y

    def begin(self):
        # Set the current camera offset so you can draw your scene.
        # Translate using the zoom and the offset.
        glTranslatef(-self.offset_x * self._zoom, -self.offset_y * self._zoom, 0)

        # Scale by zoom level.
        glScalef(self._zoom, self._zoom, 1)

    def end(self):
        # Since this is a matrix, you will need to reverse the translate after rendering otherwise
        # it will multiply the current offset every draw update pushing it further and further away.

        # Reverse scale, since that was the last transform.
        glScalef(1 / self._zoom, 1 / self._zoom, 1)

        # Reverse translate.
        glTranslatef(self.offset_x * self._zoom, self.offset_y * self._zoom, 0)

    def __enter__(self):
        self.begin()

    def __exit__(self, exception_type, exception_value, traceback):
        self.end()


# --------------------- CONSTANTS ---------------------
MAP_CAMERA = Camera(min_zoom=Fraction(1, 2), max_zoom=Fraction(1, 1))
UI_CAMERA = Camera(min_zoom=1, max_zoom=1)
ZOOM_OUT_SCALE_FACTOR: Final = 0.5                     # how much to scale all sprites when map is zoomed out
ZOOM_IN_SCALE_FACTOR: Final = 1.0                      # how much to scale all sprites when map is zoomed in
MAP_WIDTH: Final = 8192                                # full-size map width
MAP_HEIGHT: Final = 4096                               # full-size map height
MIN_RESOLUTION_WIDTH: Final = 1280                     # minimum screen resolution width supported by the app UI
MIN_RESOLUTION_HEIGHT: Final = 720                     # minimum screen resolution height supported by the app UI
SCHEDULE_ROWS: Final = 12                              # number of schedule rows on schedule screen
SCHEDULE_COLUMNS: Final = 2                            # number of schedule columns on schedule screen
TRACKS: Final = 0                                      # matrix #0 stores tracks state
ENVIRONMENT: Final = 1                                 # matrix #1 stores environment tiers state
CONSTRUCTOR_VIEW_TRACK_CELLS: Final = 4                # number of cells for tracks on constructor screen
CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS: Final = 4          # number of cells for environment tiers on constructor screen
SHOP_DETAILS_BUTTON_NORMAL_SIZE = (250, 40)
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
# colors
ORANGE_RGB: Final = (255, 127, 0)                      # orange UI color
ORANGE_GREY_RGB: Final = (112, 56, 0)
GREEN_RGB: Final = (0, 192, 0)                         # green UI color
GREEN_GREY_RGB: Final = (0, 84, 0)
RED_RGB: Final = (255, 0, 0)                           # red UI color
RED_GREY_RGB: Final = (112, 0, 0)
WHITE_RGB: Final = (255, 255, 255)                     # white UI color
GREY_RGB: Final = (112, 112, 112)                      # grey UI color
# time
FRAMES_IN_ONE_DAY: Final = 345600                      # indicates how many frames fit in one in-game day
FRAMES_IN_ONE_HOUR: Final = 14400                      # indicates how many frames fit in one in-game hour
FRAMES_IN_ONE_MINUTE: Final = 240                      # indicates how many frames fit in one in-game minute
FRAMES_IN_ONE_SECOND: Final = 4                        # indicates how many frames fit in one in-game second
MINUTES_IN_ONE_HOUR: Final = 60
SECONDS_IN_ONE_MINUTE: Final = 60
HOURS_IN_ONE_DAY: Final = 24
SCHEDULE_ARRIVAL_TIME_THRESHOLD: Final = [FRAMES_IN_ONE_HOUR, FRAMES_IN_ONE_HOUR * 10]
# base_schedule matrix properties
TRAIN_ID: Final = 0                                    # property #0 indicates train identification number
ARRIVAL_TIME: Final = 1                                # property #1 indicates arrival time
DIRECTION: Final = 2                                   # property #2 indicates direction
NEW_DIRECTION: Final = 3                               # property #3 indicates new direction
CARS: Final = 4                                        # property #4 indicates number of cars
STOP_TIME: Final = 5                                   # property #5 indicates how much stop time left
EXP: Final = 6                                         # property #6 indicates how much exp the train gives
MONEY: Final = 7                                       # property #7 indicates how much money the train gives
# bonus code matrix properties
CODE_TYPE: Final = 0
BONUS_VALUE: Final = 1
REQUIRED_LEVEL: Final = 2
MAXIMUM_BONUS_TIME: Final = 3
ACTIVATION_AVAILABLE: Final = 4
ACTIVATIONS_LEFT: Final = 5
IS_ACTIVATED: Final = 6
BONUS_TIME: Final = 7
# main surface which harbors all the app
SURFACE: Final = Window(width=MIN_RESOLUTION_WIDTH, height=MIN_RESOLUTION_HEIGHT,
                        caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)
# flip the surface so user knows game has launched and is loading now
SURFACE.flip()
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
HAND_CURSOR: Final = SURFACE.get_system_mouse_cursor(SURFACE.CURSOR_HAND)
DEFAULT_CURSOR: Final = SURFACE.get_system_mouse_cursor(SURFACE.CURSOR_DEFAULT)
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
