from logging import getLogger

from controller import *


class DispatcherController(Controller):
    """
    Implements Dispatcher controller.
    Dispatcher object is responsible for assigning routes to approaching trains.
    """
    def __init__(self, map_id, parent_controller):
        """
        Properties:
            map_id                              ID of the map which this dispatcher belongs to

        :param map_id:                          ID of the map which this dispatcher belongs to
        :param parent_controller:               Map controller subclass
        """
        super().__init__(parent_controller=parent_controller,
                         logger=getLogger(f'root.app.game.map.{map_id}.dispatcher.controller'))
        self.map_id = map_id

    def on_update_view(self):
        """
        Notifies the view and fade-in/fade-out animations.
        """
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

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
        Notifies the model to save dispatcher state to user progress database.
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

    def on_add_train(self, train_controller):
        """
        Notifies the model to add approaching train to the dispatcher.
        After train is created, it needs to be dispatched to the most suitable track.

        :param train_controller:        controller of the train to be added
        """
        self.model.on_add_train(train_controller)

    def on_leave_track(self, track):
        """
        Notifies the model the track is clear for any of the next trains.

        :param track:                   track number
        """
        self.model.on_leave_track(track)

    def on_unlock_track(self, track):
        """
        Notifies the model the track is unlocked and now available for any of the next trains.

        :param track:                   track number
        """
        self.model.on_unlock_track(track)

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
