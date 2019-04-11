from controller import *


class SchedulerController(Controller):
    """
    Implements Scheduler controller.
    Scheduler object is responsible for properties, UI and events related to the train schedule.
    """
    def __init__(self, parent_controller, logger):
        """
        :param parent_controller:               Map controller subclass
        :param logger:                          telemetry instance
        """
        super().__init__(parent_controller=parent_controller, logger=logger)

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        self.view.on_update()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Scheduler object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Scheduler object: controller, view and model.
        Notifies Map controller about it.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.parent_controller.on_close_schedule()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)

    def on_save_state(self):
        """
        Notifies the model to save scheduler state to user progress database.
        """
        self.model.on_save_state()

    def on_update_time(self, game_time):
        """
        Notifies the model about in-game time update.

        :param game_time:               current in-game time
        """
        self.model.on_update_time(game_time)

    def on_level_up(self, level):
        """
        Notifies the model about level update when user hits new level.

        :param level:                   new level value
        """
        self.model.on_level_up(level)

    def on_unlock_track(self, track):
        """
        Notifies the model the track is unlocked.

        :param track:                   track number
        """
        self.model.on_unlock_track(track)

    def on_activate_view(self):
        """
        Activates the view if user opened schedule screen in the app.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view if user either closed schedule screen or opened constructor screen.
        Notifies Map controller about it.
        """
        self.view.on_deactivate()
        self.parent_controller.on_close_schedule()

    def on_leave_entry(self, entry_id):
        """
        Notifies the model the entry is ready for new trains approaching.

        :param entry_id:                        entry identification number from 0 to 3
        """
        self.model.on_leave_entry(entry_id)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)

    def on_disable_notifications(self):
        """
        Disables system notifications for the view and all child controllers.
        """
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        """
        Enables system notifications for the view and all child controllers.
        """
        self.view.on_enable_notifications()

    def on_apply_shaders_and_draw_vertices(self):
        """
        Notifies the view and child controllers to draw all sprites with shaders.
        """
        self.view.on_apply_shaders_and_draw_vertices()