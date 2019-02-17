from logging import getLogger

from model import *


class TrainModel(Model):
    """
    Implements Train model.
    Train object is responsible for properties, UI and events related to the train.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor, train_id):
        """
        Properties:
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

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param train_id:                        train identification number
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger(f'root.app.game.map.train.{train_id}.model'))
        self.logger.info('START INIT')
        self.train_maximum_speed = TRAIN_ACCELERATION_FACTOR[-1] - TRAIN_ACCELERATION_FACTOR[-2]
        self.logger.debug(f'train_maximum_speed: {self.train_maximum_speed}')
        self.speed_factor_position_limit = len(TRAIN_ACCELERATION_FACTOR) - 1
        self.logger.debug(f'speed_factor_position_limit: {self.speed_factor_position_limit}')
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
        self.logger.info('END INIT')

    def on_train_setup(self, train_id):
        """
        This method is used when train is created from saved database entry when user launches the game.

        :param train_id:                        train identification number
        """
        self.logger.info('START ON_TRAIN_SETUP')
        self.user_db_cursor.execute('''SELECT * FROM trains WHERE train_id = ?''', (train_id, ))
        train_id, self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.speed, self.speed_state, self.speed_factor_position, self.priority, \
            self.boarding_time, self.exp, self.money, cars_position_parsed, cars_position_abs_parsed, \
            self.stop_point, self.destination_point, self.car_image_collection \
            = self.user_db_cursor.fetchone()
        self.logger.debug(f'cars: {self.cars}')
        self.logger.debug(f'track: {self.track}')
        self.logger.debug(f'train_route: {self.train_route}')
        self.logger.debug(f'state: {self.state}')
        self.logger.debug(f'direction: {self.direction}')
        self.logger.debug(f'new_direction: {self.new_direction}')
        self.logger.debug(f'current_direction: {self.current_direction}')
        self.logger.debug(f'speed: {self.speed}')
        self.logger.debug(f'speed_state: {self.speed_state}')
        self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')
        self.logger.debug(f'priority: {self.priority}')
        self.logger.debug(f'boarding_time: {self.boarding_time}')
        self.logger.debug(f'exp: {self.exp}')
        self.logger.debug(f'money: {self.money}')
        self.logger.debug(f'stop_point: {self.stop_point}')
        self.logger.debug(f'destination_point: {self.destination_point}')
        self.logger.debug(f'car_image_collection: {self.car_image_collection}')
        if cars_position_parsed is not None:
            cars_position_parsed = cars_position_parsed.split(',')
            for i in range(len(cars_position_parsed)):
                cars_position_parsed[i] = int(cars_position_parsed[i])

            self.cars_position = cars_position_parsed

        self.logger.debug(f'cars_position: {self.cars_position}')
        if cars_position_abs_parsed is not None:
            cars_position_abs_parsed = cars_position_abs_parsed.split('|')
            for i in range(len(cars_position_abs_parsed)):
                cars_position_abs_parsed[i] = cars_position_abs_parsed[i].split(',')
                cars_position_abs_parsed[i][0] = int(cars_position_abs_parsed[i][0])
                cars_position_abs_parsed[i][1] = int(cars_position_abs_parsed[i][1])

            self.cars_position_abs = cars_position_abs_parsed

        self.logger.debug(f'cars_position_abs: {self.cars_position_abs}')
        self.logger.info('END ON_TRAIN_SETUP')

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
        self.logger.info('START ON_TRAIN_INIT')
        self.cars, self.track, self.train_route, self.state, self.direction, self.new_direction, \
            self.current_direction, self.priority, self.boarding_time, \
            self.exp, self.money, self.car_image_collection \
            = cars, track, train_route, state, direction, new_direction, current_direction, \
            priority, boarding_time, exp, money, car_image_collection
        self.logger.debug(f'cars: {self.cars}')
        self.logger.debug(f'track: {self.track}')
        self.logger.debug(f'train_route: {self.train_route}')
        self.logger.debug(f'state: {self.state}')
        self.logger.debug(f'direction: {self.direction}')
        self.logger.debug(f'new_direction: {self.new_direction}')
        self.logger.debug(f'current_direction: {self.current_direction}')
        self.logger.debug(f'priority: {self.priority}')
        self.logger.debug(f'boarding_time: {self.boarding_time}')
        self.logger.debug(f'exp: {self.exp}')
        self.logger.debug(f'money: {self.money}')
        self.logger.debug(f'car_image_collection: {self.car_image_collection}')
        self.speed = self.train_maximum_speed
        self.speed_state = 'move'
        self.speed_factor_position = self.speed_factor_position_limit
        self.logger.debug(f'speed: {self.speed}')
        self.logger.debug(f'speed_state: {self.speed_state}')
        self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')
        self.logger.info('END ON_TRAIN_INIT')

    def on_set_train_start_point(self, first_car_start_point):
        """
        Updates train initial position on train route.

        :param first_car_start_point:           data
        """
        self.logger.info('START ON_SET_TRAIN_START_POINT')
        self.cars_position = []
        for i in range(self.cars):
            self.cars_position.append(first_car_start_point - i * CAR_LENGTH)

        self.logger.info('END ON_SET_TRAIN_START_POINT')

    def on_set_train_stop_point(self, first_car_stop_point):
        """
        Updates the trail point where to stop the train if signal is at danger.

        :param first_car_stop_point:            data
        """
        self.logger.info('START ON_SET_TRAIN_STOP_POINT')
        self.stop_point = first_car_stop_point
        self.logger.debug(f'stop_point: {self.stop_point}')
        self.logger.info('END ON_SET_TRAIN_STOP_POINT')

    def on_set_train_destination_point(self, first_car_destination_point):
        """
        Updates the trail point destination point.
        When train reaches destination point, route is completed.

        :param first_car_destination_point:     data
        """
        self.logger.info('START ON_SET_TRAIN_DESTINATION_POINT')
        self.destination_point = first_car_destination_point
        self.logger.debug(f'destination_point: {self.destination_point}')
        self.logger.info('END ON_SET_TRAIN_DESTINATION_POINT')

    def on_set_trail_points(self, trail_points_v2):
        """
        Updates trail points.

        :param trail_points_v2:                 data
        """
        self.logger.info('START ON_SET_TRAIL_POINTS')
        self.trail_points_v2 = trail_points_v2
        self.logger.debug(f'trail_points_v2: {self.trail_points_v2}')
        self.logger.info('END ON_SET_TRAIL_POINTS')

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.on_activate_view()
        self.logger.info('END ON_ACTIVATE')

    def on_activate_view(self):
        """
        Updates car positions, direction, image collection ID, state and activates the view.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        car_position_view = []
        if len(self.cars_position) > 0:
            for i in self.cars_position:
                car_position_view.append(self.trail_points_v2[i])
        else:
            for i in self.cars_position_abs:
                car_position_view.append((i[0], i[1], 0.0))

        self.logger.debug(f'car_position_view: {car_position_view}')
        self.view.on_update_car_position(car_position_view)
        self.logger.debug(f'current_direction: {self.current_direction}')
        self.view.on_update_direction(self.current_direction)
        self.logger.debug(f'car_image_collection: {self.car_image_collection}')
        self.view.on_update_car_image_collection(self.car_image_collection)
        self.logger.debug(f'state: {self.state}')
        self.view.on_update_state(self.state)
        self.view.on_activate()
        self.logger.info('END ON_ACTIVATE_VIEW')

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_save_state(self):
        """
        Saves train state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        self.logger.debug(f'cars_position: {self.cars_position}')
        cars_position_string = None
        if len(self.cars_position) > 0:
            cars_position_string = ''
            for i in self.cars_position:
                cars_position_string += f'{i},'

            cars_position_string = cars_position_string[0:len(cars_position_string) - 1]

        self.logger.debug(f'cars_position_string: {cars_position_string}')
        self.logger.debug(f'cars_position_abs: {self.cars_position_abs}')
        cars_position_abs_string = None
        if len(self.cars_position_abs) > 0:
            cars_position_abs_string = ''
            for i in self.cars_position_abs:
                cars_position_abs_string += f'{i[0]},{i[1]}|'

            cars_position_abs_string = cars_position_abs_string[0:len(cars_position_abs_string) - 1]

        self.logger.debug(f'cars_position_abs_string: {cars_position_abs_string}')
        self.logger.debug(f'train_id: {self.controller.train_id}')
        self.logger.debug(f'cars: {self.cars}')
        self.logger.debug(f'track: {self.track}')
        self.logger.debug(f'train_route: {self.train_route}')
        self.logger.debug(f'state: {self.state}')
        self.logger.debug(f'direction: {self.direction}')
        self.logger.debug(f'new_direction: {self.new_direction}')
        self.logger.debug(f'current_direction: {self.current_direction}')
        self.logger.debug(f'speed: {self.speed}')
        self.logger.debug(f'speed_state: {self.speed_state}')
        self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')
        self.logger.debug(f'priority: {self.priority}')
        self.logger.debug(f'boarding_time: {self.boarding_time}')
        self.logger.debug(f'exp: {self.exp}')
        self.logger.debug(f'money: {self.money}')
        self.logger.debug(f'stop_point: {self.stop_point}')
        self.logger.debug(f'destination_point: {self.destination_point}')
        self.logger.debug(f'car_image_collection: {self.car_image_collection}')
        self.user_db_cursor.execute('''INSERT INTO trains VALUES 
                                       (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                    (self.controller.train_id, self.cars, self.track, self.train_route, self.state,
                                     self.direction, self.new_direction, self.current_direction, self.speed,
                                     self.speed_state, self.speed_factor_position, self.priority, self.boarding_time,
                                     self.exp, self.money, cars_position_string, cars_position_abs_string,
                                     self.stop_point, self.destination_point, self.car_image_collection))
        self.logger.debug('train info saved successfully')
        self.logger.info('END ON_SAVE_STATE')

    def on_update_time(self, game_time):
        """
        Updates train properties every frame, including speed, state, priority, etc.

        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TIME')
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

        self.logger.debug(f'state: {self.state}')
        if self.state not in ('boarding_in_progress', 'boarding_in_progress_pass_through'):
            # update speed and speed state
            # when train reaches stop point, update state to 'stop', speed and speed_factor_position to 0
            self.logger.debug(f'first car position: {self.cars_position[0]}')
            self.logger.debug(f'stop_point: {self.stop_point}')
            self.logger.debug('acceleration factor at speed_factor_position: {}'
                              .format(TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]))
            if self.cars_position[0] == self.stop_point:
                self.speed_state = 'stop'
                self.logger.debug(f'speed_state: {self.speed_state}')
                self.speed = 0
                self.logger.debug(f'speed: {self.speed}')
                self.speed_factor_position = 0
                self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')
            # when train needs to stop at stop point and distance is less than braking distance,
            # update state to 'decelerate'
            elif self.stop_point - self.cars_position[0] <= TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]:
                self.speed_state = 'decelerate'
                self.logger.debug(f'speed_state: {self.speed_state}')
            # when train needs to stop at stop point and distance is more than braking distance,
            # update state to 'accelerate' if train is not at maximum speed already
            else:
                if self.speed_state != 'move':
                    self.speed_state = 'accelerate'

                self.logger.debug(f'speed_state: {self.speed_state}')

            # when train reaches destination point, current train route is complete,
            # update state according to previous state
            self.logger.debug(f'first car position: {self.cars_position[0]}')
            self.logger.debug(f'destination_point: {self.destination_point}')
            if self.cars_position[0] == self.destination_point:
                self.logger.debug(f'state: {self.state}')
                # approaching routes are closed by dispatcher, other routes can be closed here
                if self.state not in ('approaching', 'approaching_pass_through'):
                    self.controller.parent_controller.on_close_train_route(self.track, self.train_route)

                # 'pending_boarding' state means train arrives for boarding, start boarding
                if self.state == 'pending_boarding':
                    self.priority = 0
                    self.logger.debug(f'priority: {self.priority}')
                    self.logger.debug(f'track: {self.track}')
                    if self.track in (1, 2):
                        self.state = 'boarding_in_progress_pass_through'
                    else:
                        self.state = 'boarding_in_progress'

                    self.logger.debug(f'state: {self.state}')
                    self.view.on_update_state(self.state)
                    # when boarding is started, convert trail points to 2D Cartesian
                    self.on_convert_trail_points()
                    self.trail_points_v2 = None
                    self.logger.debug(f'trail_points_v2: {self.trail_points_v2}')
                # 'boarding_complete' state means train has finished entire process,
                # update state to 'successful_departure' to delete this train later
                elif self.state == 'boarding_complete':
                    self.state = 'successful_departure'
                    self.logger.debug(f'state: {self.state}')

            # update speed depending on speed state
            self.logger.debug(f'speed_state: {self.speed_state}')
            if self.speed_state == 'accelerate':
                self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')
                self.logger.debug(f'speed_factor_position_limit: {self.speed_factor_position_limit}')
                # if train has finished acceleration, update state to 'move' (moving at maximum speed)
                if self.speed_factor_position == self.speed_factor_position_limit:
                    self.speed_state = 'move'
                    self.logger.debug(f'speed_state: {self.speed_state}')
                    self.speed = self.train_maximum_speed
                    self.logger.debug(f'speed: {self.speed}')
                # if not, continue acceleration
                else:
                    self.speed = TRAIN_ACCELERATION_FACTOR[self.speed_factor_position + 1] \
                               - TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]
                    self.logger.debug(f'speed: {self.speed}')
                    self.speed_factor_position += 1
                    self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')

            # if train decelerates, continue deceleration
            if self.speed_state == 'decelerate':
                self.speed_factor_position -= 1
                self.logger.debug(f'speed_factor_position: {self.speed_factor_position}')
                self.speed = TRAIN_ACCELERATION_FACTOR[self.speed_factor_position + 1] \
                           - TRAIN_ACCELERATION_FACTOR[self.speed_factor_position]
                self.logger.debug(f'speed: {self.speed}')

            # if train is not stopped, move all cars ahead
            if self.speed_state != 'stop':
                self.logger.debug(f'cars_position: {self.cars_position}')
                car_position_view = []
                for i in range(len(self.cars_position)):
                    self.cars_position[i] += self.speed
                    car_position_view.append(self.trail_points_v2[self.cars_position[i]])

                self.logger.debug(f'cars_position: {self.cars_position}')
                self.logger.debug(f'car_position_view: {car_position_view}')
                self.view.on_update_car_position(car_position_view)
                self.controller.parent_controller\
                    .on_update_train_route_sections(self.track, self.train_route, self.cars_position[-1])
        else:
            # if boarding is in progress, decrease boarding time
            self.logger.debug(f'boarding_time: {self.boarding_time}')
            self.boarding_time -= 1
            self.logger.debug(f'boarding_time: {self.boarding_time}')
            # after one minute left, assign exit rain route depending on new direction
            if self.boarding_time == FRAMES_IN_ONE_MINUTE:
                self.current_direction = self.new_direction
                self.logger.debug(f'current_direction: {self.current_direction}')
                self.train_route = EXIT_TRAIN_ROUTE[self.current_direction]
                self.logger.debug(f'train_route: {self.train_route}')
                self.logger.debug(f'direction: {self.direction}')
                self.logger.debug(f'new_direction: {self.new_direction}')
                if self.direction % 2 != self.new_direction % 2:
                    self.on_switch_direction()

                self.controller.parent_controller.on_open_train_route(self.track, self.train_route,
                                                                      self.controller.train_id, self.cars)
                self.on_reconvert_trail_points()

            # after boarding time is over, update train state and add exp
            if self.boarding_time == 0:
                self.state = 'boarding_complete'
                self.logger.debug(f'state: {self.state}')
                self.view.on_update_state(self.state)
                self.controller.parent_controller.parent_controller.on_add_exp(self.exp)
                self.controller.parent_controller.parent_controller.on_add_money(self.money)

        self.logger.info('END ON_UPDATE_TIME')

    def on_convert_trail_points(self):
        """
        Converts relative route trail points to 2D Cartesian positions.
        """
        self.logger.info('START ON_CONVERT_TRAIL_POINTS')
        self.cars_position_abs = []
        for i in self.cars_position:
            dot = self.trail_points_v2[i]
            self.logger.debug(f'dot: {dot}')
            self.cars_position_abs.append([dot[0], dot[1]])
            self.logger.debug(f'cars_position_abs: {self.cars_position_abs}')

        self.cars_position.clear()
        self.logger.debug(f'cars_position: {self.cars_position}')
        self.logger.info('END ON_CONVERT_TRAIL_POINTS')

    def on_reconvert_trail_points(self):
        """
        Converts 2D Cartesian car positions to relative route trail points.
        """
        self.logger.info('START ON_RECONVERT_TRAIL_POINTS')
        self.cars_position = []
        self.logger.debug(f'first trail point X: {self.trail_points_v2[0][0]}')
        for i in self.cars_position_abs:
            self.logger.debug(f'absolute X position: {i[0]}')
            self.cars_position.append(abs(i[0] - self.trail_points_v2[0][0]))
            self.logger.debug(f'cars_position: {self.cars_position}')

        self.cars_position_abs.clear()
        self.logger.debug(f'cars_position_abs: {self.cars_position_abs}')
        self.logger.info('END ON_RECONVERT_TRAIL_POINTS')

    def on_switch_direction(self):
        """
        Reverts cars order.
        """
        self.logger.info('START ON_SWITCH_DIRECTION')
        self.logger.debug(f'cars_position_abs: {self.cars_position_abs}')
        self.cars_position_abs = list(reversed(self.cars_position_abs))
        self.logger.debug(f'cars_position_abs: {self.cars_position_abs}')
        self.logger.info('END ON_SWITCH_DIRECTION')
