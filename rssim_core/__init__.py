from ctypes import c_long, windll
from os import path
from typing import Final
from hashlib import sha512

from keyring import get_password
from pyglet import gl

from database import USER_DB_LOCATION
from exceptions import VideoAdapterNotSupportedException, MonitorNotSupportedException, HackingDetectedException
from ui import MIN_RESOLUTION_WIDTH, MIN_RESOLUTION_HEIGHT


def video_adapter_is_supported(fn):
    def _launch_game_if_video_adapter_is_supported(*args, **kwargs):
        # determine if video adapter supports all game textures, if not - raise specific exception
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < REQUIRED_TEXTURE_SIZE:
            raise VideoAdapterNotSupportedException

        fn(*args, **kwargs)

    return _launch_game_if_video_adapter_is_supported


def monitor_is_supported(fn):
    def _launch_game_if_monitor_is_supported(*args, **kwargs):
        # determine if screen resolution meets requirements, if not - raise specific exception
        if windll.user32.GetSystemMetrics(0) < MIN_RESOLUTION_WIDTH \
                or windll.user32.GetSystemMetrics(1) < MIN_RESOLUTION_HEIGHT:
            raise MonitorNotSupportedException

        fn(*args, **kwargs)

    return _launch_game_if_monitor_is_supported


def game_config_was_not_modified(fn):
    def _launch_game_if_game_config_was_not_modified(*args, **kwargs):
        with open('db/config.db', 'rb') as f1, open('db/default.db', 'rb') as f2:
            data = (f2.read() + f1.read())[::-1]
            if sha512(data[::3] + data[1::3] + data[2::3]).hexdigest() != DATABASE_SHA512:
                raise HackingDetectedException

            fn(*args, **kwargs)

    return _launch_game_if_game_config_was_not_modified


def player_progress_was_not_modified(fn):
    def _launch_game_if_player_progress_was_not_modified(*args, **kwargs):
        with open(path.join(USER_DB_LOCATION, 'user.db'), 'rb') as f:
            data = f.read()[::-1]
            if sha512(data[::3] + data[1::3] + data[2::3]).hexdigest() \
                    != get_password(sha512('user_db'.encode('utf-8')).hexdigest(),
                                    sha512('user_db'.encode('utf-8')).hexdigest()):
                raise HackingDetectedException

            fn(*args, **kwargs)

    return _launch_game_if_player_progress_was_not_modified


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION: Final = (0, 10, 2)                    # current app version
MIN_UPDATE_COMPATIBLE_VERSION: Final = (0, 10, 2)      # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE: Final = 8192                    # maximum texture resolution presented in the app
LOG_LEVEL_OFF: Final = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO: Final = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG: Final = 10                            # integer log level which includes all possible logs
DATABASE_SHA512: Final = '52c573adb50b906ce8258f288366d409cb55923c9cb1b08cc2f46a4ab29e30bec49941243e4d3145f0536e246b23460480216889acdd8221b31e7917bce91f3e'
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_SCROLL_EVENTS_PER_FRAME: Final = 1
# app version tuple members
MAJOR: Final = 0
MINOR: Final = 1
PATCH: Final = 2
# ------------------- END CONSTANTS -------------------
