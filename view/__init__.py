from pyglet.window import mouse


def view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


def game_window_is_active(fn):
    def _handle_if_game_window_is_active(*args, **kwargs):
        if args[0].surface.visible:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_active


def game_is_not_fullscreen(fn):
    def _handle_if_game_window_is_not_fullscreen(*args, **kwargs):
        if not args[0].surface.fullscreen:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_not_fullscreen


def app_window_move_mode_enabled(fn):
    def _handle_if_app_window_move_mode_enabled(*args, **kwargs):
        if args[0].app_window_move_mode:
            fn(*args, **kwargs)

    return _handle_if_app_window_move_mode_enabled


def left_mouse_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def track_is_in_top4(fn):
    def _handle_if_track_is_in_top4(*args, **kwargs):
        if args[2] in args[0].locked_tracks_labels:
            fn(*args, **kwargs)

    return _handle_if_track_is_in_top4


def map_move_mode_available(fn):
    def _turn_on_move_mode_if_map_move_mode_available(*args, **kwargs):
        if args[0].map_move_mode_available and not args[0].controller.scheduler.view.is_activated \
                and not args[0].controller.constructor.view.is_activated:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_available


def map_move_mode_enabled(fn):
    def _turn_on_move_mode_if_map_move_mode_enabled(*args, **kwargs):
        if args[0].map_move_mode:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_enabled


def cursor_is_on_the_map(fn):
    def _enable_map_move_mode_if_cursor_is_on_the_map(*args, **kwargs):
        if args[1] in range(0, args[0].screen_resolution[0]) \
                and args[2] in range(args[0].bottom_bar_height, args[0].screen_resolution[1] - args[0].top_bar_height):
            fn(*args, **kwargs)

    return _enable_map_move_mode_if_cursor_is_on_the_map


def mini_map_is_not_active(fn):
    def _handle_if_mini_map_is_not_activated(*args, **kwargs):
        if not args[0].is_mini_map_activated:
            fn(*args, **kwargs)

    return _handle_if_mini_map_is_not_activated


def signal_is_displayed_on_map(fn):
    def _handle_if_signal_is_displayed_on_map(*args, **kwargs):
        if args[0].signal_sprite is not None:
            fn(*args, **kwargs)

    return _handle_if_signal_is_displayed_on_map


class View:
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        self.user_db_cursor = user_db_cursor
        self.config_db_cursor = config_db_cursor
        self.controller = None
        self.surface = surface
        self.batches = batches
        self.groups = groups
        self.is_activated = False
        self.buttons = []
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.screen_resolution = (1280, 720)
        self.bottom_bar_height = 72
        self.top_bar_height = 36
        self.base_offset = (-3456, -1688)
        self.zoom_out_activated = False
        self.zoom_factor = 1.0

    def on_update(self):
        pass

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_assign_controller(self, controller):
        self.controller = controller
        on_mouse_motion_handlers = []
        on_mouse_press_handlers = []
        on_mouse_release_handlers = []
        on_mouse_leave_handlers = []
        for b in self.buttons:
            on_mouse_motion_handlers.append(b.handle_mouse_motion)
            on_mouse_press_handlers.append(b.handle_mouse_press)
            on_mouse_release_handlers.append(b.handle_mouse_release)
            on_mouse_leave_handlers.append(b.handle_mouse_leave)

        self.controller.on_append_handlers(on_mouse_motion_handlers=self.on_mouse_motion_handlers,
                                           on_mouse_press_handlers=self.on_mouse_press_handlers,
                                           on_mouse_release_handlers=self.on_mouse_release_handlers,
                                           on_mouse_drag_handlers=self.on_mouse_drag_handlers,
                                           on_mouse_leave_handlers=self.on_mouse_leave_handlers)
        self.controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                           on_mouse_press_handlers=on_mouse_press_handlers,
                                           on_mouse_release_handlers=on_mouse_release_handlers,
                                           on_mouse_leave_handlers=on_mouse_leave_handlers)

    def on_recalculate_ui_properties(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = int(72 / 1280 * self.screen_resolution[0]) // 2
