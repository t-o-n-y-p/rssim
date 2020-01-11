from typing import Final


# --------------------- CONSTANTS ---------------------
CURRENT_VERSION: Final = (0, 10, 2)                    # current app version
MIN_UPDATE_COMPATIBLE_VERSION: Final = (0, 10, 2)      # game cannot be updated from version earlier than this
REQUIRED_TEXTURE_SIZE: Final = 8192                    # maximum texture resolution presented in the app
FPS_INTERVAL: Final = 0.2                              # interval between FPS update
LOG_LEVEL_OFF: Final = 30                              # integer log level high enough to cut off all logs
LOG_LEVEL_INFO: Final = 20                             # integer log level which includes basic logs
LOG_LEVEL_DEBUG: Final = 10                            # integer log level which includes all possible logs
DATABASE_SHA512: Final = 'aeceaa06546349242964c2d5a670a63d361412455ca0119159d1f44654075cc28d98c936fa47e4bdd3a8203bfdd7c200d82aaf4bbb166cd4fea1dd4c15520e76'
MAXIMUM_DRAW_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
# app version tuple members
MAJOR: Final = 0
MINOR: Final = 1
PATCH: Final = 2
# ------------------- END CONSTANTS -------------------
