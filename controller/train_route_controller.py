from logging import getLogger

from controller import *


class TrainRouteController(Controller):
    """
    Implements Train route controller.
    Train route object is responsible for properties, UI and events related to the train route.
    """
    def __init__(self, map_controller, track, train_route):
        """
        Properties:
            track                               route track number
            train_route                         route type (e.g. left/right entry/exit)

        :param map_controller:                  Map controller (parent controller)
        :param track:                           route track number
        :param train_route:                     route type (e.g. left/right entry/exit)
        """
        super().__init__(parent_controller=map_controller,
                         logger=getLogger(f'root.app.game.map.train_route.{track}.{train_route}.controller'))
        self.logger.info('START INIT')
        self.track = track
        self.logger.debug(f'track: {self.track}')
        self.train_route = train_route
        self.logger.debug(f'train_route: {self.train_route}')
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Train route object: controller and model. Model activates the view if necessary.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Train route object: controller, view and model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    def on_save_state(self):
        """
        Notifies the model to save train route state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        self.model.on_save_state()
        self.logger.info('END ON_SAVE_STATE')

    def on_open_train_route(self, train_id, cars):
        """
        Notifies the model to open train route.

        :param train_id:                        ID of the train which opens the train route
        :param cars:                            number of cars in the train
        """
        self.logger.info('START ON_OPEN_TRAIN_ROUTE')
        self.model.on_open_train_route(train_id, cars)
        self.logger.info('END ON_OPEN_TRAIN_ROUTE')

    def on_close_train_route(self):
        """
        Notifies the model to close train route.
        """
        self.logger.info('START ON_CLOSE_TRAIN_ROUTE')
        self.model.on_close_train_route()
        self.logger.info('END ON_CLOSE_TRAIN_ROUTE')

    def on_update_train_route_sections(self, last_car_position):
        """
        Notifies the model about last train car position update.

        :param last_car_position:               train last car position on the route
        """
        self.logger.info('START ON_UPDATE_TRAIN_ROUTE_SECTIONS')
        self.model.on_update_train_route_sections(last_car_position)
        self.logger.info('END ON_UPDATE_TRAIN_ROUTE_SECTIONS')

    def on_update_time(self, game_time):
        """
        Notifies the model about in-game time update.

        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TIME')
        self.model.on_update_time(game_time)
        self.logger.info('END ON_UPDATE_TIME')

    def on_update_priority(self, priority):
        """
        Notifies the model about priority update.

        :param priority:                        new priority value
        """
        self.logger.info('START ON_UPDATE_PRIORITY')
        self.model.on_update_priority(priority)
        self.logger.info('END ON_UPDATE_PRIORITY')

    def on_update_section_status(self, section, status):
        """
        Notifies the model about particular section status update.

        :param section:                         train route section number
        :param status:                          new status
        """
        self.logger.info('START ON_UPDATE_SECTION_STATUS')
        self.model.on_update_section_status(section, status)
        self.logger.info('END ON_UPDATE_SECTION_STATUS')

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
