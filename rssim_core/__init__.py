from typing import Final


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION: Final = (0, 9, 8)                     # current app version
MIN_UPDATE_COMPATIBLE_VERSION: Final = (0, 9, 8)       # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE: Final = 8192                    # maximum texture resolution presented in the app
FPS_INTERVAL: Final = 0.2                              # interval between FPS update
LOG_LEVEL_OFF: Final = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO: Final = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG: Final = 10                            # integer log level which includes all possible logs
DATABASE_SHA512: Final = 'd3ad5f4757136f0df404d77c707f86c3de9bd348bcf797e773fd0450c7239b99f73529b7541f753ad49657f7f1c3df91fff350923cc50651f184bb1012879ddc'
MAXIMUM_DRAW_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
# app version tuple members
MAJOR: Final = 0
MINOR: Final = 1
PATCH: Final = 2
# ------------------- END CONSTANTS -------------------
