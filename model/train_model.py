from .model_base import Model


def _model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def _model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


class TrainModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.direction_from_left_to_right = 0
        self.direction_from_right_to_left = 1
        self.direction_from_left_to_right_side = 2
        self.direction_from_right_to_left_side = 3
        self.cars = None
        self.track = None
        self.train_route = None
        self.state = None
        self.direction = None
        self.new_direction = None
        self.current_direction = None
        self.speed = None
        self.speed_state = None
        self.speed_factor_position = None
        self.priority = None
        self.boarding_time = None
        self.exp = None
        self.money = None
        self.cars_position = None
        self.cars_position_abs = None
        self.stop_point = None
        self.destination_point = None

    def on_train_setup(self, train_id):
        self.user_db_cursor.execute('''SELECT * FROM trains WHERE train_id = ?''', (train_id, ))
        train_id, self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.speed_factor_position, self.priority, \
            self.boarding_time, self.exp, self.money, cars_position_parsed, cars_position_abs_parsed \
            = self.user_db_cursor.fetchone()
        if cars_position_parsed is not None:
            cars_position_parsed = cars_position_parsed.split(',')
            for i in range(len(cars_position_parsed)):
                cars_position_parsed[i] = int(cars_position_parsed[i])

        self.cars_position = cars_position_parsed
        if cars_position_abs_parsed is not None:
            cars_position_abs_parsed = cars_position_abs_parsed.split('|')
            for i in range(len(cars_position_abs_parsed)):
                cars_position_abs_parsed[i] = cars_position_abs_parsed[i].split(',')
                cars_position_abs_parsed[i][0] = int(cars_position_abs_parsed[i][0])
                cars_position_abs_parsed[i][1] = int(cars_position_abs_parsed[i][1])

        self.cars_position_abs = cars_position_abs_parsed

    def on_train_init(self, cars, track, train_route, status, direction, new_direction, current_direction, speed,
                      speed_state, priority, boarding_time, exp, money):
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.priority, self.boarding_time, \
            self.exp, self.money \
            = cars, track, train_route, status, direction, new_direction, current_direction, speed, speed_state, \
            priority, boarding_time, exp, money

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = None
        for i in range(self.cars):
            self.cars_position.append(first_car_start_point - i * 251)

    def on_set_train_stop_point(self, first_car_stop_point):
        self.stop_point = first_car_stop_point

    def on_set_train_destination_point(self, first_car_destination_point):
        self.destination_point = first_car_destination_point

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        self.view.on_activate()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_save_state(self):
        pass

    def on_update_time(self, game_time):
        if self.cars < 9:
            self.priority += 1
        elif self.cars < 12:
            self.priority += 2
        elif self.cars < 15:
            self.priority += 3
        elif self.cars < 18:
            self.priority += 4
        elif self.cars < 21:
            self.priority += 5

        self.controller.parent_controller.on_update_train_route_priority(self.track, self.train_route, self.priority)
