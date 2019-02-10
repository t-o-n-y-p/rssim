"""
This module implements all controllers.
Controller is an element in MVC pattern which dispatches all possible events to models, views and child controllers.


__init__.py                         implements decorators, constants and base Controller class
app_controller.py                   implements App object controller
constructor_controller.py           implements Constructor object controller
crossover_controller.py             implements Crossover object controller
dispatcher_controller.py            implements Dispatcher object controller
fps_controller.py                   implements FPS object controller
game_controller.py                  implements Game object controller
map_controller.py                   implements Map object controller
railroad_switch_controller.py       implements Railroad switch object controller
scheduler_controller.py             implements Scheduler object controller
settings_controller.py              implements Settings object controller
signal_controller.py                implements Signal object controller
train_controller.py                 implements Train object controller
train_route_controller.py           implements Train route object controller
"""


def controller_is_active(fn):
    """
    Use this decorator to execute function only if controller object is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            args[0].logger.debug('controller_is_active decorator passed')
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def controller_is_not_active(fn):
    """
    Use this decorator to execute function only if controller object is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            args[0].logger.debug('controller_is_not_active decorator passed')
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


def game_is_not_paused(fn):
    """
    Use this decorator within Game object controller to execute function only if game is not paused.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[0].model.game_paused:
            args[0].logger.debug('game_is_not_paused decorator passed')
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def map_view_is_active(fn):
    """
    Use this decorator within Map object controller to execute function only if Map object view is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_map_view_is_activated(*args, **kwargs):
        if args[0].view.is_activated:
            args[0].logger.debug('map_view_is_active decorator passed')
            fn(*args, **kwargs)

    return _handle_if_map_view_is_activated


# --------------------- CONSTANTS ---------------------
FRAMES_IN_2_HOURS = 28800           # number of frames in 2 in-game hours
ZOOM_OUT_SCALE_FACTOR = 0.5         # how much to scale all sprites when map is zoomed out
ZOOM_IN_SCALE_FACTOR = 1.0          # how much to scale all sprites when map is zoomed in
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
        """
        self.model = None
        self.view = None
        self.is_activated = False
        self.parent_controller = parent_controller
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.logger = logger

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
        self.logger.info('START ON_APPEND_HANDLERS')
        if on_mouse_motion_handlers is not None:
            self.logger.debug('on_mouse_motion_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_motion_handlers)}')
            self.logger.debug(f'handlers to add: {len(on_mouse_motion_handlers)}')
            self.on_mouse_motion_handlers.extend(on_mouse_motion_handlers)
            self.logger.debug(f'handlers: {len(self.on_mouse_motion_handlers)}')
        else:
            self.logger.debug('on_mouse_motion_handlers is None')

        if on_mouse_press_handlers is not None:
            self.logger.debug('on_mouse_press_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_press_handlers)}')
            self.logger.debug(f'handlers to add: {len(on_mouse_press_handlers)}')
            self.on_mouse_press_handlers.extend(on_mouse_press_handlers)
            self.logger.debug(f'handlers: {len(self.on_mouse_press_handlers)}')
        else:
            self.logger.debug('on_mouse_press_handlers is None')

        if on_mouse_release_handlers is not None:
            self.logger.debug('on_mouse_release_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_release_handlers)}')
            self.logger.debug(f'handlers to add: {len(on_mouse_release_handlers)}')
            self.on_mouse_release_handlers.extend(on_mouse_release_handlers)
            self.logger.debug(f'handlers: {len(self.on_mouse_release_handlers)}')
        else:
            self.logger.debug('on_mouse_release_handlers is None')

        if on_mouse_drag_handlers is not None:
            self.logger.debug('on_mouse_drag_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_drag_handlers)}')
            self.logger.debug(f'handlers to add: {len(on_mouse_drag_handlers)}')
            self.on_mouse_drag_handlers.extend(on_mouse_drag_handlers)
            self.logger.debug(f'handlers: {len(self.on_mouse_drag_handlers)}')
        else:
            self.logger.debug('on_mouse_drag_handlers is None')

        if on_mouse_leave_handlers is not None:
            self.logger.debug('on_mouse_leave_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_leave_handlers)}')
            self.logger.debug(f'handlers to add: {len(on_mouse_leave_handlers)}')
            self.on_mouse_leave_handlers.extend(on_mouse_leave_handlers)
            self.logger.debug(f'handlers: {len(self.on_mouse_leave_handlers)}')
        else:
            self.logger.debug('on_mouse_leave_handlers is None')

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        if self.parent_controller is not None:
            self.parent_controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers)

        self.logger.info('END ON_APPEND_HANDLERS')

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
        self.logger.info('START ON_DETACH_HANDLERS')
        if on_mouse_motion_handlers is not None:
            self.logger.debug('on_mouse_motion_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_motion_handlers)}')
            self.logger.debug(f'handlers to remove: {len(on_mouse_motion_handlers)}')
            for handler in on_mouse_motion_handlers:
                self.on_mouse_motion_handlers.remove(handler)

            self.logger.debug(f'handlers: {len(self.on_mouse_motion_handlers)}')
        else:
            self.logger.debug('on_mouse_motion_handlers is None')

        if on_mouse_press_handlers is not None:
            self.logger.debug('on_mouse_press_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_press_handlers)}')
            self.logger.debug(f'handlers to remove: {len(on_mouse_press_handlers)}')
            for handler in on_mouse_press_handlers:
                self.on_mouse_press_handlers.remove(handler)

            self.logger.debug(f'handlers: {len(self.on_mouse_press_handlers)}')
        else:
            self.logger.debug('on_mouse_press_handlers is None')

        if on_mouse_release_handlers is not None:
            self.logger.debug('on_mouse_release_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_release_handlers)}')
            self.logger.debug(f'handlers to remove: {len(on_mouse_release_handlers)}')
            for handler in on_mouse_release_handlers:
                self.on_mouse_release_handlers.remove(handler)

            self.logger.debug(f'handlers: {len(self.on_mouse_release_handlers)}')
        else:
            self.logger.debug('on_mouse_release_handlers is None')

        if on_mouse_drag_handlers is not None:
            self.logger.debug('on_mouse_drag_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_drag_handlers)}')
            self.logger.debug(f'handlers to remove: {len(on_mouse_drag_handlers)}')
            for handler in on_mouse_drag_handlers:
                self.on_mouse_drag_handlers.remove(handler)

            self.logger.debug(f'handlers: {len(self.on_mouse_drag_handlers)}')
        else:
            self.logger.debug('on_mouse_drag_handlers is None')

        if on_mouse_leave_handlers is not None:
            self.logger.debug('on_mouse_leave_handlers is not None')
            self.logger.debug(f'handlers: {len(self.on_mouse_leave_handlers)}')
            self.logger.debug(f'handlers to remove: {len(on_mouse_leave_handlers)}')
            for handler in on_mouse_leave_handlers:
                self.on_mouse_leave_handlers.remove(handler)

            self.logger.debug(f'handlers: {len(self.on_mouse_leave_handlers)}')
        else:
            self.logger.debug('on_mouse_leave_handlers is None')

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        if self.parent_controller is not None:
            self.parent_controller.on_detach_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers)

        self.logger.info('END ON_DETACH_HANDLERS')
