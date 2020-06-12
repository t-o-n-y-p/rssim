from abc import ABC
from ctypes import windll
from inspect import getfullargspec
from typing import Final, final

from pyglet import resource
from pyglet.window import Window
from pyglet.graphics import Batch, OrderedGroup

from camera.map_camera import MapCamera
from camera.ui_camera import UICamera
from database import CONFIG_DB_CURSOR, USER_DB_CURSOR, SECONDS_IN_ONE_HOUR
from i18n import I18N_RESOURCES
from midi_player import MIDIPlayer
from speaker import Speaker
from ui.fade_animation_v2.fade_in_animation_v2 import FadeInAnimationV2
from ui.fade_animation_v2.fade_out_animation_v2 import FadeOutAnimationV2


def _to_snake_case(string):
    return ''.join('_' + c.lower() if c.isupper() else c for c in string).lstrip('_')\
        .replace('f_p_s_', 'fps_').replace('r_u_', 'ru_').replace('e_n_', 'en_').replace('u_s_', 'us_')\
        .replace('12_h_', '_12h_').replace('24_h_', '_24h_')


def _create_button(cls, parent_object):
    button_name_snake_case = _to_snake_case(cls.__name__)
    on_click_action_method_name = 'on_click_action_' + button_name_snake_case
    on_hover_action_method_name = 'on_hover_action_' + button_name_snake_case
    on_leave_action_method_name = 'on_leave_action_' + button_name_snake_case
    parent_object.__setattr__(
        button_name_snake_case,
        cls(
            logger=parent_object.logger.getChild(button_name_snake_case),
            parent_viewport=parent_object.parent_viewport,
            on_click_action=parent_object.__getattribute__(on_click_action_method_name),
            on_hover_action=parent_object.__getattribute__(on_hover_action_method_name)
            if hasattr(parent_object, on_hover_action_method_name) else None,
            on_leave_action=parent_object.__getattribute__(on_leave_action_method_name)
            if hasattr(parent_object, on_leave_action_method_name) else None
        )
    )
    button_object = parent_object.__getattribute__(button_name_snake_case)
    parent_object.ui_objects.append(button_object)
    parent_object.buttons.append(button_object)
    parent_object.fade_out_animation.child_animations.append(button_object.fade_out_animation)
    parent_object.on_mouse_press_handlers.extend(button_object.on_mouse_press_handlers)
    parent_object.on_mouse_release_handlers.extend(button_object.on_mouse_release_handlers)
    parent_object.on_mouse_motion_handlers.extend(button_object.on_mouse_motion_handlers)
    parent_object.on_mouse_leave_handlers.extend(button_object.on_mouse_leave_handlers)
    parent_object.on_window_resize_handlers.extend(button_object.on_window_resize_handlers)
    return button_object


def _create_knob(cls, parent_object):
    knob_name_snake_case = _to_snake_case(cls.__name__)
    on_value_update_action_method_name = 'on_value_update_action_' + knob_name_snake_case
    parent_object.__setattr__(
        knob_name_snake_case,
        cls(
            logger=parent_object.logger.getChild(knob_name_snake_case),
            parent_viewport=parent_object.parent_viewport,
            on_value_update_action=parent_object.__getattribute__(on_value_update_action_method_name)
        )
    )
    knob_object = parent_object.__getattribute__(knob_name_snake_case)
    parent_object.ui_objects.append(knob_object)
    parent_object.fade_out_animation.child_animations.append(knob_object.fade_out_animation)
    parent_object.on_mouse_press_handlers.extend(knob_object.on_mouse_press_handlers)
    parent_object.on_mouse_release_handlers.extend(knob_object.on_mouse_release_handlers)
    parent_object.on_mouse_motion_handlers.extend(knob_object.on_mouse_motion_handlers)
    parent_object.on_mouse_leave_handlers.extend(knob_object.on_mouse_leave_handlers)
    parent_object.on_mouse_drag_handlers.extend(knob_object.on_mouse_drag_handlers)
    parent_object.on_window_resize_handlers.extend(knob_object.on_window_resize_handlers)
    return knob_object


def _create_object(cls, parent_object):
    object_name_snake_case = _to_snake_case(cls.__name__)
    cls_resource_keys = getfullargspec(cls).args[3:]
    parent_object.__setattr__(
        object_name_snake_case,
        cls(
            parent_object.logger.getChild(object_name_snake_case), parent_object.viewport,
            *(parent_object.__getattribute__(a) for a in cls_resource_keys)
        )
    )
    new_object = parent_object.__getattribute__(object_name_snake_case)
    parent_object.ui_objects.append(new_object)
    parent_object.buttons.extend(new_object.buttons)
    parent_object.fade_out_animation.child_animations.append(new_object.fade_out_animation)
    parent_object.on_mouse_press_handlers.extend(new_object.on_mouse_press_handlers)
    parent_object.on_mouse_release_handlers.extend(new_object.on_mouse_release_handlers)
    parent_object.on_mouse_motion_handlers.extend(new_object.on_mouse_motion_handlers)
    parent_object.on_mouse_drag_handlers.extend(new_object.on_mouse_drag_handlers)
    parent_object.on_mouse_leave_handlers.extend(new_object.on_mouse_leave_handlers)
    parent_object.on_mouse_scroll_handlers.extend(new_object.on_mouse_scroll_handlers)
    parent_object.on_key_press_handlers.extend(new_object.on_key_press_handlers)
    parent_object.on_text_handlers.extend(new_object.on_text_handlers)
    parent_object.on_window_resize_handlers.extend(new_object.on_window_resize_handlers)
    parent_object.on_window_activate_handlers.extend(new_object.on_window_activate_handlers)
    parent_object.on_window_show_handlers.extend(new_object.on_window_show_handlers)
    parent_object.on_window_deactivate_handlers.extend(new_object.on_window_deactivate_handlers)
    parent_object.on_window_hide_handlers.extend(new_object.on_window_hide_handlers)
    return new_object


def default_object(cls):
    def _default_object(f):
        def _add_default_object(*args, **kwargs):
            f(*args, **kwargs)
            if cls.__name__.find('Button') > 0:
                new_object = _create_button(cls, args[0])
            elif cls.__name__.find('Knob') > 0:
                new_object = _create_knob(cls, args[0])
            else:
                new_object = _create_object(cls, args[0])

            args[0].fade_in_animation.child_animations.append(new_object.fade_in_animation)

        return _add_default_object

    return _default_object


def optional_object(cls):
    def _optional_object(f):
        def _add_optional_object(*args, **kwargs):
            f(*args, **kwargs)
            if cls.__name__.find('Button') > 0:
                _create_button(cls, args[0])
            elif cls.__name__.find('Knob') > 0:
                _create_knob(cls, args[0])
            else:
                _create_object(cls, args[0])

        return _add_optional_object

    return _optional_object


def double_object(cls1, cls2):
    def _double_object(f):
        def _add_double_object(*args, **kwargs):
            f(*args, **kwargs)
            if cls1.__name__.find('Button') > 0 and cls2.__name__.find('Button') > 0:
                new_object_1 = _create_button(cls1, args[0])
                new_object_2 = _create_button(cls2, args[0])
                new_object_1.paired_object = new_object_2
                new_object_2.paired_object = new_object_1

        return _add_double_object

    return _double_object


def window_size_has_changed(f):
    def _update_if_window_size_has_changed(*args, **kwargs):
        if args[1:3] != args[0].screen_resolution:
            f(*args, **kwargs)

    return _update_if_window_size_has_changed


def localizable(f):
    def _make_an_instance_localizable(*args, **kwargs):
        def on_update_current_locale(new_locale):
            args[0].current_locale = new_locale
            for o in [o for o in args[0].ui_objects if hasattr(o, 'current_locale')]:
                o.on_update_current_locale(new_locale)

        def on_update_current_locale_label(new_locale):
            args[0].current_locale = new_locale
            if args[0].text_label:
                args[0].text_label.text = args[0].get_formatted_text()

        f(*args, **kwargs)
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        args[0].current_locale = USER_DB_CURSOR.fetchone()[0]
        if hasattr(args[0], 'text_label'):
            args[0].on_update_current_locale = on_update_current_locale_label
        else:
            args[0].on_update_current_locale = on_update_current_locale

    return _make_an_instance_localizable


def localizable_with_resource(i18n_key):
    def _localizable_with_resource(f):
        def _make_an_instance_localizable(*args, **kwargs):
            def on_update_current_locale(new_locale):
                args[0].current_locale = new_locale
                if args[0].text_label:
                    args[0].text_label.text = args[0].get_formatted_text()

            def get_formatted_text():
                return I18N_RESOURCES[args[0].i18n_key][args[0].current_locale].format(*args[0].arguments)

            def get_complicated_formatted_text():
                base_resource = I18N_RESOURCES[args[0].i18n_key][args[0].current_locale]
                for k in args[0].resource_list_keys:
                    base_resource = base_resource[k]

                return base_resource.format(*args[0].arguments)

            f(*args, **kwargs)
            USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
            args[0].current_locale = USER_DB_CURSOR.fetchone()[0]
            args[0].on_update_current_locale = on_update_current_locale
            args[0].i18n_key = i18n_key
            if hasattr(args[0], 'resource_list_keys') and len(args[0].resource_list_keys) > 0:
                args[0].get_formatted_text = get_complicated_formatted_text
            else:
                args[0].get_formatted_text = get_formatted_text

        return _make_an_instance_localizable

    return _localizable_with_resource


def is_active(f):
    def _check_if_an_object_is_active(*args, **kwargs):
        if args[0].is_activated:
            f(*args, **kwargs)

    return _check_if_an_object_is_active


def is_not_active(f):
    def _check_if_an_object_is_not_active(*args, **kwargs):
        if not args[0].is_activated:
            f(*args, **kwargs)

    return _check_if_an_object_is_not_active


def _create_window():
    CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
    screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
    monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
    if USER_DB_CURSOR.fetchone()[0] and monitor_resolution_config in screen_resolution_config:
        window = Window(
            width=monitor_resolution_config[0], height=monitor_resolution_config[1],
            caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False
        )
        window.set_fullscreen(True)
        return window

    USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
    screen_resolution = USER_DB_CURSOR.fetchone()
    return Window(
        width=screen_resolution[0], height=screen_resolution[1],
        caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False
    )


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

WINDOW: Final = _create_window()
WINDOW.flip()
# large portions of sprites which can be drawn together
BATCHES: Final = {
    'main_batch': Batch(),
    'mini_map_batch': Batch(),
    'main_frame': Batch(),
    'ui_batch': Batch()
}
# groups are layers of OpenGL scene
GROUPS: Final = {
    'environment': OrderedGroup(0),
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
    'button_text': OrderedGroup(10)
}
# mouse cursor shapes
HAND_CURSOR: Final = WINDOW.get_system_mouse_cursor(WINDOW.CURSOR_HAND)
DEFAULT_CURSOR: Final = WINDOW.get_system_mouse_cursor(WINDOW.CURSOR_DEFAULT)
# button states
HOVER: Final = 'hover'
PRESSED: Final = 'pressed'
NORMAL: Final = 'normal'

_car_collections_implemented = [20, 10]
MAXIMUM_CAR_COLLECTIONS: Final = [20, 10]
resource.path = ['font', 'img', 'img/textures.zip']
resource.reindex()
_atlas = resource.texture('atlas.dds')
resource.add_font('perfo-bold.ttf')

# CAR_HEAD_IMAGE includes all textures for leading carriage
PASSENGER_CAR_HEAD_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_CAR_HEAD_IMAGE.append([])
    for j in range(4):
        PASSENGER_CAR_HEAD_IMAGE[i].append(_atlas.get_region((j % 2) * 251, 3072 + i * 47 + 3, 251, 41))

FREIGHT_CAR_HEAD_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_CAR_HEAD_IMAGE.append([])
    for j in range(10):
        FREIGHT_CAR_HEAD_IMAGE[i].append(_atlas.get_region(6 * 251, 3072 + i * 94 + 3 + 47 * (j % 2), 251, 41))

CAR_HEAD_IMAGE: Final = [PASSENGER_CAR_HEAD_IMAGE, FREIGHT_CAR_HEAD_IMAGE]

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_HEAD_IMAGE)):
    for j in range(4):
        PASSENGER_CAR_HEAD_IMAGE[i][j].anchor_x = PASSENGER_CAR_HEAD_IMAGE[i][j].width // 2
        PASSENGER_CAR_HEAD_IMAGE[i][j].anchor_y = PASSENGER_CAR_HEAD_IMAGE[i][j].height // 2

for i in range(len(FREIGHT_CAR_HEAD_IMAGE)):
    for j in range(10):
        FREIGHT_CAR_HEAD_IMAGE[i][j].anchor_x = FREIGHT_CAR_HEAD_IMAGE[i][j].width // 2
        FREIGHT_CAR_HEAD_IMAGE[i][j].anchor_y = FREIGHT_CAR_HEAD_IMAGE[i][j].height // 2

# CAR_MID_IMAGE includes all textures for middle carriage
PASSENGER_CAR_MID_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_CAR_MID_IMAGE.append(_atlas.get_region(2 * 251, 3072 + i * 47 + 3, 251, 41))

FREIGHT_CAR_MID_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_CAR_MID_IMAGE.append(_atlas.get_region(6 * 251, 3072 + 20 * 47 + 3, 151, 41))

CAR_MID_IMAGE: Final = [PASSENGER_CAR_MID_IMAGE, FREIGHT_CAR_MID_IMAGE]

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
        PASSENGER_CAR_TAIL_IMAGE[i].append(_atlas.get_region((j % 2 + 3) * 251, 3072 + i * 47 + 3, 251, 41))

FREIGHT_CAR_TAIL_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_CAR_TAIL_IMAGE.append([])
    for j in range(10):
        FREIGHT_CAR_TAIL_IMAGE[i].append(_atlas.get_region(7 * 251, 3072 + i * 94 + 3 + 47 * (j % 2), 251, 41))

CAR_TAIL_IMAGE: Final = [PASSENGER_CAR_TAIL_IMAGE, FREIGHT_CAR_TAIL_IMAGE]

# anchor is set to the carriage middle point
for i in range(len(PASSENGER_CAR_TAIL_IMAGE)):
    for j in range(4):
        PASSENGER_CAR_TAIL_IMAGE[i][j].anchor_x = PASSENGER_CAR_TAIL_IMAGE[i][j].width // 2
        PASSENGER_CAR_TAIL_IMAGE[i][j].anchor_y = PASSENGER_CAR_TAIL_IMAGE[i][j].height // 2

for i in range(len(FREIGHT_CAR_TAIL_IMAGE)):
    for j in range(10):
        FREIGHT_CAR_TAIL_IMAGE[i][j].anchor_x = FREIGHT_CAR_TAIL_IMAGE[i][j].width // 2
        FREIGHT_CAR_TAIL_IMAGE[i][j].anchor_y = FREIGHT_CAR_TAIL_IMAGE[i][j].height // 2

# BOARDING_LIGHT_IMAGE includes all textures for boarding lights - they are enabled if boarding is in progress
PASSENGER_BOARDING_LIGHT_IMAGE: Final = []
for i in range(_car_collections_implemented[0]):
    PASSENGER_BOARDING_LIGHT_IMAGE.append(_atlas.get_region(5 * 251, 3072 + i * 47 + 3, 251, 41))

FREIGHT_BOARDING_LIGHT_IMAGE: Final = []
for i in range(_car_collections_implemented[1]):
    FREIGHT_BOARDING_LIGHT_IMAGE.append(_atlas.get_region(6 * 251, 3072 + 20 * 47 + 3, 151, 41))

BOARDING_LIGHT_IMAGE: Final = [PASSENGER_BOARDING_LIGHT_IMAGE, FREIGHT_BOARDING_LIGHT_IMAGE]

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
WHITE_SIGNAL: Final = 'white_signal'
GREEN_SIGNAL_IMAGE: Final = _atlas.get_region(3, 4084, 7, 9)
RED_SIGNAL_IMAGE: Final = _atlas.get_region(16, 4084, 7, 9)
WHITE_SIGNAL_IMAGE: Final = _atlas.get_region(29, 4084, 7, 9)
# anchor is set to the middle point
GREEN_SIGNAL_IMAGE.anchor_x = 3
GREEN_SIGNAL_IMAGE.anchor_y = 4
RED_SIGNAL_IMAGE.anchor_x = 3
RED_SIGNAL_IMAGE.anchor_y = 4
WHITE_SIGNAL_IMAGE.anchor_x = 3
WHITE_SIGNAL_IMAGE.anchor_y = 4

# textures for localization buttons in the top left corner
FLAG_US: Final = _atlas.get_region(3840, 3968, 128, 128)
FLAG_RU: Final = _atlas.get_region(3968, 3968, 128, 128)
FLAG_US.anchor_x = FLAG_US.width // 2
FLAG_US.anchor_y = FLAG_US.height // 2
FLAG_RU.anchor_x = FLAG_RU.width // 2
FLAG_RU.anchor_y = FLAG_RU.height // 2

# textures for switches in crossovers in straight and diverging state
SWITCHES_STRAIGHT: Final = _atlas.get_region(0, 0, 4096, 512)
SWITCHES_DIVERGING: Final = _atlas.get_region(0, 1536, 4096, 512)
# ------------------- END CONSTANTS -------------------


def get_top_bar_height(screen_resolution):
    return int(72 / 1280 * screen_resolution[0]) // 2


def get_bottom_bar_height(screen_resolution):
    return int(72 / 1280 * screen_resolution[0])


def get_inner_area_rect(screen_resolution):
    bottom_bar_height = get_bottom_bar_height(screen_resolution)
    inner_area_size = (
        (
            int(6.875 * bottom_bar_height) * 2 + bottom_bar_height // 4,
            19 * bottom_bar_height // 4
        )
    )
    inner_area_position = (
        (screen_resolution[0] - inner_area_size[0]) // 2,
        (screen_resolution[1] - inner_area_size[1] - 3 * bottom_bar_height // 2) // 2 + bottom_bar_height
    )
    return *inner_area_position, *inner_area_size


def get_mini_map_x(screen_resolution):
    return screen_resolution[0] - get_mini_map_width(screen_resolution) - 8


def get_mini_map_y(screen_resolution):
    return screen_resolution[1] - get_top_bar_height(screen_resolution) - 6 - get_mini_map_height(screen_resolution)


def get_mini_map_width(screen_resolution):
    return screen_resolution[0] // 4


def get_mini_map_height(screen_resolution):
    return round(get_mini_map_width(screen_resolution) / 2)


def get_map_tracks(map_id, tracks):
    return resource.texture(f'tracks_m{map_id}t{tracks}.dds')


def get_map_environment_primary(map_id, tiers):
    return resource.texture(f'primary_m{map_id}e{tiers}.dds')


def get_map_environment_secondary(map_id, tracks, tiers):
    return resource.texture(f'secondary_m{map_id}t{tracks}e{tiers}.dds')


@final
class Viewport:
    def __init__(self):
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0


class UIObject(ABC):
    def __init__(self, logger, parent_viewport=None):
        self.logger = logger
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.screen_resolution = (0, 0)
        self.is_activated = False
        self.opacity = 0
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.on_mouse_scroll_handlers = []
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.on_window_resize_handlers = [self.on_window_resize]
        self.on_window_activate_handlers = []
        self.on_window_show_handlers = []
        self.on_window_deactivate_handlers = []
        self.on_window_hide_handlers = []
        self.fade_in_animation = FadeInAnimationV2(self, self.logger.getChild('fade_in_animation'))
        self.fade_out_animation = FadeOutAnimationV2(self, self.logger.getChild('fade_out_animation'))
        self.ui_objects = []
        self.buttons = []

    @is_not_active
    def on_activate(self):
        self.is_activated = True

    @is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height

    @final
    def on_fade_animation_update(self, dt):
        self.fade_in_animation.on_update(dt)
        self.fade_out_animation.on_update(dt)
        for o in self.ui_objects:
            o.on_fade_animation_update(dt)

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        for o in self.ui_objects:
            o.on_update_fade_animation_state(new_state)
