# --------------------- CONSTANTS ---------------------
SCHEDULE_ROWS = 12                              # number of schedule rows on schedule screen
SCHEDULE_COLUMNS = 2                            # number of schedule columns on schedule screen
# track and environment state matrix properties
LOCKED = 0                                      # property #0 indicates if track/env. is locked
UNDER_CONSTRUCTION = 1                          # property #1 indicates if track/env. is under construction
CONSTRUCTION_TIME = 2                           # property #2 indicates construction time left
UNLOCK_CONDITION_FROM_LEVEL = 3                 # property #3 indicates if unlock condition from level is met
UNLOCK_CONDITION_FROM_PREVIOUS_TRACK = 4        # property #4 indicates if unlock condition from previous track is met
UNLOCK_CONDITION_FROM_PREVIOUS_ENVIRONMENT = 4  # property #4 indicates if unlock condition from previous env. is met
UNLOCK_CONDITION_FROM_ENVIRONMENT = 5           # property #5 indicates if unlock condition from environment is met
UNLOCK_AVAILABLE = 6                            # property #6 indicates if all unlock conditions are met
PRICE = 7                                       # property #7 indicates track/env. price
LEVEL_REQUIRED = 8                              # property #8 indicates required level for this track/env.
ENVIRONMENT_REQUIRED = 9                        # property #9 indicates required environment tier for this track
# colors
GREY = (112, 112, 112, 255)                     # grey UI color
ORANGE = (255, 127, 0, 255)                     # orange UI color
GREEN = (0, 192, 0, 255)                        # green UI color
RED = (255, 0, 0, 255)                          # red UI color
# time
FRAMES_IN_ONE_DAY = 345600                      # indicates how many frames fit in one in-game day
FRAMES_IN_ONE_HOUR = 14400                      # indicates how many frames fit in one in-game hour
FRAMES_IN_ONE_MINUTE = 240                      # indicates how many frames fit in one in-game minute
FRAMES_IN_ONE_SECOND = 4                        # indicates how many frames fit in one in-game second
MINUTES_IN_ONE_HOUR = 60
SECONDS_IN_ONE_MINUTE = 60
HOURS_IN_ONE_DAY = 24
# base_schedule matrix properties
TRAIN_ID = 0                                    # property #0 indicates train identification number
ARRIVAL_TIME = 1                                # property #1 indicates arrival time
DIRECTION = 2                                   # property #2 indicates direction
NEW_DIRECTION = 3                               # property #3 indicates new direction
CARS = 4                                        # property #4 indicates number of cars
STOP_TIME = 5                                   # property #5 indicates how much stop time left
EXP = 6                                         # property #6 indicates how much exp the train gives
MONEY = 7                                       # property #7 indicates how much money the train gives
# ------------------- END CONSTANTS -------------------
