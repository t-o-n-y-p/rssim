from logging import getLogger

from controller import *


class TrainRouteController(Controller):
    """
    Implements Train route controller.
    Train route object is responsible for properties, UI and events related to the train route.
    """
    def __init__(self, map_id, parent_controller, track, train_route):
        """
        Properties:
            map_id                              ID of the map which this constructor belongs to
            track                               route track number
            train_route                         route type (e.g. left/right entry/exit)

        :param map_id:                          ID of the map which this constructor belongs to
        :param parent_controller:               Map controller subclass
        :param track:                           route track number
        :param train_route:                     route type (e.g. left/right entry/exit)
        """
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.train_route.{track}.{train_route}.controller'))
        self.track = track
        self.train_route = train_route
        self.map_id = map_id

    def on_update_view(self):
        """
        Notifies the view and fade-in/fade-out animations.
        """
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    @controller_is_not_active
    def on_activate(self):
        """
        Activates Train route object: controller and model. Model activates the view if necessary.
        """
        self.is_activated = True
        self.model.on_activate()

    @controller_is_active
    def on_deactivate(self):
        """
        Deactivates Train route object: controller, view and model.
        """
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()

    def on_activate_view(self):
        """
        Activates the view.
        """
        self.model.on_activate_view()

    def on_deactivate_view(self):
        """
        Deactivates the view.
        """
        self.view.on_deactivate()

    def on_save_state(self):
        """
        Notifies the model to save train route state to user progress database.
        """
        self.model.on_save_state()

    def on_open_train_route(self, train_id, cars):
        """
        Notifies the model to open train route.

        :param train_id:                        ID of the train which opens the train route
        :param cars:                            number of cars in the train
        """
        self.model.on_open_train_route(train_id, cars)

    def on_close_train_route(self):
        """
        Notifies the model to close train route.
        """
        self.model.on_close_train_route()

    def on_update_train_route_sections(self, last_car_position):
        """
        Notifies the model about last train car position update.

        :param last_car_position:               train last car position on the route
        """
        self.model.on_update_train_route_sections(last_car_position)

    def on_update_time(self, game_time):
        """
        Notifies the model about in-game time update.

        :param game_time:               current in-game time
        """
        self.model.on_update_time(game_time)

    def on_update_priority(self, priority):
        """
        Notifies the model about priority update.

        :param priority:                        new priority value
        """
        self.model.on_update_priority(priority)

    def on_update_section_status(self, section, status):
        """
        Notifies the model about particular section status update.

        :param section:                         train route section number
        :param status:                          new status
        """
        self.model.on_update_section_status(section, status)

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

    def on_update_fade_animation_state(self, new_state):
        """
        Notifies fade-in/fade-out animations about state update.

        :param new_state:                       indicates if fade animations were enabled or disabled
        """
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
