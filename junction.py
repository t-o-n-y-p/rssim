from game_object import GameObject
import configparser
import os


class Junction(GameObject):
    def __init__(self, straight_track, side_track, direction):
        super().__init__()
        self.straight_track = straight_track
        self.side_track = side_track
        self.direction = direction
        self.dependencies = []
        self.busy = False
        self.last_entered_by = 0
        self.busy_from_dependencies = False
        self.trail_points = {self.straight_track: (), self.side_track: ()}
        self.config = None
        self.read_state()

    def read_state(self):
        self.config = configparser.RawConfigParser()
        if os.path.exists('user_cfg/junctions/junction_{}_{}_{}.ini'.format(self.straight_track,
                                                                            self.side_track,
                                                                            self.direction)):
            self.config.read('user_cfg/junctions/junction_{}_{}_{}.ini'.format(self.straight_track,
                                                                               self.side_track,
                                                                               self.direction))
        else:
            self.config.read('default_cfg/junctions/junction_{}_{}_{}.ini'.format(self.straight_track,
                                                                                  self.side_track,
                                                                                  self.direction))

        self.busy = self.config['user_data'].getboolean('busy')
        self.last_entered_by = self.config['user_data'].getint('last_entered_by')
        self.busy_from_dependencies = self.config['user_data'].getboolean('busy_from_dependencies')
        straight_trail_points_parsed = self.config['junction_config']['straight_trail_points'].split('|')
        for i in range(len(straight_trail_points_parsed)):
            straight_trail_points_parsed[i] = straight_trail_points_parsed[i].split(',')
            straight_trail_points_parsed[i] = (int(straight_trail_points_parsed[i][0]),
                                               int(straight_trail_points_parsed[i][1]))

        self.straight_trail_points = tuple(straight_trail_points_parsed)
        side_trail_points_parsed = self.config['junction_config']['side_trail_points'].split('|')
        for i in range(len(side_trail_points_parsed)):
            side_trail_points_parsed[i] = side_trail_points_parsed[i].split(',')
            side_trail_points_parsed[i] = (int(side_trail_points_parsed[i][0]),
                                           int(side_trail_points_parsed[i][1]))

        self.side_trail_points = tuple(side_trail_points_parsed)

    def save_state(self):
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        if not os.path.exists('user_cfg/junctions'):
            os.mkdir('user_cfg/junctions')

        self.config['user_data']['busy'] = str(self.busy)
        self.config['user_data']['last_entered_by'] = str(self.last_entered_by)
        self.config['user_data']['busy_from_dependencies'] = str(self.busy_from_dependencies)

        with open('user_cfg/junctions/junction_{}_{}_{}.ini'.format(
                self.straight_track, self.side_track, self.direction), 'w') as configfile:
            self.config.write(configfile)

    def update(self, game_paused):
        if not game_paused:
            self.busy_from_dependencies = False
            for i in self.dependencies:
                self.busy_from_dependencies = self.busy_from_dependencies or i.busy

