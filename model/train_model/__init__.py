from logging import getLogger

from model import *
from database import USER_DB_CURSOR


class TrainModel(MapBaseModel):
    def __init__(self, map_id, train_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.model'))
        self.map_id = map_id
        self.train_acceleration_factor = None
        self.train_maximum_speed = None
        self.speed_factor_position_limit = None
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
        self.trail_points_v2_head_tail = []
        self.trail_points_v2_mid = []
        self.car_image_collection = 0
        self.exp_bonus_multiplier = None
        self.money_bonus_multiplier = None

    def on_train_setup(self, train_id):
        USER_DB_CURSOR.execute('''SELECT train_id, cars, train_route_track_number, train_route_type, 
                                  state, direction, new_direction, current_direction, speed, speed_state, 
                                  speed_factor_position, priority, boarding_time, exp, money, 
                                  cars_position, cars_position_abs, stop_point, destination_point, 
                                  car_image_collection FROM trains WHERE train_id = ? AND map_id = ?''',
                               (train_id, self.map_id))
        train_id, self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.speed_factor_position, self.priority, \
            self.boarding_time, self.exp, self.money, cars_position_parsed, cars_position_abs_parsed, \
            self.stop_point, self.destination_point, self.car_image_collection \
            = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT exp_bonus_multiplier, money_bonus_multiplier FROM game_progress''')
        self.exp_bonus_multiplier, self.money_bonus_multiplier = USER_DB_CURSOR.fetchone()
        if cars_position_parsed is not None:
            self.cars_position = list(map(float, cars_position_parsed.split(',')))

        if cars_position_abs_parsed is not None:
            cars_position_abs_parsed = cars_position_abs_parsed.split('|')
            for i in range(len(cars_position_abs_parsed)):
                cars_position_abs_parsed[i] = list(map(float, cars_position_abs_parsed[i].split(',')))

            self.cars_position_abs = cars_position_abs_parsed

    def on_train_init(self, cars, track, train_route, state, direction, new_direction, current_direction,
                      priority, boarding_time, exp, money, car_image_collection,
                      exp_bonus_multiplier, money_bonus_multiplier):
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.priority, self.boarding_time, \
            self.exp, self.money, self.car_image_collection, self.exp_bonus_multiplier, self.money_bonus_multiplier \
            = cars, track, train_route, state, direction, new_direction, current_direction, \
            priority, boarding_time, exp, money, car_image_collection, exp_bonus_multiplier, money_bonus_multiplier
        self.speed = self.train_maximum_speed
        self.speed_state = 'move'
        self.speed_factor_position = self.speed_factor_position_limit

    def on_set_train_start_point(self, first_car_start_point):
        pass

    def on_set_train_stop_point(self, first_car_stop_point):
        self.stop_point = first_car_stop_point

    def on_set_train_destination_point(self, first_car_destination_point):
        self.destination_point = first_car_destination_point

    def on_set_trail_points(self, trail_points_v2_head_tail, trail_points_v2_mid):
        self.trail_points_v2_head_tail = trail_points_v2_head_tail
        self.trail_points_v2_mid = trail_points_v2_mid

    def on_activate_view(self):
        car_position_view = []
        if len(self.cars_position) > 0:
            for i in range(len(self.cars_position)):
                car_position_view.append(self.on_calculate_car_position_view(i))
        else:
            for i in self.cars_position_abs:
                car_position_view.append((i[0], i[1], 0.0))

        self.view.on_update_car_position(car_position_view)
        self.view.on_update_direction(self.current_direction)
        self.view.on_update_car_image_collection(self.car_image_collection)
        self.view.on_update_state(self.state)
        self.view.on_activate()

    def on_save_state(self):
        cars_position_string = None
        if len(self.cars_position) > 0:
            cars_position_string = ','.join(list(map(str, self.cars_position)))

        cars_position_abs_strings_list = []
        cars_position_abs_string = None
        if len(self.cars_position_abs) > 0:
            for i in self.cars_position_abs:
                cars_position_abs_strings_list.append(','.join(list(map(str, i))))

            cars_position_abs_string = '|'.join(list(map(str, cars_position_abs_strings_list)))

        USER_DB_CURSOR.execute('''INSERT INTO trains VALUES 
                                  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (self.map_id, self.controller.train_id, self.cars, self.track, self.train_route,
                                self.state, self.direction, self.new_direction, self.current_direction, self.speed,
                                self.speed_state, self.speed_factor_position, self.priority, self.boarding_time,
                                self.exp, self.money, cars_position_string, cars_position_abs_string,
                                self.stop_point, self.destination_point, self.car_image_collection))

    def on_update_time(self):
        super().on_update_time()
        # shorter trains gain more priority because they arrive more frequently
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

        # update train route priority to be sorted and dispatched in correct order
        self.controller.parent_controller.on_update_train_route_priority(self.track, self.train_route, self.priority)

        if self.state not in ('boarding_in_progress', 'boarding_in_progress_pass_through'):
            # update speed and speed state
            # when train reaches stop point, update state to 'stop', speed and speed_factor_position to 0
            if int(self.cars_position[0]) == self.stop_point:
                self.speed_state = 'stop'
                self.speed = 0
                self.speed_factor_position = 0
            # when train needs to stop at stop point and distance is less than braking distance,
            # update state to 'decelerate'
            elif round(self.stop_point - self.cars_position[0], 1) \
                    <= self.train_acceleration_factor[self.speed_factor_position]:
                self.speed_state = 'decelerate'
            # when train needs to stop at stop point and distance is more than braking distance,
            # update state to 'accelerate' if train is not at maximum speed already
            else:
                if self.speed_state != 'move':
                    self.speed_state = 'accelerate'

            # when train reaches destination point, current train route is complete,
            # update state according to previous state
            if int(self.cars_position[0]) == self.destination_point:
                # approaching routes are closed by dispatcher, other routes can be closed here
                if self.state not in ('approaching', 'approaching_pass_through'):
                    self.controller.parent_controller.on_close_train_route(self.track, self.train_route)

                # 'pending_boarding' state means train arrives for boarding, start boarding
                if self.state == 'pending_boarding':
                    self.priority = 0
                    if self.track in (1, 2):
                        self.state = 'boarding_in_progress_pass_through'
                    else:
                        self.state = 'boarding_in_progress'

                    self.view.on_update_state(self.state)
                    # when boarding is started, convert trail points to 2D Cartesian
                    self.on_convert_trail_points()
                    self.trail_points_v2_head_tail = None
                    self.trail_points_v2_mid = None
                # 'boarding_complete' state means train has finished entire process,
                # update state to 'successful_departure' to delete this train later
                elif self.state == 'boarding_complete':
                    self.state = 'successful_departure'

            # update speed depending on speed state
            if self.speed_state == 'accelerate':
                # if train has finished acceleration, update state to 'move' (moving at maximum speed)
                if self.speed_factor_position == self.speed_factor_position_limit:
                    self.speed_state = 'move'
                    self.speed = self.train_maximum_speed
                # if not, continue acceleration
                else:
                    self.speed = self.train_acceleration_factor[self.speed_factor_position + 1] \
                                 - self.train_acceleration_factor[self.speed_factor_position]
                    self.speed_factor_position += 1

            # if train decelerates, continue deceleration
            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.speed = self.train_acceleration_factor[self.speed_factor_position + 1] \
                             - self.train_acceleration_factor[self.speed_factor_position]

            # if train is not stopped, move all cars ahead
            if self.speed_state != 'stop':
                car_position_view = []
                for i in range(len(self.cars_position)):
                    self.cars_position[i] = round(self.cars_position[i] + self.speed, 1)
                    car_position_view.append(self.on_calculate_car_position_view(i))

                self.view.on_update_car_position(car_position_view)
                self.controller.parent_controller\
                    .on_update_train_route_sections(self.track, self.train_route, self.cars_position[-1])
        else:
            # if boarding is in progress, decrease boarding time
            self.boarding_time -= 1
            # after one minute left, assign exit rain route depending on new direction
            if self.boarding_time == FRAMES_IN_ONE_MINUTE // 2:
                self.current_direction = self.new_direction
                self.train_route = EXIT_TRAIN_ROUTE[self.map_id][self.current_direction]
                self.view.on_update_direction(self.current_direction)
                if self.direction % 2 != self.new_direction % 2:
                    self.on_switch_direction()

                self.controller.parent_controller.on_open_train_route(self.track, self.train_route,
                                                                      self.controller.train_id, self.cars)
                self.on_reconvert_trail_points()

            # after boarding time is over, update train state and add exp/money
            if self.boarding_time == 0:
                self.state = 'boarding_complete'
                self.view.on_update_state(self.state)
                self.controller.parent_controller.parent_controller.on_add_exp(self.exp * self.exp_bonus_multiplier)
                self.controller.parent_controller.parent_controller\
                    .on_add_money(self.money * self.money_bonus_multiplier)

    def on_convert_trail_points(self):
        self.cars_position_abs = []
        for i in range(len(self.cars_position)):
            if i in (0, len(self.cars_position) - 1):
                dot = self.trail_points_v2_head_tail[round(self.cars_position[i])]
            else:
                dot = self.trail_points_v2_mid[round(self.cars_position[i])]

            self.cars_position_abs.append([dot[0], dot[1]])

        self.cars_position.clear()

    def on_reconvert_trail_points(self):
        self.cars_position = []
        for i in range(len(self.cars_position_abs)):
            if i in (0, len(self.cars_position_abs) - 1):
                self.cars_position.append(float(round(abs(self.cars_position_abs[i][0]
                                                          - self.trail_points_v2_head_tail[0][0]))))
            else:
                self.cars_position.append(float(round(abs(self.cars_position_abs[i][0]
                                                          - self.trail_points_v2_mid[0][0]))))

        self.cars_position_abs.clear()

    def on_switch_direction(self):
        self.cars_position_abs = list(reversed(self.cars_position_abs))
        car_position_view = []
        for i in self.cars_position_abs:
            car_position_view.append((i[0], i[1], 0.0))

        self.view.on_update_car_position(car_position_view)

    def on_calculate_car_position_view(self, car_index):
        if car_index in (0, len(self.cars_position) - 1):
            if self.cars_position[car_index] % 1 < 0.1:
                return self.trail_points_v2_head_tail[round(self.cars_position[car_index])]
            else:
                return (
                    (self.trail_points_v2_head_tail[int(self.cars_position[car_index])][0]
                     + self.trail_points_v2_head_tail[int(self.cars_position[car_index]) + 1][0]) / 2,
                    (self.trail_points_v2_head_tail[int(self.cars_position[car_index])][1]
                     + self.trail_points_v2_head_tail[int(self.cars_position[car_index]) + 1][1]) / 2,
                    (self.trail_points_v2_head_tail[int(self.cars_position[car_index])][2]
                     + self.trail_points_v2_head_tail[int(self.cars_position[car_index]) + 1][2]) / 2
                )
        else:
            if self.cars_position[car_index] % 1 < 0.1:
                return self.trail_points_v2_mid[round(self.cars_position[car_index])]
            else:
                return (
                    (self.trail_points_v2_mid[int(self.cars_position[car_index])][0]
                     + self.trail_points_v2_mid[int(self.cars_position[car_index]) + 1][0]) / 2,
                    (self.trail_points_v2_mid[int(self.cars_position[car_index])][1]
                     + self.trail_points_v2_mid[int(self.cars_position[car_index]) + 1][1]) / 2,
                    (self.trail_points_v2_mid[int(self.cars_position[car_index])][2]
                     + self.trail_points_v2_mid[int(self.cars_position[car_index]) + 1][2]) / 2
                )
