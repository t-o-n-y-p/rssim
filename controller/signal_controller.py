from logging import getLogger

from controller import *


class SignalController(Controller):
    """
    Implements Signal controller.
    Signal object is responsible for properties, UI and events related to the signal state.
    """
    def __init__(self, map_controller, track, base_route):
        """
        Properties:
            track                               signal track number
            base_route                          base route (train route part) which signal belongs to

        :param map_controller:                  Map controller (parent controller)
        :param track:                           signal track number
        :param base_route:                      base route (train route part) which signal belongs to
        """
        super().__init__(parent_controller=map_controller,
                         logger=getLogger(f'root.app.game.map.signal.{track}.{base_route}.controller'))
        self.logger.info('START INIT')
        self.track = track
        self.logger.debug(f'track: {self.track}')
        self.base_route = base_route
        self.logger.debug(f'base_route: {self.base_route}')
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
        Activates Signal object: controller and model. Model activates the view if necessary.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Signal object: controller, view and model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.logger.info('END ON_DEACTIVATE')

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

    def on_unlock(self):
        """
        Notifies model the signal was unlocked.
        """
        self.logger.info('START ON_UNLOCK')
        self.model.on_unlock()
        self.logger.info('END ON_UNLOCK')

    def on_save_state(self):
        """
        Notifies the model to save signal state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        self.model.on_save_state()
        self.logger.info('END ON_SAVE_STATE')

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

    def on_switch_to_green(self):
        """
        Notifies the model about state change to green.
        """
        self.logger.info('START ON_SWITCH_TO_GREEN')
        self.model.on_switch_to_green()
        self.logger.info('END ON_SWITCH_TO_GREEN')

    def on_switch_to_red(self):
        """
        Notifies the model about state change to red.
        """
        self.logger.info('START ON_SWITCH_TO_RED')
        self.model.on_switch_to_red()
        self.logger.info('END ON_SWITCH_TO_RED')
