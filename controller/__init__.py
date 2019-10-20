from typing import Final, final


def view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].view.is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].view.is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


def game_is_not_paused(fn):
    def _update_if_game_is_not_paused(*args, **kwargs):
        if not args[0].model.game_paused:
            fn(*args, **kwargs)

    return _update_if_game_is_not_paused


def map_view_is_active(fn):
    def _handle_if_map_view_is_activated(*args, **kwargs):
        if args[0].view.is_activated:
            fn(*args, **kwargs)

    return _handle_if_map_view_is_activated


# --------------------- CONSTANTS ---------------------
FRAMES_IN_ONE_HOUR: Final = 14400              # number of frames in 1 in-game hour
ZOOM_OUT_SCALE_FACTOR: Final = 0.5             # how much to scale all sprites when map is zoomed out
ZOOM_IN_SCALE_FACTOR: Final = 1.0              # how much to scale all sprites when map is zoomed in
SECTION_TYPE: Final = 0                        # meaning of section[] list's element 0
SECTION_TRACK_NUMBER_1: Final = 1              # meaning of section[] list's element 1
SECTION_TRACK_NUMBER_2: Final = 2              # meaning of section[] list's element 2
TRAIN_ROUTE_DATA_TRACK_NUMBER: Final = 0       # meaning of train_route_data[] list's element 0
TRAIN_ROUTE_DATA_TYPE: Final = 1               # meaning of train_route_data[] list's element 1
TRAIN_ROUTE_DATA_SECTION_NUMBER: Final = 2     # meaning of train_route_data[] list's element 2
# ------------------- END CONSTANTS -------------------


class AppBaseController:
    def __init__(self, parent_controller=None, logger=None):
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
        self.on_mouse_scroll_handlers = []
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.fade_in_animation = None
        self.fade_out_animation = None

    def on_activate_view(self):
        self.model.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()

    def on_update_view(self):
        self.view.on_update()
        self.fade_in_animation.on_update()
        self.fade_out_animation.on_update()

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)

    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()

    def on_disable_notifications(self):
        self.view.on_disable_notifications()

    def on_enable_notifications(self):
        self.view.on_enable_notifications()

    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)

    def on_save_state(self):
        self.model.on_save_state()

    @final
    def on_append_handlers(self, on_mouse_motion_handlers=None, on_mouse_press_handlers=None,
                           on_mouse_release_handlers=None, on_mouse_drag_handlers=None,
                           on_mouse_leave_handlers=None, on_mouse_scroll_handlers=None,
                           on_key_press_handlers=None, on_text_handlers=None):
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

        if on_mouse_scroll_handlers is not None:
            self.on_mouse_scroll_handlers.extend(on_mouse_scroll_handlers)

        if on_key_press_handlers is not None:
            self.on_key_press_handlers.extend(on_key_press_handlers)

        if on_text_handlers is not None:
            self.on_text_handlers.extend(on_text_handlers)

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        if self.parent_controller is not None:
            self.parent_controller.on_append_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers,
                                                      on_mouse_scroll_handlers=on_mouse_scroll_handlers,
                                                      on_key_press_handlers=on_key_press_handlers,
                                                      on_text_handlers=on_text_handlers)

    @final
    def on_detach_handlers(self, on_mouse_motion_handlers=None, on_mouse_press_handlers=None,
                           on_mouse_release_handlers=None, on_mouse_drag_handlers=None,
                           on_mouse_leave_handlers=None, on_mouse_scroll_handlers=None,
                           on_key_press_handlers=None, on_text_handlers=None):
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

        if on_mouse_scroll_handlers is not None:
            for handler in on_mouse_scroll_handlers:
                self.on_mouse_scroll_handlers.remove(handler)

        if on_key_press_handlers is not None:
            for handler in on_key_press_handlers:
                self.on_key_press_handlers.remove(handler)

        if on_text_handlers is not None:
            for handler in on_text_handlers:
                self.on_text_handlers.remove(handler)

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        if self.parent_controller is not None:
            self.parent_controller.on_detach_handlers(on_mouse_motion_handlers=on_mouse_motion_handlers,
                                                      on_mouse_press_handlers=on_mouse_press_handlers,
                                                      on_mouse_release_handlers=on_mouse_release_handlers,
                                                      on_mouse_drag_handlers=on_mouse_drag_handlers,
                                                      on_mouse_leave_handlers=on_mouse_leave_handlers,
                                                      on_mouse_scroll_handlers=on_mouse_scroll_handlers,
                                                      on_key_press_handlers=on_key_press_handlers,
                                                      on_text_handlers=on_text_handlers)


class GameBaseController:
    def __init__(self):
        self.model = None

    def on_update_time(self):
        self.model.on_update_time()

    def on_level_up(self):
        self.model.on_level_up()
