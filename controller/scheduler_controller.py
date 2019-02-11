from logging import getLogger

from controller import *


class SchedulerController(Controller):
    """
    Implements Scheduler controller.
    Scheduler object is responsible for properties, UI and events related to the train schedule.
    """
    def __init__(self, map_controller):
        """
        :param map_controller:                  Map controller (parent controller)
        """
        super().__init__(parent_controller=map_controller,
                         logger=getLogger('root.app.game.map.scheduler.controller'))
        self.logger.info('START INIT')
        self.logger.info('END INIT')

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        self.logger.info('START ON_UPDATE_VIEW')
        self.view.on_update()
        self.logger.info('END ON_UPDATE_VIEW')

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Scheduler object: controller and model. Model activates the view if necessary.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_activate()
        self.logger.info('END ON_ACTIVATE')

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Scheduler object: controller, view and model.
        Notifies Map controller about it.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.parent_controller.on_close_schedule()
        self.logger.info('END ON_DEACTIVATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.view.on_change_screen_resolution(screen_resolution)
        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_save_state(self):
        """
        Notifies the model to save scheduler state to user progress database.
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

    def on_level_up(self, level):
        """
        Notifies the model about level update when user hits new level.

        :param level:                   new level value
        """
        self.logger.info('START ON_LEVEL_UP')
        self.model.on_level_up(level)
        self.logger.info('END ON_LEVEL_UP')

    def on_unlock_track(self, track):
        """
        Notifies the model the track is unlocked.

        :param track:                   track number
        """
        self.logger.info('START ON_UNLOCK_TRACK')
        self.model.on_unlock_track(track)
        self.logger.info('END ON_UNLOCK_TRACK')

    def on_activate_view(self):
        """
        Activates the view if user opened schedule screen in the app.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.model.on_activate_view()
        self.logger.info('END ON_ACTIVATE_VIEW')

    def on_deactivate_view(self):
        """
        Deactivates the view if user either closed schedule screen or opened constructor screen.
        Notifies Map controller about it.
        """
        self.logger.info('START ON_DEACTIVATE_VIEW')
        self.view.on_deactivate()
        self.parent_controller.on_close_schedule()
        self.logger.info('END ON_DEACTIVATE_VIEW')

    def on_leave_entry(self, entry_id):
        """
        Notifies the model the entry is ready for new trains approaching.

        :param entry_id:                        entry identification number from 0 to 3
        """
        self.logger.info('START ON_LEAVE_ENTRY')
        self.model.on_leave_entry(entry_id)
        self.logger.info('END ON_LEAVE_ENTRY')
