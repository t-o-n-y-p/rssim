from logging import getLogger

from controller import *


class TrainController(Controller):
    """
    Implements Train controller.
    Train object is responsible for properties, UI and events related to the train.
    """
    def __init__(self, map_controller, train_id):
        """
        Properties:
            train_id                            train identification number

        :param map_controller:                  Map controller (parent controller)
        :param train_id:                        train identification number
        """
        super().__init__(parent_controller=map_controller,
                         logger=getLogger(f'root.app.game.map.train.{train_id}.controller'))
        self.logger.info('START INIT')
        self.train_id = train_id
        self.logger.debug(f'train_id: {self.train_id}')
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view to create car sprites if they are inside game window and delete if they are not.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Train object: controller and model. Model activates the view if necessary.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Train object: controller, view and model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    def on_save_state(self):
        """
        Notifies the model to save train state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        self.model.on_save_state()
        self.logger.info('END ON_SAVE_STATE')

    def on_update_time(self, game_time):
        """
        Notifies the model about in-game time update.

        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TIME')
        self.model.on_update_time(game_time)
        self.logger.info('END ON_UPDATE_TIME')

    def on_change_base_offset(self, new_base_offset):
        """
        Notifies the view about base offset update.

        :param new_base_offset:         new base offset
        """
        self.logger.info('START ON_CHANGE_BASE_OFFSET')
        self.view.on_change_base_offset(new_base_offset)
        self.logger.info('END ON_CHANGE_BASE_OFFSET')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.view.on_change_screen_resolution(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_zoom_in(self):
        """
        Notifies the view to zoom in all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.
        """
        self.logger.info('START ON_ZOOM_IN')
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)
        self.logger.info('END ON_ZOOM_IN')

    def on_zoom_out(self):
        """
        Notifies the view to zoom out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.
        """
        self.logger.info('START ON_ZOOM_OUT')
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)
        self.logger.info('END ON_ZOOM_OUT')

    def on_activate_view(self):
        """
        Activates the view if user opened game screen in the app.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.model.on_activate_view()
        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_deactivate_view(self):
        """
        Deactivates the view if user either closed game screen or opened settings screen.
        """
        self.logger.info('START ON_DEACTIVATE_VIEW')
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE_VIEW')

    def on_set_train_start_point(self, first_car_start_point):
        """
        Notifies the model about initial position update.

        :param first_car_start_point:           data
        """
        self.logger.info('START ON_SET_TRAIN_START_POINT')
        self.model.on_set_train_start_point(first_car_start_point)
        self.logger.info('END ON_SET_TRAIN_START_POINT')

    def on_set_train_stop_point(self, first_car_stop_point):
        """
        Notifies the model where to stop the train if signal is at danger.

        :param first_car_stop_point:            data
        """
        self.logger.info('START ON_SET_TRAIN_STOP_POINT')
        self.model.on_set_train_stop_point(first_car_stop_point)
        self.logger.info('END ON_SET_TRAIN_STOP_POINT')

    def on_set_train_destination_point(self, first_car_destination_point):
        """
        Notifies the model about destination point update.
        When train reaches destination point, route is completed.

        :param first_car_destination_point:     data
        """
        self.logger.info('START ON_SET_TRAIN_DESTINATION_POINT')
        self.model.on_set_train_destination_point(first_car_destination_point)
        self.logger.info('END ON_SET_TRAIN_DESTINATION_POINT')

    def on_set_trail_points(self, trail_points_v2):
        """
        Notifies the model about trail points update.

        :param trail_points_v2:                 data
        """
        self.logger.info('START ON_SET_TRAIL_POINTS')
        self.model.on_set_trail_points(trail_points_v2)
        self.logger.info('END ON_SET_TRAIL_POINTS')
