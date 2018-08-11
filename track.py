from game_object import GameObject
import configparser


class Track(GameObject):
    def __init__(self, track_number, base_routes_in_track):
        super().__init__()
        self.config = None
        self.track_number = track_number
        self.base_routes = base_routes_in_track
        self.busy = False
        self.last_entered_by = None
        self.override = False
        self.read_track_state()

    def read_track_state(self):
        self.config = configparser.RawConfigParser()
        self.config.read('tracks_cfg/track{}.ini'.format(self.track_number))
        self.busy = self.config['user_data'].getboolean('busy')
        self.last_entered_by = self.config['user_data'].getint('last_entered_by')
        self.override = self.config['user_data'].getboolean('override')

    def update(self, game_paused):
        # if game is paused, track status should not be updated
        # if track settings are overridden, we do nothing too
        if not game_paused and not self.override:
            busy_1 = False
            # if any of 4 base routes are busy, all track will become busy
            for i in self.base_routes:
                busy_1 = busy_1 or i.route_config['busy']
                if i.route_config['busy']:
                    self.last_entered_by = i.route_config['last_entered_by']

            self.busy = busy_1
