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
        self.train_id = train_id

    def on_update_view(self):
        """
        Notifies the view to create car sprites if they are inside game window and delete if they are not.
        """
        self.view.on_update()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Train object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Train object: controller, view and model.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    def on_save_state(self):
        """
        Notifies the model to save train state to user progress database.
        """
        self.model.on_save_state()

    def on_update_time(self, game_time):
        """
        Notifies the model about in-game time update.

        :param game_time:               current in-game time
        """
        self.model.on_update_time(game_time)

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

    def on_set_train_start_point(self, first_car_start_point):
        """
        Notifies the model about initial position update.

        :param first_car_start_point:           data
        """
        self.model.on_set_train_start_point(first_car_start_point)

    def on_set_train_stop_point(self, first_car_stop_point):
        """
        Notifies the model where to stop the train if signal is at danger.

        :param first_car_stop_point:            data
        """
        self.model.on_set_train_stop_point(first_car_stop_point)

    def on_set_train_destination_point(self, first_car_destination_point):
        """
        Notifies the model about destination point update.
        When train reaches destination point, route is completed.

        :param first_car_destination_point:     data
        """
        self.model.on_set_train_destination_point(first_car_destination_point)

    def on_set_trail_points(self, trail_points_v2):
        """
        Notifies the model about trail points update.

        :param trail_points_v2:                 data
        """
        self.model.on_set_trail_points(trail_points_v2)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        self.view.on_update_current_locale(new_locale)
