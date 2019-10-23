from ctypes import windll

from pyglet.window import mouse

from ui import *
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
        if not SURFACE.fullscreen:
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
                and args[2] in range(get_bottom_bar_height(args[0].screen_resolution),
                                     args[0].screen_resolution[1] - get_top_bar_height(args[0].screen_resolution)):
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


def bonus_expired_notification_enabled(fn):
    def _send_notification_if_bonus_expired_notification_enabled(*args, **kwargs):
        if args[0].bonus_expired_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_bonus_expired_notification_enabled


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


def shop_storage_notification_enabled(fn):
    def _send_notification_if_shop_storage_notification_enabled(*args, **kwargs):
        if args[0].shop_storage_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_shop_storage_notification_enabled


def cursor_is_over_the_app_header(fn):
    def _handle_if_cursor_is_over_the_app_header(*args, **kwargs):
        if args[1] in range(args[0].viewport.x1 + get_top_bar_height(args[0].screen_resolution) * 2,
                            args[0].viewport.x2 - get_top_bar_height(args[0].screen_resolution) * 3) \
                and args[2] in range(args[0].viewport.y2 - get_top_bar_height(args[0].screen_resolution),
                                     args[0].viewport.y2):
            fn(*args, **kwargs)

    return _handle_if_cursor_is_over_the_app_header


# --------------------- CONSTANTS ---------------------
MINI_MAP_FADE_OUT_TIMER: Final = 1.0        # time since user releases mouse button after which mini-map disappears
# ------------------- END CONSTANTS -------------------


class AppBaseView:
    def __init__(self, logger, child_window=False):
        self.logger = logger
        self.child_window = child_window
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
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.screen_resolution = (0, 0)
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = bool(USER_DB_CURSOR.fetchone()[0])
        self.all_notifications_enabled = False
        self.shader_sprite = None

    def on_activate(self):
        self.is_activated = True
        self.on_append_handlers()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.on_detach_handlers()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale

    def on_change_screen_resolution(self, screen_resolution):
        pass

    def on_apply_shaders_and_draw_vertices(self):
        pass

    def on_update_clock_state(self, clock_24h_enabled):
        pass

    def on_update_opacity(self, new_opacity):
        pass

    @final
    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @final
    def on_disable_notifications(self):
        self.all_notifications_enabled = False

    @final
    def on_enable_notifications(self):
        self.all_notifications_enabled = True

    @final
    def on_append_handlers(self):
        # appends view handlers
        self.controller.on_append_handlers(on_mouse_motion_handlers=self.on_mouse_motion_handlers,
                                           on_mouse_press_handlers=self.on_mouse_press_handlers,
                                           on_mouse_release_handlers=self.on_mouse_release_handlers,
                                           on_mouse_drag_handlers=self.on_mouse_drag_handlers,
                                           on_mouse_leave_handlers=self.on_mouse_leave_handlers,
                                           on_mouse_scroll_handlers=self.on_mouse_scroll_handlers,
                                           on_key_press_handlers=self.on_key_press_handlers,
                                           on_text_handlers=self.on_text_handlers)
        # appends button handlers
        for b in self.buttons:
            self.controller.on_append_handlers(on_mouse_motion_handlers=(b.handle_mouse_motion, ),
                                               on_mouse_press_handlers=(b.handle_mouse_press, ),
                                               on_mouse_release_handlers=(b.handle_mouse_release, ),
                                               on_mouse_leave_handlers=(b.handle_mouse_leave, ))

    @final
    def on_detach_handlers(self):
        # detaches view handlers
        self.controller.on_detach_handlers(on_mouse_motion_handlers=self.on_mouse_motion_handlers,
                                           on_mouse_press_handlers=self.on_mouse_press_handlers,
                                           on_mouse_release_handlers=self.on_mouse_release_handlers,
                                           on_mouse_drag_handlers=self.on_mouse_drag_handlers,
                                           on_mouse_leave_handlers=self.on_mouse_leave_handlers,
                                           on_mouse_scroll_handlers=self.on_mouse_scroll_handlers,
                                           on_key_press_handlers=self.on_key_press_handlers,
                                           on_text_handlers=self.on_text_handlers)
        # detaches button handlers
        for b in self.buttons:
            self.controller.on_detach_handlers(on_mouse_motion_handlers=(b.handle_mouse_motion, ),
                                               on_mouse_press_handlers=(b.handle_mouse_press, ),
                                               on_mouse_release_handlers=(b.handle_mouse_release, ),
                                               on_mouse_leave_handlers=(b.handle_mouse_leave, ))


class GameBaseView(AppBaseView):
    def __init__(self, logger):
        super().__init__(logger)
        USER_DB_CURSOR.execute('SELECT game_time FROM epoch_timestamp')
        self.game_time = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('''SELECT level, money, exp_bonus_multiplier, money_bonus_multiplier 
                                  FROM game_progress''')
        self.level, self.money, self.exp_bonus_multiplier, self.money_bonus_multiplier = USER_DB_CURSOR.fetchone()

    def on_update_time(self):
        self.game_time += 1

    def on_level_up(self):
        self.level += 1

    def on_update_money(self, money):
        self.money = money

    def on_activate_exp_bonus_code(self, value):
        self.exp_bonus_multiplier = round(1.0 + value, 2)

    def on_deactivate_exp_bonus_code(self):
        self.exp_bonus_multiplier = 1.0

    def on_activate_money_bonus_code(self, value):
        self.money_bonus_multiplier = round(1.0 + value, 2)

    def on_deactivate_money_bonus_code(self):
        self.money_bonus_multiplier = 1.0


class MapBaseView(GameBaseView):
    def __init__(self, logger):
        super().__init__(logger)
        self.locked = True
        USER_DB_CURSOR.execute('SELECT last_known_base_offset FROM graphics')
        self.base_offset = tuple(map(int, USER_DB_CURSOR.fetchone()[0].split(',')))
        USER_DB_CURSOR.execute('SELECT zoom_out_activated FROM graphics')
        self.zoom_out_activated = bool(USER_DB_CURSOR.fetchone()[0])
        if self.zoom_out_activated:
            self.zoom_factor = 0.5
        else:
            self.zoom_factor = 1.0

    def on_change_base_offset(self, new_base_offset):
        pass

    def on_change_zoom_factor(self, scale_factor, zoom_out_activated):
        pass

    @final
    def on_unlock(self):
        self.locked = False
        # this workaround is needed for the object to be displayed immediately on the map
        self.on_change_base_offset(self.base_offset)
