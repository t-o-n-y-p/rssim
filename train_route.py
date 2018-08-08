import config as c
from game_object import GameObject


class TrainRoute(GameObject):
    def __init__(self, base_routes, track_number, route_type):
        super().__init__()
        self.track_number = track_number
        self.base_routes = base_routes
        # while train moves, some pieces of train route become free
        self.busy_routes = []
        self.opened_routes = []
        self.route_type = route_type
        self.opened = False
        self.last_opened_by = None
        self.trail_points = []
        self.start_point = None
        # to aggregate all possible stop points
        self.stop_points = []
        # to aggregate stop points based on red signals
        self.active_stop_points = []
        # single stop point which is closest to the first chassis of the train
        self.next_stop_point = None
        self.destination_point = None
        self.supported_carts = [0, 0]
        self.signals = []
        # number of supported carts is decided below
        for j in self.base_routes:
            if j.route_config.supported_carts[0] > self.supported_carts[0]:
                self.supported_carts[0] = j.route_config.supported_carts[0]

            if j.route_config.supported_carts[1] > self.supported_carts[1]:
                self.supported_carts[1] = j.route_config.supported_carts[1]

        # merge trail points of all base routes into single route
        for i in self.base_routes:
            self.trail_points.extend(list(i.route_config.trail_points))

        # get start point for entire route if it exists
        if len(self.base_routes) > 0:
            if self.base_routes[0].route_config.start_point:
                self.start_point = self.trail_points.index(self.base_routes[0].route_config.start_point)

        # get all signals along the way
        for j in self.base_routes:
            if j.route_config.exit_signal:
                self.signals.append(j.route_config.exit_signal)

    def set_next_stop_point(self, first_cart_position):
        # update single stop point which is closest to the first chassis of the train
        index = len(self.active_stop_points)
        if index == 1:
            if first_cart_position <= self.active_stop_points[0]:
                self.next_stop_point = self.active_stop_points[0]
        elif index > 1:
            if first_cart_position <= self.active_stop_points[0]:
                self.next_stop_point = self.active_stop_points[0]
            else:
                for i in range(index-1):
                    if first_cart_position in (self.active_stop_points[i]+1, self.active_stop_points[i+1]+1):
                        self.next_stop_point = self.active_stop_points[i+1]

    def set_stop_points(self, carts):
        self.stop_points = []
        self.active_stop_points = []
        self.destination_point = None
        for j in self.base_routes:
            if j.route_config.stop_point:
                self.stop_points.append(self.trail_points.index(j.route_config.stop_point[carts]))

        if len(self.stop_points) > 0:
            for i in self.stop_points:
                self.active_stop_points.append(i)

            self.destination_point = self.stop_points[len(self.stop_points)-1]

        self.supported_carts = tuple(self.supported_carts)
        self.set_next_stop_point(0)

    def open_train_route(self, train_id):
        # open route and all base routes included;
        # remember which train opens it
        self.opened = True
        self.last_opened_by = train_id
        self.base_routes[0].route_config.busy = True
        self.base_routes[0].last_entered_by = train_id
        self.busy_routes.clear()
        self.opened_routes.clear()
        for i in self.base_routes:
            i.route_config.opened = True
            i.last_opened_by = train_id
            self.busy_routes.append(i)
            self.opened_routes.append(i)

    def close_train_route(self):
        # fully unlock entire route and remaining base routes
        self.opened = False
        for i in self.opened_routes:
            i.route_config.opened = False

        for i in self.busy_routes:
            i.route_config.busy = False

    def update(self, game_paused):
        if not game_paused:
            # if signal turns green, make this stop point inactive
            self.active_stop_points = []
            index = list(range(len(self.signals)))
            for i in index:
                if self.signals[i].state != c.GREEN_SIGNAL and len(self.stop_points) > 0:
                    self.active_stop_points.append(self.stop_points[i])
