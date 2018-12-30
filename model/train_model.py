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
        self.entry_train_route = ('left_entry', 'right_entry', 'left_side_entry', 'right_side_entry')
        self.exit_train_route = ('right_exit', 'left_exit', 'right_side_exit', 'left_side_exit')
        self.approaching_train_route = ('left_approaching', 'right_approaching',
                                        'left_side_approaching', 'right_side_approaching')
        self.train_acceleration_factor = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 6, 6, 6,
                                          7, 7, 7, 8, 8, 9, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16,
                                          17, 17, 18, 18, 19, 20, 20, 21, 21, 22, 23, 23, 24, 25, 26, 26, 27, 28,
                                          29, 29, 30, 31, 32, 32, 33, 34, 35, 36, 37, 37, 38, 39, 40, 41, 42, 43, 44,
                                          45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63,
                                          64, 66, 67, 68, 69, 70, 71, 73, 74, 75, 76, 78, 79, 80, 81, 83, 84, 85, 86,
                                          88, 89, 90, 92, 93, 95, 96, 97, 99, 100, 102, 103, 104, 106, 107, 109, 110,
                                          112, 113, 115, 116, 118, 119, 121, 123, 124, 126, 128, 129, 131, 133, 135,
                                          136, 138, 140, 142, 144, 146, 147, 149, 151, 153, 155, 157, 159, 161, 163,
                                          165, 168, 170, 172, 174, 176, 178, 181, 183, 185, 187, 190, 192, 194, 197,
                                          199, 201, 204, 206, 209, 211, 214, 216, 219, 221, 224, 227, 229, 232, 234,
                                          237, 240, 243, 245, 248, 251, 254, 256, 259, 262, 265, 268, 271, 274, 277,
                                          280, 283, 286, 289, 292, 295, 299, 302, 305, 309, 312, 316, 319, 323, 326,
                                          330, 334, 338, 341, 345, 349, 353, 357, 361, 366, 370, 374, 378, 383, 387,
                                          392, 396, 401, 405, 410, 415, 419, 424, 429, 434, 439, 444, 449, 454, 459,
                                          464, 470, 475, 480, 486, 491, 497, 502, 508, 513, 519, 525, 531, 536, 542,
                                          548, 554, 560, 566, 573, 579, 585, 591, 598, 604, 611, 617, 624, 630, 637,
                                          644, 650, 657, 664, 671, 678, 685)
        self.train_maximum_speed = 7
        self.speed_factor_position_limit = len(self.train_acceleration_factor) - 1
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
        self.trail_points_v2 = None
        self.car_image_collection = None

    def on_train_setup(self, train_id):
        self.user_db_cursor.execute('''SELECT * FROM trains WHERE train_id = ?''', (train_id, ))
        train_id, self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.speed_factor_position, self.priority, \
            self.boarding_time, self.exp, self.money, cars_position_parsed, cars_position_abs_parsed, \
            self.stop_point, self.destination_point, self.car_image_collection \
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
                      speed_state, priority, boarding_time, exp, money, car_image_collection):
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.priority, self.boarding_time, \
            self.exp, self.money, self.car_image_collection \
            = cars, track, train_route, status, direction, new_direction, current_direction, speed, speed_state, \
            priority, boarding_time, exp, money, car_image_collection
        self.speed_factor_position = self.speed_factor_position_limit
        self.controller.parent_controller.on_open_train_route(self.track, self.train_route,
                                                              self.controller.train_id, self.cars)

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = None
        car_position_view = []
        for i in range(self.cars):
            self.cars_position.append(first_car_start_point - i * 251)
            car_position_view.append(self.trail_points_v2[first_car_start_point - i * 251])

        self.view.on_update_car_position(car_position_view)

    def on_set_train_stop_point(self, first_car_stop_point):
        self.stop_point = first_car_stop_point

    def on_set_train_destination_point(self, first_car_destination_point):
        self.destination_point = first_car_destination_point

    def on_set_trail_points(self, trail_points_v2):
        self.trail_points_v2 = trail_points_v2

    @_model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        car_position_view = []
        if self.cars_position is not None:
            for i in self.cars_position:
                car_position_view.append(self.trail_points_v2[i])
        else:
            for i in self.cars_position_abs:
                car_position_view.append((i[0], i[1], 0.0))

        self.view.on_update_car_position(car_position_view)
        self.view.on_update_direction(self.current_direction)
        self.view.on_update_car_image_collection(self.car_image_collection)
        self.view.on_update_state(self.state)
        self.view.on_activate()

    @_model_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_save_state(self):
        cars_position_string = ''
        if len(self.cars_position) == 0:
            cars_position_string = None
        else:
            for i in self.cars_position:
                cars_position_string += f'{i},'

            cars_position_string = cars_position_string[0:len(cars_position_string) - 1]

        cars_position_abs_string = ''
        if len(self.cars_position_abs) == 0:
            cars_position_abs_string = None
        else:
            for i in self.cars_position_abs:
                cars_position_abs_string += f'{i[0]},{i[1]}|'

            cars_position_abs_string = cars_position_abs_string[0:len(cars_position_abs_string) - 1]

        self.user_db_cursor.execute('''INSERT INTO trains VALUES 
                                       (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (self.controller.train_id, self.cars, self.track, self.train_route, self.state,
                                     self.direction, self.new_direction, self.current_direction, self.speed,
                                     self.speed_state, self.speed_factor_position, self.priority, self.boarding_time,
                                     self.exp, self.money, cars_position_string, cars_position_abs_string,
                                     self.stop_point, self.destination_point))

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

        if self.state != 'boarding_in_progress':
            if self.cars_position[0] == self.stop_point:
                self.speed_state = 'stop'
                self.speed = 0
                self.speed_factor_position = 0
            elif self.stop_point - self.cars_position[0] <= self.train_acceleration_factor[self.speed_factor_position]:
                self.speed_state = 'decelerate'
            else:
                if self.speed_state != 'move':
                    self.speed_state = 'accelerate'

            if self.cars_position[0] == self.destination_point:
                self.controller.parent_controller.on_close_train_route(self.track, self.train_route)
                if self.state == 'pending_boarding':
                    self.state = 'boarding_in_progress'
                    self.view.on_update_state(self.state)
                    self.on_convert_trail_points()
                    self.trail_points_v2 = None
                elif self.state == 'boarding_complete':
                    self.controller.parent_controller.on_delete_train(self.controller.train_id)

            if self.speed_state == 'accelerate':
                if self.speed_factor_position == self.speed_factor_position_limit:
                    self.speed_state = 'move'
                    self.speed = self.train_maximum_speed
                else:
                    self.speed = self.train_acceleration_factor[self.speed_factor_position + 1] \
                                 - self.train_acceleration_factor[self.speed_factor_position]
                    self.speed_factor_position += 1

            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.speed = self.train_acceleration_factor[self.speed_factor_position + 1] \
                             - self.train_acceleration_factor[self.speed_factor_position]

            if self.speed_state != 'stop':
                car_position_view = []
                for i in range(len(self.cars_position)):
                    self.cars_position[i] += self.speed
                    car_position_view.append(self.trail_points_v2[self.cars_position[i]])

                self.view.on_update_car_position(car_position_view)

        else:
            self.boarding_time -= 1
            if self.boarding_time == 240:
                self.current_direction = self.new_direction
                self.train_route = self.exit_train_route[self.current_direction]
                if self.direction % 2 != self.new_direction % 2:
                    self.on_switch_direction()

                self.controller.parent_controller.on_open_train_route(self.track, self.train_route,
                                                                      self.controller.train_id, self.cars)
                self.on_reconvert_trail_points()

            if self.boarding_time == 0:
                self.state = 'boarding_complete'
                self.view.on_update_state(self.state)
                self.controller.parent_controller.on_add_exp(self.exp)
                self.controller.parent_controller.on_add_money(self.money)

    def on_convert_trail_points(self):
        self.cars_position_abs.clear()
        for i in self.cars_position:
            dot = self.trail_points_v2[i]
            self.cars_position_abs.append([dot[0], dot[1]])

        self.cars_position.clear()

    def on_reconvert_trail_points(self):
        self.cars_position.clear()
        for i in self.cars_position_abs:
            self.cars_position.append(abs(i[0] - self.trail_points_v2[0][0]))

        self.cars_position_abs.clear()

    def on_switch_direction(self):
        self.cars_position_abs = list(reversed(self.cars_position_abs))
