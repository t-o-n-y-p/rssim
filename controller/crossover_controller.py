from logging import getLogger

from controller import *


class CrossoverController(Controller):
    """
    Implements Crossover controller.
    Crossover object is responsible for properties, UI and events related to the crossover.
    """
    def __init__(self, map_controller, track_param_1, track_param_2, crossover_type):
        """
        Properties:
            track_param_1               number of the first track of two being connected by the crossover
            track_param_2               number of the second track of two being connected by the crossover
            crossover_type              crossover location: left/right side of the map

        :param map_controller:          Map controller (parent controller)
        :param track_param_1:           number of the first track of two being connected by the crossover
        :param track_param_2:           number of the second track of two being connected by the crossover
        :param crossover_type:          crossover location: left/right side of the map
        """
        super().__init__(
            parent_controller=map_controller,
            logger=getLogger(
                f'root.app.game.map.crossover.{track_param_1}.{track_param_2}.{crossover_type}.controller'
            )
        )
        self.logger.info('START INIT')
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.crossover_type = crossover_type
        self.logger.debug(f'crossover params: {self.track_param_1} {self.track_param_2} {self.crossover_type}')
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
        Activates Crossover object: controller and model.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Crossover object: controller, view and model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

    def on_save_state(self):
        """
        Notifies the model to save crossover state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        self.model.on_save_state()
        self.logger.info('END ON_SAVE_STATE')

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
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)
        self.logger.info('END ON_ZOOM_IN')

    def on_zoom_out(self):
        """
        Notifies the view to zoom out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.
        """
        self.logger.info('START ON_ZOOM_OUT')
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)
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

    def on_force_busy_on(self, positions, train_id):
        """
        Notifies model the train is approaching.

        :param positions:               direction the train is about to proceed to
        :param train_id:                ID of the train which is about to pass through the crossover
        """
        self.logger.info('START ON_FORCE_BUSY_ON')
        self.model.on_force_busy_on(positions, train_id)
        self.logger.info('END ON_FORCE_BUSY_ON')

    def on_force_busy_off(self, positions):
        """
        Notifies model the train has passed the crossover.

        :param positions:               direction that was previously locked for train
        """
        self.logger.info('START ON_FORCE_BUSY_OFF')
        self.model.on_force_busy_off(positions)
        self.logger.info('END ON_FORCE_BUSY_OFF')
