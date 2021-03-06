from abc import ABC, abstractmethod
from logging import getLogger
from math import log
from typing import final

from database import USER_DB_CURSOR, FALSE, SECONDS_IN_ONE_MINUTE, DEPARTURE_ANNOUNCEMENT, \
    ARRIVAL_FINISHED_ANNOUNCEMENT, FIVE_MINUTES_LEFT_ANNOUNCEMENT
from model import MapBaseModel, TRAIN_MAXIMUM_SPEED, TRAIN_VELOCITY_BASE, get_braking_distance, get_speed_state_time, \
    get_distance, EXIT_TRAIN_ROUTE


class TrainModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id, train_id):
        super().__init__(
            controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.model')
        )
        self.train_id = train_id
        self.cars = 0
        self.track = 0
        self.train_route = ''
        self.state = ''
        self.direction = 0
        self.new_direction = 0
        self.current_direction = 0
        self.speed_state = ''
        self.speed_state_time = 0.0
        self.priority = 0
        self.boarding_time = 0
        self.exp = 0.0
        self.money = 0.0
        self.cars_position = []
        self.cars_position_abs = []
        self.stop_point = 0
        self.destination_point = 0
        self.trail_points_v2 = None
        self.car_image_collection = 0
        self.switch_direction_required = FALSE

    @final
    def on_train_setup(self):
        USER_DB_CURSOR.execute(
            '''SELECT cars, train_route_track_number, train_route_type, state, direction, new_direction, 
            current_direction, speed_state, speed_state_time, priority, boarding_time, exp, money, cars_position, 
            cars_position_abs, stop_point, destination_point, car_image_collection, switch_direction_required 
            FROM trains WHERE train_id = ? AND map_id = ?''', (self.train_id, self.map_id)
        )
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed_state, self.speed_state_time, self.priority, \
            self.boarding_time, self.exp, self.money, cars_position_parsed, cars_position_abs_parsed, \
            self.stop_point, self.destination_point, self.car_image_collection, self.switch_direction_required \
            = USER_DB_CURSOR.fetchone()
        if cars_position_parsed is not None:
            self.cars_position = [float(p) for p in cars_position_parsed.split(',')]
            self.view.car_position = []
            self.view.car_position.append(self.trail_points_v2.get_head_tail_car_position(self.cars_position[0]))
            for i in range(1, len(self.cars_position) - 1):
                self.view.car_position.append(self.trail_points_v2.get_mid_car_position(self.cars_position[i]))

            self.view.car_position.append(self.trail_points_v2.get_head_tail_car_position(self.cars_position[-1]))

        if cars_position_abs_parsed is not None:
            self.cars_position_abs = [[float(p) for p in s.split(',')] for s in cars_position_abs_parsed.split('|')]
            self.view.car_position = []
            for i in range(len(self.cars_position_abs)):
                self.view.car_position.append([*self.cars_position_abs[i], 0.0])

        self.view.on_train_setup()

    @final
    def on_train_init(
            self, cars, track, train_route, state, direction, new_direction, current_direction,
            priority, boarding_time, exp, money, car_image_collection, switch_direction_required,
            exp_bonus_multiplier, money_bonus_multiplier, game_time, game_time_fraction, dt_multiplier
    ):
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.priority, self.boarding_time, \
            self.exp, self.money, self.car_image_collection, self.switch_direction_required, \
            self.exp_bonus_multiplier, self.money_bonus_multiplier, self.game_time, self.game_time_fraction, \
            self.dt_multiplier \
            = cars, track, train_route, state, direction, new_direction, current_direction, \
            priority, boarding_time, exp, money, car_image_collection, switch_direction_required, \
            exp_bonus_multiplier, money_bonus_multiplier, game_time, game_time_fraction, dt_multiplier
        self.speed_state = 'move'
        self.speed_state_time = log(TRAIN_MAXIMUM_SPEED[self.map_id] + 1, TRAIN_VELOCITY_BASE)
        self.view.on_train_init(
            self.cars, self.state, self.direction, self.car_image_collection,
            self.game_time, self.game_time_fraction, self.dt_multiplier
        )

    @final
    def on_save_state(self):
        cars_position_string = None
        if len(self.cars_position) > 0:
            cars_position_string = ','.join(str(p) for p in self.cars_position)

        cars_position_abs_string = None
        if len(self.cars_position_abs) > 0:
            cars_position_abs_strings_list = []
            for i in self.cars_position_abs:
                cars_position_abs_strings_list.append(','.join(str(p) for p in i))

            cars_position_abs_string = '|'.join(cars_position_abs_strings_list)

        USER_DB_CURSOR.execute(
            '''INSERT INTO trains VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                self.map_id, self.train_id, self.cars, self.track, self.train_route, self.state, self.direction,
                self.new_direction, self.current_direction, self.speed_state, self.speed_state_time, self.priority,
                self.boarding_time, self.exp, self.money, cars_position_string, cars_position_abs_string,
                self.stop_point, self.destination_point, self.car_image_collection, self.switch_direction_required
            )
        )

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
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
            if self.cars_position[0] >= self.stop_point:
                self.on_train_move(self.stop_point - self.cars_position[0])
                self.speed_state = 'stop'
                self.speed_state_time = 0.0
            # when train needs to stop at stop point and distance is less than braking distance,
            # update state to 'decelerate'
            elif (k := get_braking_distance(self.speed_state_time) - (self.stop_point - self.cars_position[0])) >= 0:
                self.speed_state = 'decelerate'
                if k > TRAIN_MAXIMUM_SPEED[self.map_id] // 10:
                    self.speed_state_time = get_speed_state_time(
                        self.stop_point - self.cars_position[0] + 0.2, self.map_id
                    )
            # when train needs to stop at stop point and distance is more than braking distance,
            # update state to 'accelerate' if train is not at maximum speed already
            elif self.speed_state != 'move':
                self.speed_state = 'accelerate'

            # when train reaches destination point, current train route is complete,
            # update state according to previous state
            if self.cars_position[0] >= self.destination_point:
                self.on_train_move(self.destination_point - self.cars_position[0])
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
                        self.controller.parent_controller.on_announcement_add(
                            announcement_time=int(self.game_time + self.boarding_time),
                            announcement_type=DEPARTURE_ANNOUNCEMENT,
                            train_id=self.train_id, track_number=self.track
                        )
                        if self.boarding_time >= SECONDS_IN_ONE_MINUTE * 5:
                            self.controller.parent_controller.on_announcement_add(
                                announcement_time=self.game_time,
                                announcement_type=ARRIVAL_FINISHED_ANNOUNCEMENT,
                                train_id=self.train_id, track_number=self.track
                            )
                            
                        if self.boarding_time >= SECONDS_IN_ONE_MINUTE * 10:
                            self.controller.parent_controller.on_announcement_add(
                                announcement_time=int(self.game_time + self.boarding_time - SECONDS_IN_ONE_MINUTE * 5),
                                announcement_type=FIVE_MINUTES_LEFT_ANNOUNCEMENT,
                                train_id=self.train_id, track_number=self.track
                            )

                    self.view.state = self.state
                    # when boarding is started, convert trail points to 2D Cartesian
                    self.on_convert_trail_points()
                    self.trail_points_v2 = None
                # 'boarding_complete' state means train has finished entire process,
                # call on_train_lifecycle_ended() method for map controller to delete this train later
                elif self.state == 'boarding_complete':
                    self.controller.parent_controller.on_train_lifecycle_ended(self.controller)

            # update speed depending on speed state
            if self.speed_state == 'accelerate':
                if self.speed_state_time >= log(TRAIN_MAXIMUM_SPEED[self.map_id] + 1, TRAIN_VELOCITY_BASE):
                    # if train has finished acceleration, update state to 'move' (moving at maximum speed)
                    self.speed_state_time = log(TRAIN_MAXIMUM_SPEED[self.map_id] + 1, TRAIN_VELOCITY_BASE)
                    self.speed_state = 'move'
                else:
                    self.on_train_move(
                        get_distance(self.speed_state_time, self.speed_state_time + dt * self.dt_multiplier)
                    )
                    self.speed_state_time += dt * self.dt_multiplier

            elif self.speed_state == 'move':
                self.on_train_move(TRAIN_MAXIMUM_SPEED[self.map_id] * dt * self.dt_multiplier)
            # if train decelerates, continue deceleration
            elif self.speed_state == 'decelerate':
                self.on_train_move(
                    get_distance(self.speed_state_time - dt * self.dt_multiplier, self.speed_state_time)
                )
                self.speed_state_time -= dt * self.dt_multiplier

        else:
            # after half a minute left, assign exit rain route depending on new direction
            if self.boarding_time - dt * self.dt_multiplier <= SECONDS_IN_ONE_MINUTE // 2 < self.boarding_time:
                self.current_direction = self.new_direction
                self.train_route = EXIT_TRAIN_ROUTE[self.map_id][self.current_direction]
                if self.switch_direction_required:
                    self.on_switch_direction()
                    self.view.on_update_direction(self.current_direction)

                self.controller.parent_controller.on_open_train_route(
                    self.track, self.train_route, self.train_id, self.cars
                )
                self.on_reconvert_trail_points()

            self.boarding_time -= dt * self.dt_multiplier
            # after boarding time is over, update train state and add exp/money
            if self.boarding_time <= 0:
                self.state = 'boarding_complete'
                self.view.state = self.state
                self.controller.parent_controller.parent_controller.on_add_exp(self.exp)
                self.controller.parent_controller.parent_controller.on_add_money(self.money)

    @abstractmethod
    def on_set_train_start_point(self, first_car_start_point):
        pass

    @final
    def on_set_train_stop_point(self, first_car_stop_point):
        self.stop_point = first_car_stop_point

    @final
    def on_set_train_destination_point(self, first_car_destination_point):
        self.destination_point = first_car_destination_point

    @final
    def on_set_trail_points(self, trail_points_v2):
        self.trail_points_v2 = trail_points_v2

    @final
    def on_convert_trail_points(self):
        self.cars_position_abs = []
        for p in self.cars_position:
            self.cars_position_abs.append(self.trail_points_v2.get_conversion_index(p))

        self.cars_position.clear()

    @final
    def on_reconvert_trail_points(self):
        self.cars_position = []
        for p in self.cars_position_abs:
            self.cars_position.append(self.trail_points_v2.get_reconversion_index(p))

        self.cars_position_abs.clear()

    @final
    def on_switch_direction(self):
        self.switch_direction_required = FALSE
        self.cars_position_abs = list(reversed(self.cars_position_abs))
        self.view.car_position = []
        for i in self.cars_position_abs:
            self.view.car_position.append((*i, 0.0))

    @final
    def on_train_move(self, ds):
        self.view.car_position = []
        self.cars_position[0] += ds
        self.view.car_position.append(self.trail_points_v2.get_head_tail_car_position(self.cars_position[0]))
        for i in range(1, len(self.cars_position) - 1):
            self.cars_position[i] += ds
            self.view.car_position.append(self.trail_points_v2.get_mid_car_position(self.cars_position[i]))

        self.cars_position[-1] += ds
        self.view.car_position.append(self.trail_points_v2.get_head_tail_car_position(self.cars_position[-1]))
        self.controller.parent_controller.on_update_train_route_sections(
            self.track, self.train_route, self.cars_position[-1]
        )
