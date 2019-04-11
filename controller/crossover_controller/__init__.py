from controller import *


class CrossoverController(Controller):
    """
    Implements Crossover controller.
    Crossover object is responsible for properties, UI and events related to the crossover.
    """
    def __init__(self, parent_controller, track_param_1, track_param_2, crossover_type, logger):
        """
        Properties:
            track_param_1               number of the first track of two being connected by the crossover
            track_param_2               number of the second track of two being connected by the crossover
            crossover_type              crossover location: left/right side of the map

        :param parent_controller:       Map controller subclass
        :param track_param_1:           number of the first track of two being connected by the crossover
        :param track_param_2:           number of the second track of two being connected by the crossover
        :param crossover_type:          crossover location: left/right side of the map
        :param logger:                  telemetry instance
        """
        super().__init__(
            parent_controller=parent_controller,
            logger=logger
        )
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.crossover_type = crossover_type

    def on_update_view(self):
        """
        Notifies the view to update fade-in/fade-out animations.
        """
        self.view.on_update()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Crossover object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Crossover object: controller, view and model.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    def on_save_state(self):
        """
        Notifies the model to save crossover state to user progress database.
        """
        self.model.on_save_state()

    def on_change_base_offset(self, new_base_offset):
        """
        Notifies the view about base offset update.

        :param new_base_offset:         new base offset
        """
        self.view.on_change_base_offset(new_base_offset)

    def on_change_screen_resolution(self, screen_resolution):
        """
        Notifies the view about screen resolution update.

        :param screen_resolution:       new screen resolution
        """
        self.view.on_change_screen_resolution(screen_resolution)

    def on_zoom_in(self):
        """
        Notifies the view to zoom in all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.
        """
        self.view.on_change_zoom_factor(ZOOM_IN_SCALE_FACTOR, zoom_out_activated=False)

    def on_zoom_out(self):
        """
        Notifies the view to zoom out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.
        """
        self.view.on_change_zoom_factor(ZOOM_OUT_SCALE_FACTOR, zoom_out_activated=True)

    def on_activate_view(self):
        """
        Activates the view if user opened game screen in the app.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view if user either closed game screen or opened settings screen.
        """
        self.view.on_deactivate()

    def on_force_busy_on(self, positions, train_id):
        """
        Notifies model the train is approaching.

        :param positions:               direction the train is about to proceed to
        :param train_id:                ID of the train which is about to pass through the crossover
        """
        self.model.on_force_busy_on(positions, train_id)

    def on_force_busy_off(self, positions):
        """
        Notifies model the train has passed the crossover.

        :param positions:               direction that was previously locked for train
        """
        self.model.on_force_busy_off(positions)

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

    def on_unlock(self):
        """
        Notifies model the crossover was unlocked.
        """
        self.model.on_unlock()