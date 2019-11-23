from typing import Final


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION: Final = (0, 9, 8)                     # current app version
MIN_UPDATE_COMPATIBLE_VERSION: Final = (0, 9, 8)       # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE: Final = 8192                    # maximum texture resolution presented in the app
FPS_INTERVAL: Final = 0.2                              # interval between FPS update
LOG_LEVEL_OFF: Final = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO: Final = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG: Final = 10                            # integer log level which includes all possible logs
DATABASE_SHA512: Final = '6d91af06f4b7ef3ba161fefb4dd589ee924139ce435962989e38049beb2893e3b0b1d2b19bf50dbdb36a53395a17b9b7246cd8875adb7c830b07598eec554ed5'
MAXIMUM_DRAW_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
# app version tuple members
MAJOR: Final = 0
MINOR: Final = 1
PATCH: Final = 2
# ------------------- END CONSTANTS -------------------
