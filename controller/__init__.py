def controller_is_active(fn):
    """
    Use this decorator to execute function only if controller is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def controller_is_not_active(fn):
    """
    Use this decorator to execute function only if controller is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


def game_is_not_paused(fn):
    """
    Use this decorator within Game controller to execute function only if game is not paused.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[0].model.game_paused:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def map_view_is_active(fn):
    """
    Use this decorator within Map controller to execute function only if Map object view is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_map_view_is_activated(*args, **kwargs):
        if args[0].view.is_activated:
            fn(*args, **kwargs)

    return _handle_if_map_view_is_activated


# --------------------- CONSTANTS ---------------------
FRAMES_IN_ONE_HOUR = 14400              # number of frames in 1 in-game hour
ZOOM_OUT_SCALE_FACTOR = 0.5             # how much to scale all sprites when map is zoomed out
ZOOM_IN_SCALE_FACTOR = 1.0              # how much to scale all sprites when map is zoomed in
SECTION_TYPE = 0                        # meaning of section[] list's element 0
SECTION_TRACK_NUMBER_1 = 1              # meaning of section[] list's element 1
SECTION_TRACK_NUMBER_2 = 2              # meaning of section[] list's element 2
TRAIN_ROUTE_DATA_TRACK_NUMBER = 0       # meaning of train_route_data[] list's element 0
TRAIN_ROUTE_DATA_TYPE = 1               # meaning of train_route_data[] list's element 1
TRAIN_ROUTE_DATA_SECTION_NUMBER = 2     # meaning of train_route_data[] list's element 2
# ------------------- END CONSTANTS -------------------


class Controller:
    """
    Base class for all controllers in the app.
    """
    def __init__(self, parent_controller=None, logger=None):
        """
        Properties:
            model                           object model
            view                            object view
            is_activated                    indicates if controller (and object in general) is active
            parent_controller               controller which this controller is child for in the hierarchy
            on_mouse_press_handlers         list of on_mouse_press event handlers
                                            from this controller and all child controllers
            on_mouse_release_handlers       list of on_mouse_release event handlers
                                            from this controller and all child controllers
            on_mouse_motion_handlers        list of on_mouse_motion event handlers
                                            from this controller and all child controllers
            on_mouse_drag_handlers          list of on_mouse_drag event handlers
                                            from this controller and all child controllers
            on_mouse_leave_handlers         list of on_mouse_leave event handlers
                                            from this controller and all child controllers
            logger                          telemetry instance

        :param parent_controller:           controller which this controller is child for in the hierarchy
        :param logger:                      telemetry instance
        """
        self.logger = logger
        self.model = None
        self.view = None
        self.is_activated = False
        self.parent_controller = parent_controller
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []

    def on_update_view(self):
        """
        Notifies object view and child objects views to update.
        Usually it is needed for fade-in/fade-out animations
        or for some views where all sprites are not created at once
        and remaining sprites are created frame by frame to avoid massive FPS drop.
        """
        pass

    def on_activate(self):
        """
        Activates controller (and object in general), its model and view (if necessary)
        and child objects (if necessary).
        """
        pass

    def on_deactivate(self):
        """
        Deactivates controller (and object in general), its model and view (if necessary)
        and child objects.
        """
        pass

    def on_append_handlers(self, on_mouse_motion_handlers=None, on_mouse_press_handlers=None,
                           on_mouse_release_handlers=None, on_mouse_drag_handlers=None,
                           on_mouse_leave_handlers=None):
        """
        When view is created, we need to append handlers from its buttons and view itself
        to controller and all parent controllers up to App object controller
        because main game loop grabs handlers from there.

        :param on_mouse_motion_handlers:            list of on_mouse_motion event handlers to be appended
        :param on_mouse_press_handlers:             list of on_mouse_press event handlers to be appended
        :param on_mouse_release_handlers:           list of on_mouse_release event handlers to be appended
        :param on_mouse_drag_handlers:              list of on_mouse_drag event handlers to be appended
        :param on_mouse_leave_handlers:             list of on_mouse_leave event handlers to be appended
        """
        if on_mouse_motion_handlers is not None:
            self.on_mouse_motion_handlers.extend(on_mouse_motion_handlers)

        if on_mouse_press_handlers is not None:
            self.on_mouse_press_handlers.extend(on_mouse_press_handlers)

        if on_mouse_release_handlers is not None:
            self.on_mouse_release_handlers.extend(on_mouse_release_handlers)

        if on_mouse_drag_handlers is not None:
            self.on_mouse_drag_handlers.extend(on_mouse_drag_handlers)

        if on_mouse_leave_handlers is not None:
            self.on_mouse_leave_handlers.extend(on_mouse_leave_handlers)

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        if self.parent_controller is not None:
            self.parent_controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers)

    def on_detach_handlers(self, on_mouse_motion_handlers=None, on_mouse_press_handlers=None,
                           on_mouse_release_handlers=None, on_mouse_drag_handlers=None,
                           on_mouse_leave_handlers=None):
        """
        When handlers should no longer be executed (e.g. button was removed permanently),
        we need to detach handlers from controller and all parent controllers up to App object controller
        because main game loop grabs handlers from there.

        :param on_mouse_motion_handlers:            list of on_mouse_motion event handlers to be detached
        :param on_mouse_press_handlers:             list of on_mouse_press event handlers to be detached
        :param on_mouse_release_handlers:           list of on_mouse_release event handlers to be detached
        :param on_mouse_drag_handlers:              list of on_mouse_drag event handlers to be detached
        :param on_mouse_leave_handlers:             list of on_mouse_leave event handlers to be detached
        """
        if on_mouse_motion_handlers is not None:
            for handler in on_mouse_motion_handlers:
                self.on_mouse_motion_handlers.remove(handler)

        if on_mouse_press_handlers is not None:
            for handler in on_mouse_press_handlers:
                self.on_mouse_press_handlers.remove(handler)

        if on_mouse_release_handlers is not None:
            for handler in on_mouse_release_handlers:
                self.on_mouse_release_handlers.remove(handler)

        if on_mouse_drag_handlers is not None:
            for handler in on_mouse_drag_handlers:
                self.on_mouse_drag_handlers.remove(handler)

        if on_mouse_leave_handlers is not None:
            for handler in on_mouse_leave_handlers:
                self.on_mouse_leave_handlers.remove(handler)

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        if self.parent_controller is not None:
            self.parent_controller.on_detach_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers)

    def on_update_current_locale(self, new_locale):
        """
        Notifies the view and child controllers (if any) about current locale value update.

        :param new_locale:                      selected locale
        """
        pass
