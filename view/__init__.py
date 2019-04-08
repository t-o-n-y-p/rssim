from pyglet.window import mouse

from ui import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


def view_is_active(fn):
    """
    Use this decorator to execute function only if view is active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def view_is_not_active(fn):
    """
    Use this decorator to execute function only if view is not active.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


def game_is_not_fullscreen(fn):
    """
    Use this decorator within App view to execute function only if fullscreen mode is not activated.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_game_window_is_not_fullscreen(*args, **kwargs):
        if not args[0].surface.fullscreen:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_not_fullscreen


def app_window_move_mode_enabled(fn):
    """
    Use this decorator within App view to execute function only if user is about to move the app window.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_app_window_move_mode_enabled(*args, **kwargs):
        if args[0].app_window_move_mode:
            fn(*args, **kwargs)

    return _handle_if_app_window_move_mode_enabled


def left_mouse_button(fn):
    """
    Use this decorator to execute function only if left mouse button was used.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def track_cell_is_created(fn):
    """
    Use this decorator within Constructor view to execute function
    only if the track is displayed on constructor screen.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_track_is_in_top4(*args, **kwargs):
        if args[2] in args[0].locked_tracks_labels:
            fn(*args, **kwargs)

    return _handle_if_track_is_in_top4


def map_move_mode_available(fn):
    """
    Use this decorator within Map view to execute function only if user can move the map
    (schedule, constructor screen, etc. are not opened).

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _turn_on_move_mode_if_map_move_mode_available(*args, **kwargs):
        if args[0].map_move_mode_available and not args[0].controller.scheduler.view.is_activated \
                and not args[0].controller.constructor.view.is_activated:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_available


def map_move_mode_enabled(fn):
    """
    Use this decorator within Map view to execute function only if user is about to move the map.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _turn_on_move_mode_if_map_move_mode_enabled(*args, **kwargs):
        if args[0].map_move_mode:
            fn(*args, **kwargs)

    return _turn_on_move_mode_if_map_move_mode_enabled


def cursor_is_on_the_map(fn):
    """
    Use this decorator within Map view to execute function only if map is under the mouse cursor.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _enable_map_move_mode_if_cursor_is_on_the_map(*args, **kwargs):
        if args[1] in range(0, args[0].screen_resolution[0]) \
                and args[2] in range(args[0].bottom_bar_height, args[0].screen_resolution[1] - args[0].top_bar_height):
            fn(*args, **kwargs)

    return _enable_map_move_mode_if_cursor_is_on_the_map


def mini_map_is_not_active(fn):
    """
    Use this decorator within Map view to execute function only if mini-map is not displayed.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_mini_map_is_not_activated(*args, **kwargs):
        if not args[0].is_mini_map_activated:
            fn(*args, **kwargs)

    return _handle_if_mini_map_is_not_activated


def signal_is_displayed_on_map(fn):
    """
    Use this decorator within Signal view to execute function only if player can see this signal on the map.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _handle_if_signal_is_displayed_on_map(*args, **kwargs):
        if args[0].signal_sprite is not None:
            fn(*args, **kwargs)

    return _handle_if_signal_is_displayed_on_map


def notifications_available(fn):
    """
    Use this decorator to execute function
    only if system notifications are enabled
    (if app window is not active).

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _send_notifications_if_they_are_enabled(*args, **kwargs):
        if args[0].all_notifications_enabled:
            fn(*args, **kwargs)

    return _send_notifications_if_they_are_enabled


def level_up_notification_enabled(fn):
    """
    Use this decorator within Game view to execute function
    only if level up notifications are enabled in game settings.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _send_notification_if_level_up_notification_enabled(*args, **kwargs):
        if args[0].level_up_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_level_up_notification_enabled


def enough_money_notification_enabled(fn):
    """
    Use this decorator within Game view to execute function
    only if enough money notifications are enabled in game settings.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _send_notification_if_enough_money_notification_enabled(*args, **kwargs):
        if args[0].enough_money_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_enough_money_notification_enabled


def feature_unlocked_notification_enabled(fn):
    """
    Use this decorator within Constructor view to execute function
    only if feature unlocked notifications are enabled in game settings.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _send_notification_if_feature_unlocked_notification_enabled(*args, **kwargs):
        if args[0].feature_unlocked_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_feature_unlocked_notification_enabled


def construction_completed_notification_enabled(fn):
    """
    Use this decorator within Constructor view to execute function
    only if construction completed notifications are enabled in game settings.

    :param fn:                      function to decorate
    :return:                        decorator function
    """
    def _send_notification_if_construction_completed_notification_enabled(*args, **kwargs):
        if args[0].construction_completed_notification_enabled:
            fn(*args, **kwargs)

    return _send_notification_if_construction_completed_notification_enabled


def game_frame_opacity_exists(fn):
    def _handle_if_game_frame_opacity_is_positive(*args, **kwargs):
        if args[0].game_frame_opacity > 0:
            fn(*args, **kwargs)

    return _handle_if_game_frame_opacity_is_positive


def map_opacity_exists(fn):
    def _handle_if_map_opacity_is_positive(*args, **kwargs):
        if args[0].map_opacity > 0:
            fn(*args, **kwargs)

    return _handle_if_map_opacity_is_positive


def schedule_opacity_exists(fn):
    def _handle_if_schedule_opacity_is_positive(*args, **kwargs):
        if args[0].schedule_opacity > 0:
            fn(*args, **kwargs)

    return _handle_if_schedule_opacity_is_positive


def constructor_opacity_exists(fn):
    def _handle_if_constructor_opacity_is_positive(*args, **kwargs):
        if args[0].constructor_opacity > 0:
            fn(*args, **kwargs)

    return _handle_if_constructor_opacity_is_positive


def settings_opacity_exists(fn):
    def _handle_if_settings_opacity_is_positive(*args, **kwargs):
        if args[0].settings_opacity > 0:
            fn(*args, **kwargs)

    return _handle_if_settings_opacity_is_positive


# --------------------- CONSTANTS ---------------------
MAP_WIDTH = 8192                                # full-size map width
MAP_HEIGHT = 4096                               # full-size map height
MINI_MAP_FADE_OUT_TIMER = 1.0                   # time since user releases mouse button after which mini-map disappears
TRACKS = 0                                      # matrix #0 stores tracks state
ENVIRONMENT = 1                                 # matrix #1 stores environment tiers state
CONSTRUCTOR_VIEW_TRACK_CELLS = 4                # number of cells for tracks on constructor screen
CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS = 4          # number of cells for environment tiers on constructor screen
# ------------------- END CONSTANTS -------------------


class View:
    """
    Base class for all views in the app.
    """
    def __init__(self, logger):
        """
        Properties:
            logger                              telemetry instance
            user_db_cursor:                     user DB cursor (is used to execute user DB queries)
            config_db_cursor:                   configuration DB cursor (is used to execute configuration DB queries)
            controller                          object controller
            surface                             surface to draw all UI objects on
            batches                             batches to group all labels and sprites
            groups                              defines drawing layers (some labels and sprites behind others)
            is_activated                        indicates if view is active
            buttons                             list of all buttons on the view
            on_mouse_motion_handlers            list of on_mouse_motion event handlers to be appended
            on_mouse_press_handlers             list of on_mouse_press event handlers to be appended
            on_mouse_release_handlers           list of on_mouse_release event handlers to be appended
            on_mouse_drag_handlers              list of on_mouse_drag event handlers to be appended
            on_mouse_leave_handlers             list of on_mouse_leave event handlers to be appended
            screen_resolution                   current screen resolution
            bottom_bar_height                   height of the bottom bar with buttons
            top_bar_height                      height of the top bar
            base_offset                         current map base offset
            zoom_out_activated                  indicated if zoom out map mode is activated
            zoom_factor                         sprite scale factor
            current_locale                      current locale selected by player
            all_notifications_enabled           indicates if app can send system notifications

        :param logger:                          telemetry instance
        """
        self.logger = logger
        self.user_db_cursor = USER_DB_CURSOR
        self.config_db_cursor = CONFIG_DB_CURSOR
        self.controller = None
        self.surface = SURFACE
        self.batches = BATCHES
        self.groups = GROUPS
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
        self.user_db_cursor.execute('SELECT current_locale FROM i18n')
        self.current_locale = self.user_db_cursor.fetchone()[0]
        self.all_notifications_enabled = False

    def on_update(self):
        """
        Updates the view every frame.
        Usually it is needed for fade-in/fade-out animations
        or for some views where all sprites are not created at once
        and remaining sprites are created frame by frame to avoid massive FPS drop.
        """
        pass

    def on_activate(self):
        """
        Activates the view and creates all sprites and labels.
        """
        pass

    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        pass

    def on_assign_controller(self, controller):
        """
        Links the controller to the view and appends view handlers and all buttons handlers to the controller.

        :param controller:                      object controller
        """
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
                                           on_mouse_leave_handlers=self.on_mouse_leave_handlers)
        # appends button handlers
        self.controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                           on_mouse_press_handlers=on_mouse_press_handlers,
                                           on_mouse_release_handlers=on_mouse_release_handlers,
                                           on_mouse_leave_handlers=on_mouse_leave_handlers)

    def on_recalculate_ui_properties(self, screen_resolution):
        """
        Recalculates top and bottom bar height based on new screen resolution.

        :param screen_resolution:               new screen resolution
        """
        self.screen_resolution = screen_resolution
        self.bottom_bar_height = int(72 / 1280 * self.screen_resolution[0])
        self.top_bar_height = self.bottom_bar_height // 2

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        pass

    def on_disable_notifications(self):
        """
        Disables sending notifications from this view.
        """
        self.all_notifications_enabled = False

    def on_enable_notifications(self):
        """
        Enables sending notifications from this view.
        """
        self.all_notifications_enabled = True
