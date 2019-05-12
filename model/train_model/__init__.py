from logging import getLogger

from model import *


class TrainModel(Model):
    """
    Implements Train model.
    Train object is responsible for properties, UI and events related to the train.
    """
    def __init__(self, map_id, train_id):
        """
        Properties:
            map_id                              ID of the map which this train belongs to
            train_maximum_speed                 maximum speed the train can achieve
            speed_factor_position_limit         maximum position on acceleration chart
            cars                                number of cars in the train
            track                               track number (0 for regular entry and 100 for side entry)
            train_route                         train route type (left/right approaching or side_approaching)
            state                               train state: approaching or approaching_pass_through
            direction                           train arrival direction
            new_direction                       train departure direction
            current_direction                   train current direction
            speed                               current train speed
            speed_state                         indicates if train accelerates, decelerates, just moves or is still
            speed_factor_position               acceleration chart position
            priority                            train priority in the queue
            boarding_time                       amount of boarding time left for this train
            exp                                 exp gained when boarding finishes
            money                               money gained when boarding finishes
            cars_position                       list of trail point ID for each car (empty if boarding is in progress)
            cars_position_abs                   list of 2D Cartesian positions for each car
                                                (used when boarding is in progress)
            stop_point                          indicates where to stop the train if signal is at danger
            destination_point                   when train reaches destination point, route is completed
            trail_points_v2                     list of train route trail points in 2D Cartesian coordinates
                                                plus rotation angle
            car_image_collection                number of car collection used for this train

        :param map_id:                          ID of the map which this train belongs to
        :param train_id:                        train identification number
        """
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.train.{train_id}.model'))
        self.map_id = map_id
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
        self.trail_points_v2 = []
        self.car_image_collection = 0

    def on_train_setup(self, train_id):
        """
        This method is used when train is created from saved database entry when user launches the game.

        :param train_id:                        train identification number
        """
        self.user_db_cursor.execute('''SELECT train_id, cars, train_route_track_number, train_route_type, 
                                       state, direction, new_direction, current_direction, speed, speed_state, 
                                       speed_factor_position, priority, boarding_time, exp, money, 
                                       cars_position, cars_position_abs, stop_point, destination_point, 
                                       car_image_collection FROM trains WHERE train_id = ? AND map_id = ?''',
                                    (train_id, self.map_id))
        train_id, self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.speed_factor_position, self.priority, \
            self.boarding_time, self.exp, self.money, cars_position_parsed, cars_position_abs_parsed, \
            self.stop_point, self.destination_point, self.car_image_collection \
            = self.user_db_cursor.fetchone()
        if cars_position_parsed is not None:
            self.cars_position = list(map(int, cars_position_parsed.split(',')))

        if cars_position_abs_parsed is not None:
            cars_position_abs_parsed = cars_position_abs_parsed.split('|')
            for i in range(len(cars_position_abs_parsed)):
                cars_position_abs_parsed[i] = list(map(int, cars_position_abs_parsed[i].split(',')))

            self.cars_position_abs = cars_position_abs_parsed

    def on_train_init(self, cars, track, train_route, state, direction, new_direction, current_direction,
                      priority, boarding_time, exp, money, car_image_collection):
        """
        This method is used when train is created from schedule during the game.

        :param cars:                            number of cars in the train
        :param track:                           track number (0 for regular entry and 100 for side entry)
        :param train_route:                     train route type (left/right approaching or side_approaching)
        :param state:                           train state: approaching or approaching_pass_through
        :param direction:                       train arrival direction
        :param new_direction:                   train departure direction
        :param current_direction:               train current direction
        :param priority:                        train priority in the queue
        :param boarding_time:                   amount of boarding time left for this train
        :param exp:                             exp gained when boarding finishes
        :param money:                           money gained when boarding finishes
        :param car_image_collection:            number of car collection used for this train
        """
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.priority, self.boarding_time, \
            self.exp, self.money, self.car_image_collection \
            = cars, track, train_route, state, direction, new_direction, current_direction, \
            priority, boarding_time, exp, money, car_image_collection
        self.speed = self.train_maximum_speed
        self.speed_state = 'move'
        self.speed_factor_position = self.speed_factor_position_limit

    def on_set_train_start_point(self, first_car_start_point):
        """
        Updates train initial position on train route.

        :param first_car_start_point:           data
        """
        pass

    def on_set_train_stop_point(self, first_car_stop_point):
        """
        Updates the trail point where to stop the train if signal is at danger.

        :param first_car_stop_point:            data
        """
        self.stop_point = first_car_stop_point

    def on_set_train_destination_point(self, first_car_destination_point):
        """
        Updates the trail point destination point.
        When train reaches destination point, route is completed.

        :param first_car_destination_point:     data
        """
        self.destination_point = first_car_destination_point

    def on_set_trail_points(self, trail_points_v2):
        """
        Updates trail points.

        :param trail_points_v2:                 data
        """
        self.trail_points_v2 = trail_points_v2

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True

    def on_activate_view(self):
        """
        Updates car positions, direction, image collection ID, state and activates the view.
        """
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
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_save_state(self):
        """
        Saves train state to user progress database.
        """
        cars_position_string = None
        if len(self.cars_position) > 0:
            cars_position_string = ','.join(list(map(str, self.cars_position)))

        cars_position_abs_strings_list = []
        cars_position_abs_string = None
        if len(self.cars_position_abs) > 0:
            for i in self.cars_position_abs:
                cars_position_abs_strings_list.append(','.join(list(map(str, i))))

            cars_position_abs_string = '|'.join(list(map(str, cars_position_abs_strings_list)))

        self.user_db_cursor.execute('''INSERT INTO trains VALUES 
                                       (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (self.map_id, self.controller.train_id, self.cars, self.track, self.train_route,
                                     self.state, self.direction, self.new_direction, self.current_direction, self.speed,
                                     self.speed_state, self.speed_factor_position, self.priority, self.boarding_time,
                                     self.exp, self.money, cars_position_string, cars_position_abs_string,
                                     self.stop_point, self.destination_point, self.car_image_collection))

    def on_update_time(self, game_time):
        """
        Updates train properties every frame, including speed, state, priority, etc.

        :param game_time:               current in-game time
        """
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
            if self.cars_position[0] == self.stop_point:
                self.speed_state = 'stop'
                self.speed = 0
                self.speed_factor_position = 0
            # when train needs to stop at stop point and distance is less than braking distance,
            # update state to 'decelerate'
            elif self.stop_point - self.cars_position[0] \
                    <= PASSENGER_TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]:
                self.speed_state = 'decelerate'
            # when train needs to stop at stop point and distance is more than braking distance,
            # update state to 'accelerate' if train is not at maximum speed already
            else:
                if self.speed_state != 'move':
                    self.speed_state = 'accelerate'

            # when train reaches destination point, current train route is complete,
            # update state according to previous state
            if self.cars_position[0] == self.destination_point:
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
                    self.trail_points_v2 = None
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
                    self.speed = PASSENGER_TRAIN_ACCELERATION_FACTOR[self.speed_factor_position + 1] \
                                 - PASSENGER_TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]
                    self.speed_factor_position += 1

            # if train decelerates, continue deceleration
            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.speed = PASSENGER_TRAIN_ACCELERATION_FACTOR[self.speed_factor_position + 1] \
                             - PASSENGER_TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]

            # if train is not stopped, move all cars ahead
            if self.speed_state != 'stop':
                car_position_view = []
                for i in range(len(self.cars_position)):
                    self.cars_position[i] += self.speed
                    car_position_view.append(self.trail_points_v2[self.cars_position[i]])

                self.view.on_update_car_position(car_position_view)
                self.controller.parent_controller\
                    .on_update_train_route_sections(self.track, self.train_route, self.cars_position[-1])
        else:
            # if boarding is in progress, decrease boarding time
            self.boarding_time -= 1
            # after one minute left, assign exit rain route depending on new direction
            if self.boarding_time == FRAMES_IN_ONE_MINUTE:
                self.current_direction = self.new_direction
                self.train_route = EXIT_TRAIN_ROUTE[self.current_direction]
                if self.direction % 2 != self.new_direction % 2:
                    self.on_switch_direction()

                self.controller.parent_controller.on_open_train_route(self.track, self.train_route,
                                                                      self.controller.train_id, self.cars)
                self.on_reconvert_trail_points()

            # after boarding time is over, update train state and add exp
            if self.boarding_time == 0:
                self.state = 'boarding_complete'
                self.view.on_update_state(self.state)
                self.controller.parent_controller.parent_controller.on_add_exp(self.exp)
                self.controller.parent_controller.parent_controller.on_add_money(self.money)

    def on_convert_trail_points(self):
        """
        Converts relative route trail points to 2D Cartesian positions.
        """
        self.cars_position_abs = []
        for i in self.cars_position:
            dot = self.trail_points_v2[i]
            self.cars_position_abs.append([dot[0], dot[1]])

        self.cars_position.clear()

    def on_reconvert_trail_points(self):
        """
        Converts 2D Cartesian car positions to relative route trail points.
        """
        self.cars_position = []
        for i in self.cars_position_abs:
            self.cars_position.append(abs(i[0] - self.trail_points_v2[0][0]))

        self.cars_position_abs.clear()

    def on_switch_direction(self):
        """
        Reverts cars order.
        """
        self.cars_position_abs = list(reversed(self.cars_position_abs))
