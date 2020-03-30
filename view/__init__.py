from abc import ABC

from pyglet.window import mouse

from ui import *
from database import USER_DB_CURSOR


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
        if not WINDOW.fullscreen:
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


def shader_sprite_exists(fn):
    def _delete_shader_sprite_if_it_exists(*args, **kwargs):
        if args[0].shader_sprite is not None:
            fn(*args, **kwargs)

    return _delete_shader_sprite_if_it_exists


# --------------------- CONSTANTS ---------------------
MINI_MAP_FADE_OUT_TIMER: Final = 1.0  # time since user releases mouse button after which mini-map disappears
# ------------------- END CONSTANTS -------------------


class AppBaseView(ABC):
    def __init__(self, controller, logger, child_window=False):
        self.logger = logger
        self.child_window = child_window
        self.is_activated = False
        self.controller = controller
        self.viewport = Viewport()
        self.opacity = 0
        self.buttons = []
        self.notifications = []
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.on_mouse_scroll_handlers = []
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.on_window_resize_handlers = [self.on_window_resize, ]
        self.on_window_activate_handlers = [self.on_window_activate, ]
        self.on_window_show_handlers = [self.on_window_show, ]
        self.on_window_deactivate_handlers = [self.on_window_deactivate, ]
        self.on_window_hide_handlers = [self.on_window_hide, ]
        self.screen_resolution = (0, 0)
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = USER_DB_CURSOR.fetchone()[0]
        self.all_notifications_enabled = False
        self.shader_sprite = None
        USER_DB_CURSOR.execute('SELECT * FROM notification_settings')
        self.level_up_notification_enabled, self.feature_unlocked_notification_enabled, \
            self.construction_completed_notification_enabled, self.enough_money_notification_enabled, \
            self.bonus_expired_notification_enabled, self.shop_storage_notification_enabled = USER_DB_CURSOR.fetchone()

    def on_activate(self):
        self.is_activated = True
        self.on_append_view_handlers()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        self.on_detach_view_handlers()
        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    def on_update(self):
        pass

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        if self.child_window:
            inner_area_rect = get_inner_area_rect(self.screen_resolution)
            self.viewport.x1, self.viewport.y1 = inner_area_rect[:2]
            self.viewport.x2 = self.viewport.x1 + inner_area_rect[2]
            self.viewport.y2 = self.viewport.y1 + inner_area_rect[3]
        else:
            self.viewport.x1, self.viewport.y1 = 0, 0
            self.viewport.x2, self.viewport.y2 = self.screen_resolution

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()

    def on_update_clock_state(self, clock_24h_enabled):
        self.clock_24h_enabled = clock_24h_enabled

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

    def on_window_activate(self):
        self.all_notifications_enabled = False
        self.notifications.clear()

    def on_window_show(self):
        self.all_notifications_enabled = False
        self.notifications.clear()

    def on_window_deactivate(self):
        self.all_notifications_enabled = True

    def on_window_hide(self):
        self.all_notifications_enabled = True

    @final
    def on_change_level_up_notification_state(self, notification_state):
        self.level_up_notification_enabled = notification_state

    @final
    def on_change_feature_unlocked_notification_state(self, notification_state):
        self.feature_unlocked_notification_enabled = notification_state

    @final
    def on_change_construction_completed_notification_state(self, notification_state):
        self.construction_completed_notification_enabled = notification_state

    @final
    def on_change_enough_money_notification_state(self, notification_state):
        self.enough_money_notification_enabled = notification_state

    @final
    def on_change_bonus_expired_notification_state(self, notification_state):
        self.bonus_expired_notification_enabled = notification_state

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.shop_storage_notification_enabled = notification_state

    @final
    def on_append_view_handlers(self):
        # appends view handlers
        self.controller.on_append_view_handlers(
            on_mouse_motion_handlers=self.on_mouse_motion_handlers,
            on_mouse_press_handlers=self.on_mouse_press_handlers,
            on_mouse_release_handlers=self.on_mouse_release_handlers,
            on_mouse_drag_handlers=self.on_mouse_drag_handlers,
            on_mouse_leave_handlers=self.on_mouse_leave_handlers,
            on_mouse_scroll_handlers=self.on_mouse_scroll_handlers,
            on_key_press_handlers=self.on_key_press_handlers,
            on_text_handlers=self.on_text_handlers
        )
        # appends button handlers
        for b in self.buttons:
            self.controller.on_append_view_handlers(
                on_mouse_motion_handlers=(b.on_mouse_motion,),
                on_mouse_press_handlers=(b.on_mouse_press,),
                on_mouse_release_handlers=(b.on_mouse_release,),
                on_mouse_leave_handlers=(b.on_mouse_leave,)
            )

    @final
    def on_detach_view_handlers(self):
        # detaches view handlers
        self.controller.on_detach_view_handlers(
            on_mouse_motion_handlers=self.on_mouse_motion_handlers,
            on_mouse_press_handlers=self.on_mouse_press_handlers,
            on_mouse_release_handlers=self.on_mouse_release_handlers,
            on_mouse_drag_handlers=self.on_mouse_drag_handlers,
            on_mouse_leave_handlers=self.on_mouse_leave_handlers,
            on_mouse_scroll_handlers=self.on_mouse_scroll_handlers,
            on_key_press_handlers=self.on_key_press_handlers,
            on_text_handlers=self.on_text_handlers
        )
        # detaches button handlers
        for b in self.buttons:
            self.controller.on_detach_view_handlers(
                on_mouse_motion_handlers=(b.on_mouse_motion,),
                on_mouse_press_handlers=(b.on_mouse_press,),
                on_mouse_release_handlers=(b.on_mouse_release,),
                on_mouse_leave_handlers=(b.on_mouse_leave,)
            )

    @final
    def on_append_window_handlers(self):
        self.controller.on_append_window_handlers(
            on_window_resize_handlers=self.on_window_resize_handlers,
            on_window_activate_handlers=self.on_window_activate_handlers,
            on_window_show_handlers=self.on_window_show_handlers,
            on_window_deactivate_handlers=self.on_window_deactivate_handlers,
            on_window_hide_handlers=self.on_window_hide_handlers
        )
        for b in self.buttons:
            self.controller.on_append_window_handlers(on_window_resize_handlers=(b.on_window_resize,))

    @final
    def on_detach_window_handlers(self):
        self.controller.on_detach_window_handlers(
            on_window_resize_handlers=self.on_window_resize_handlers,
            on_window_activate_handlers=self.on_window_activate_handlers,
            on_window_show_handlers=self.on_window_show_handlers,
            on_window_deactivate_handlers=self.on_window_deactivate_handlers,
            on_window_hide_handlers=self.on_window_hide_handlers
        )
        for b in self.buttons:
            self.controller.on_detach_window_handlers(on_window_resize_handlers=(b.on_window_resize,))


class GameBaseView(AppBaseView, ABC):
    def __init__(self, controller, logger, child_window=False):
        super().__init__(controller, logger, child_window)
        USER_DB_CURSOR.execute('SELECT * FROM epoch_timestamp')
        self.game_time, self.game_time_fraction, self.dt_multiplier = USER_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT level, money, exp_bonus_multiplier, money_bonus_multiplier,  
                                  construction_time_bonus_multiplier FROM game_progress''')
        self.level, self.money, self.exp_bonus_multiplier, self.money_bonus_multiplier, \
            self.construction_time_bonus_multiplier = USER_DB_CURSOR.fetchone()

    def on_update_time(self, dt):
        self.game_time_fraction += dt * self.dt_multiplier
        self.game_time += int(self.game_time_fraction)
        self.game_time_fraction %= 1

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

    @final
    def on_dt_multiplier_update(self, dt_multiplier):
        self.dt_multiplier = dt_multiplier

    @final
    def on_activate_construction_time_bonus_code(self, value):
        self.construction_time_bonus_multiplier = round(1.0 + value, 2)

    @final
    def on_deactivate_construction_time_bonus_code(self):
        self.construction_time_bonus_multiplier = 1.0


class MapBaseView(GameBaseView, ABC):
    def __init__(self, controller, map_id, logger, child_window=False):
        super().__init__(controller, logger, child_window)
        self.locked = True
        self.map_id = map_id

    @final
    def on_unlock(self):
        self.locked = False
        # this workaround is needed for the object to be displayed immediately on the map
        self.on_update()
