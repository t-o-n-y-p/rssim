from ctypes import windll

from pyglet.window import mouse

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR
from ui import Viewport


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


def track_cell_is_created(fn):
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


def notifications_available(fn):
    def _send_notifications_if_they_are_enabled(*args, **kwargs):
        if args[0].all_notifications_enabled:
            fn(*args, **kwargs)

    return _send_notifications_if_they_are_enabled


def level_up_notification_enabled(fn):
    def _send_notification_if_level_up_notification_enabled(*args, **kwargs):
        if args[0].level_up_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_level_up_notification_enabled


def enough_money_notification_enabled(fn):
    def _send_notification_if_enough_money_notification_enabled(*args, **kwargs):
        if args[0].enough_money_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_enough_money_notification_enabled


def feature_unlocked_notification_enabled(fn):
    def _send_notification_if_feature_unlocked_notification_enabled(*args, **kwargs):
        if args[0].feature_unlocked_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_feature_unlocked_notification_enabled


def construction_completed_notification_enabled(fn):
    def _send_notification_if_construction_completed_notification_enabled(*args, **kwargs):
        if args[0].construction_completed_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_construction_completed_notification_enabled


def shader_sprite_exists(fn):
    def _handle_if_shader_sprite_exists(*args, **kwargs):
        if args[0].shader_sprite is not None:
            fn(*args, **kwargs)

    return _handle_if_shader_sprite_exists


# --------------------- CONSTANTS ---------------------
MAP_WIDTH = 8192                                # full-size map width
MAP_HEIGHT = 4096                               # full-size map height
MINI_MAP_FADE_OUT_TIMER = 1.0                   # time since user releases mouse button after which mini-map disappears
# ------------------- END CONSTANTS -------------------


class View:
    def __init__(self, logger):
        self.logger = logger
        self.is_activated = False
        self.controller = None
        self.viewport = Viewport()
        self.opacity = 0
        self.buttons = []
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.on_mouse_scroll_handlers = []
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.screen_resolution = monitor_resolution_config
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.screen_resolution = USER_DB_CURSOR.fetchone()

        USER_DB_CURSOR.execute('SELECT last_known_base_offset FROM graphics')
        self.base_offset = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        USER_DB_CURSOR.execute('SELECT zoom_out_activated FROM graphics')
        self.zoom_out_activated = bool(USER_DB_CURSOR.fetchone()[0])
        if self.zoom_out_activated:
            self.zoom_factor = 0.5
        else:
            self.zoom_factor = 1.0

        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.all_notifications_enabled = False
        self.shader_sprite = None

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        pass

    def on_update_opacity(self, new_opacity):
        pass

    def on_disable_notifications(self):
        self.all_notifications_enabled = False

    def on_enable_notifications(self):
        self.all_notifications_enabled = True

    def on_assign_controller(self, controller):
        self.controller = controller
        on_mouse_motion_handlers = []
        on_mouse_press_handlers = []
        on_mouse_release_handlers = []
        on_mouse_leave_handlers = []
        # collects all handlers from the buttons in four lists
        for b in self.buttons:
            on_mouse_motion_handlers.append(b.handle_mouse_motion)
            on_mouse_press_handlers.append(b.handle_mouse_press)
            on_mouse_release_handlers.append(b.handle_mouse_release)
            on_mouse_leave_handlers.append(b.handle_mouse_leave)

        # appends view handlers
        self.controller.on_append_handlers(on_mouse_motion_handlers=self.on_mouse_motion_handlers,
                                           on_mouse_press_handlers=self.on_mouse_press_handlers,
                                           on_mouse_release_handlers=self.on_mouse_release_handlers,
                                           on_mouse_drag_handlers=self.on_mouse_drag_handlers,
                                           on_mouse_leave_handlers=self.on_mouse_leave_handlers,
                                           on_mouse_scroll_handlers=self.on_mouse_scroll_handlers)
        # appends button handlers
        self.controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                           on_mouse_press_handlers=on_mouse_press_handlers,
                                           on_mouse_release_handlers=on_mouse_release_handlers,
                                           on_mouse_leave_handlers=on_mouse_leave_handlers)
