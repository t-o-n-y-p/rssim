from logging import getLogger

from controller import *


class DispatcherController(Controller):
    """
    Implements Dispatcher controller.
    Dispatcher object is responsible for assigning routes to approaching trains.
    """
    def __init__(self, map_controller):
        """
        :param map_controller:          Map controller (parent controller)
        """
        super().__init__(parent_controller=map_controller,
                         logger=getLogger('root.app.game.map.dispatcher.controller'))
        self.logger.info('START INIT')
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
        Activates Dispatcher object: controller and model. Model activates the view if necessary.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Dispatcher object: controller, view and model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    def on_save_state(self):
        """
        Notifies the model to save dispatcher state to user progress database.
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

    def on_add_train(self, train_controller):
        """
        Adds approaching train to the dispatcher.
        After train is created, it needs to be dispatched to the most suitable track.

        :param train_controller:        controller of the train to be added
        """
        self.logger.info('START ON_ADD_TRAIN')
        self.model.on_add_train(train_controller)
        self.logger.info('END ON_ADD_TRAIN')

    def on_leave_track(self, track):
        """
        Notifies the model the track is clear for any of the next trains.

        :param track:                   track number
        """
        self.logger.info('START ON_LEAVE_TRACK')
        self.model.on_leave_track(track)
        self.logger.info('END ON_LEAVE_TRACK')

    def on_unlock_track(self, track):
        """
        Notifies the model the track is unlocked and now available for any of the next trains.

        :param track:                   track number
        """
        self.logger.info('START ON_UNLOCK_TRACK')
        self.model.on_unlock_track(track)
        self.logger.info('END ON_UNLOCK_TRACK')
