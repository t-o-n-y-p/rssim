from typing import Final


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION: Final = (0, 10, 2)                    # current app version
MIN_UPDATE_COMPATIBLE_VERSION: Final = (0, 10, 2)      # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE: Final = 8192                    # maximum texture resolution presented in the app
FPS_INTERVAL: Final = 0.2                              # interval between FPS update
LOG_LEVEL_OFF: Final = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO: Final = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG: Final = 10                            # integer log level which includes all possible logs
DATABASE_SHA512: Final = '9513d513bb5bf1c02aa131e2b5ec3815e28a84b105862fec80cd63c1811403daf781df2c6e79180e9832e01384cbd9c7e3243c149eb9858a733c45d09d775db9'
MAXIMUM_DRAW_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
# app version tuple members
MAJOR: Final = 0
MINOR: Final = 1
PATCH: Final = 2
# ------------------- END CONSTANTS -------------------
