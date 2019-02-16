from logging import getLogger

from model import *


class TrainModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor, train_id):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger(f'root.app.game.map.train.{train_id}.model'))
        self.train_maximum_speed = TRAIN_ACCELERATION_FACTOR[-1] - TRAIN_ACCELERATION_FACTOR[-2]
        self.speed_factor_position_limit = len(TRAIN_ACCELERATION_FACTOR) - 1
        self.cars = 0
        self.track = 0
        self.train_route = ''
        self.state = ''
        self.direction = 0
        self.new_direction = 0
        self.current_direction = 0
        self.speed = 0
        self.speed_state = ''
        self.speed_factor_position = 0
        self.priority = 0
        self.boarding_time = 0
        self.exp = 0.0
        self.money = 0.0
        self.cars_position = []
        self.cars_position_abs = []
        self.stop_point = 0
        self.destination_point = 0
        self.trail_points_v2 = []
        self.car_image_collection = 0

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

    def on_train_init(self, cars, track, train_route, state, direction, new_direction, current_direction,
                      priority, boarding_time, exp, money, car_image_collection):
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.priority, self.boarding_time, \
            self.exp, self.money, self.car_image_collection \
            = cars, track, train_route, state, direction, new_direction, current_direction, \
            priority, boarding_time, exp, money, car_image_collection
        self.speed = self.train_maximum_speed
        self.speed_state = 'move'
        self.speed_factor_position = self.speed_factor_position_limit

    def on_set_train_start_point(self, first_car_start_point):
        self.cars_position = []
        for i in range(self.cars):
            self.cars_position.append(first_car_start_point - i * 251)

    def on_set_train_stop_point(self, first_car_stop_point):
        self.stop_point = first_car_stop_point

    def on_set_train_destination_point(self, first_car_destination_point):
        self.destination_point = first_car_destination_point

    def on_set_trail_points(self, trail_points_v2):
        self.trail_points_v2 = trail_points_v2

    @model_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        car_position_view = []
        if len(self.cars_position) > 0:
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

    @model_is_active
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
                                     self.stop_point, self.destination_point, self.car_image_collection))

    def on_update_time(self, game_time):
        if self.cars < 9:
            self.priority += 5
        elif self.cars < 12:
            self.priority += 4
        elif self.cars < 15:
            self.priority += 3
        elif self.cars < 18:
            self.priority += 2
        elif self.cars < 21:
            self.priority += 1

        self.controller.parent_controller.on_update_train_route_priority(self.track, self.train_route, self.priority)

        if self.state not in ('boarding_in_progress', 'boarding_in_progress_pass_through'):
            if self.cars_position[0] == self.stop_point:
                self.speed_state = 'stop'
                self.speed = 0
                self.speed_factor_position = 0
            elif self.stop_point - self.cars_position[0] <= TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]:
                self.speed_state = 'decelerate'
            else:
                if self.speed_state != 'move':
                    self.speed_state = 'accelerate'

            if self.cars_position[0] == self.destination_point:
                if self.state not in ('approaching', 'approaching_pass_through'):
                    self.controller.parent_controller.on_close_train_route(self.track, self.train_route)

                if self.state == 'pending_boarding':
                    self.priority = 0
                    if self.track in (1, 2):
                        self.state = 'boarding_in_progress_pass_through'
                    else:
                        self.state = 'boarding_in_progress'

                    self.view.on_update_state(self.state)
                    self.on_convert_trail_points()
                    self.trail_points_v2 = None
                elif self.state == 'boarding_complete':
                    self.state = 'successful_departure'

            if self.speed_state == 'accelerate':
                if self.speed_factor_position == self.speed_factor_position_limit:
                    self.speed_state = 'move'
                    self.speed = self.train_maximum_speed
                else:
                    self.speed = TRAIN_ACCELERATION_FACTOR[self.speed_factor_position + 1] \
                               - TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]
                    self.speed_factor_position += 1

            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.speed = TRAIN_ACCELERATION_FACTOR[self.speed_factor_position + 1] \
                           - TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]

            if self.speed_state != 'stop':
                car_position_view = []
                for i in range(len(self.cars_position)):
                    self.cars_position[i] += self.speed
                    car_position_view.append(self.trail_points_v2[self.cars_position[i]])

                self.view.on_update_car_position(car_position_view)
                self.controller.parent_controller.on_update_train_route_sections(self.track, self.train_route,
                                                                                 self.cars_position[-1])

        else:
            self.boarding_time -= 1
            if self.boarding_time == FRAMES_IN_ONE_MINUTE:
                self.current_direction = self.new_direction
                self.train_route = EXIT_TRAIN_ROUTE[self.current_direction]
                if self.direction % 2 != self.new_direction % 2:
                    self.on_switch_direction()

                self.controller.parent_controller.on_open_train_route(self.track, self.train_route,
                                                                      self.controller.train_id, self.cars)
                self.on_reconvert_trail_points()

            if self.boarding_time == 0:
                self.state = 'boarding_complete'
                self.view.on_update_state(self.state)
                self.controller.parent_controller.parent_controller.on_add_exp(self.exp)
                self.controller.parent_controller.parent_controller.on_add_money(self.money)

    def on_convert_trail_points(self):
        self.cars_position_abs = []
        for i in self.cars_position:
            dot = self.trail_points_v2[i]
            self.cars_position_abs.append([dot[0], dot[1]])

        self.cars_position.clear()

    def on_reconvert_trail_points(self):
        self.cars_position = []
        for i in self.cars_position_abs:
            self.cars_position.append(abs(i[0] - self.trail_points_v2[0][0]))

        self.cars_position_abs.clear()

    def on_switch_direction(self):
        self.cars_position_abs = list(reversed(self.cars_position_abs))
