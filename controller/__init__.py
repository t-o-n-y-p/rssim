from abc import ABC, abstractmethod
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
SECTION_TYPE: Final = 0                        # meaning of section[] list's element 0
SECTION_TRACK_NUMBER_1: Final = 1              # meaning of section[] list's element 1
SECTION_TRACK_NUMBER_2: Final = 2              # meaning of section[] list's element 2
TRAIN_ROUTE_DATA_TRACK_NUMBER: Final = 0       # meaning of train_route_data[] list's element 0
TRAIN_ROUTE_DATA_TYPE: Final = 1               # meaning of train_route_data[] list's element 1
TRAIN_ROUTE_DATA_SECTION_NUMBER: Final = 2     # meaning of train_route_data[] list's element 2
# ------------------- END CONSTANTS -------------------


class AppBaseController(ABC):
    def __init__(self, parent_controller=None, logger=None):
        self.parent_controller = parent_controller
        self.logger = logger
        self.view = None
        self.model = None
        self.fade_in_animation = None
        self.fade_out_animation = None
        self.is_activated = False
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.on_mouse_scroll_handlers = []
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.on_window_resize_handlers = []
        self.on_window_activate_handlers = []
        self.on_window_show_handlers = []
        self.on_window_deactivate_handlers = []
        self.on_window_hide_handlers = []
        self.child_controllers = []

    def on_update_current_locale(self, new_locale):
        self.view.on_update_current_locale(new_locale)
        for controller in self.child_controllers:
            controller.on_update_current_locale(new_locale)

    def on_save_state(self):
        self.model.on_save_state()
        for controller in self.child_controllers:
            controller.on_save_state()

    def on_update_clock_state(self, clock_24h_enabled):
        self.view.on_update_clock_state(clock_24h_enabled)
        for controller in self.child_controllers:
            controller.on_update_clock_state(clock_24h_enabled)

    @final
    def on_activate_view(self):
        self.view.on_activate()

    @final
    def on_update_view(self):
        self.view.on_update()
        for controller in self.child_controllers:
            controller.on_update_view()

    @final
    def on_fade_animation_update(self, dt):
        self.fade_in_animation.on_update(dt)
        self.fade_out_animation.on_update(dt)
        for controller in self.child_controllers:
            controller.on_fade_animation_update(dt)

    @final
    def on_apply_shaders_and_draw_vertices(self):
        self.view.on_apply_shaders_and_draw_vertices()
        for controller in self.child_controllers:
            controller.on_apply_shaders_and_draw_vertices()

    @final
    def on_disable_notifications(self):
        self.view.on_disable_notifications()
        for controller in self.child_controllers:
            controller.on_disable_notifications()

    @final
    def on_enable_notifications(self):
        self.view.on_enable_notifications()
        for controller in self.child_controllers:
            controller.on_enable_notifications()

    @final
    def on_change_level_up_notification_state(self, notification_state):
        self.view.on_change_level_up_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_level_up_notification_state(notification_state)

    @final
    def on_change_feature_unlocked_notification_state(self, notification_state):
        self.view.on_change_feature_unlocked_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_feature_unlocked_notification_state(notification_state)

    @final
    def on_change_construction_completed_notification_state(self, notification_state):
        self.view.on_change_construction_completed_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_construction_completed_notification_state(notification_state)

    @final
    def on_change_enough_money_notification_state(self, notification_state):
        self.view.on_change_enough_money_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_enough_money_notification_state(notification_state)

    @final
    def on_change_bonus_expired_notification_state(self, notification_state):
        self.view.on_change_bonus_expired_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_bonus_expired_notification_state(notification_state)

    @final
    def on_change_shop_storage_notification_state(self, notification_state):
        self.view.on_change_shop_storage_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_shop_storage_notification_state(notification_state)

    @final
    def on_change_voice_not_found_notification_state(self, notification_state):
        self.view.on_change_voice_not_found_notification_state(notification_state)
        for controller in self.child_controllers:
            controller.on_change_voice_not_found_notification_state(notification_state)

    @final
    def on_clear_all_notifications(self):
        self.view.on_clear_all_notifications()
        for controller in self.child_controllers:
            controller.on_clear_all_notifications()

    @final
    def on_update_fade_animation_state(self, new_state):
        self.fade_in_animation.on_update_fade_animation_state(new_state)
        self.fade_out_animation.on_update_fade_animation_state(new_state)
        for controller in self.child_controllers:
            controller.on_update_fade_animation_state(new_state)

    @final
    def on_append_view_handlers(
            self, on_mouse_motion_handlers=(), on_mouse_press_handlers=(), on_mouse_release_handlers=(),
            on_mouse_drag_handlers=(), on_mouse_leave_handlers=(), on_mouse_scroll_handlers=(),
            on_key_press_handlers=(), on_text_handlers=()
    ):
        self.on_mouse_motion_handlers.extend(on_mouse_motion_handlers)
        self.on_mouse_press_handlers.extend(on_mouse_press_handlers)
        self.on_mouse_release_handlers.extend(on_mouse_release_handlers)
        self.on_mouse_drag_handlers.extend(on_mouse_drag_handlers)
        self.on_mouse_leave_handlers.extend(on_mouse_leave_handlers)
        self.on_mouse_scroll_handlers.extend(on_mouse_scroll_handlers)
        self.on_key_press_handlers.extend(on_key_press_handlers)
        self.on_text_handlers.extend(on_text_handlers)

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        try:
            self.parent_controller.on_append_view_handlers(
                on_mouse_motion_handlers=on_mouse_motion_handlers,
                on_mouse_press_handlers=on_mouse_press_handlers,
                on_mouse_release_handlers=on_mouse_release_handlers,
                on_mouse_drag_handlers=on_mouse_drag_handlers,
                on_mouse_leave_handlers=on_mouse_leave_handlers,
                on_mouse_scroll_handlers=on_mouse_scroll_handlers,
                on_key_press_handlers=on_key_press_handlers,
                on_text_handlers=on_text_handlers
            )
        except AttributeError:
            pass

    @final
    def on_detach_view_handlers(
            self, on_mouse_motion_handlers=(), on_mouse_press_handlers=(), on_mouse_release_handlers=(),
            on_mouse_drag_handlers=(), on_mouse_leave_handlers=(), on_mouse_scroll_handlers=(),
            on_key_press_handlers=(), on_text_handlers=()
    ):
        for handler in on_mouse_motion_handlers:
            self.on_mouse_motion_handlers.remove(handler)

        for handler in on_mouse_press_handlers:
            self.on_mouse_press_handlers.remove(handler)

        for handler in on_mouse_release_handlers:
            self.on_mouse_release_handlers.remove(handler)

        for handler in on_mouse_drag_handlers:
            self.on_mouse_drag_handlers.remove(handler)

        for handler in on_mouse_leave_handlers:
            self.on_mouse_leave_handlers.remove(handler)

        for handler in on_mouse_scroll_handlers:
            self.on_mouse_scroll_handlers.remove(handler)

        for handler in on_key_press_handlers:
            self.on_key_press_handlers.remove(handler)

        for handler in on_text_handlers:
            self.on_text_handlers.remove(handler)

        # little recursive pattern there: it stops as soon as reaches
        # App object controller (App object does not have parent objects)
        try:
            self.parent_controller.on_detach_view_handlers(
                on_mouse_motion_handlers=on_mouse_motion_handlers,
                on_mouse_press_handlers=on_mouse_press_handlers,
                on_mouse_release_handlers=on_mouse_release_handlers,
                on_mouse_drag_handlers=on_mouse_drag_handlers,
                on_mouse_leave_handlers=on_mouse_leave_handlers,
                on_mouse_scroll_handlers=on_mouse_scroll_handlers,
                on_key_press_handlers=on_key_press_handlers,
                on_text_handlers=on_text_handlers
            )
        except AttributeError:
            pass

    @final
    def on_append_window_handlers(
            self, on_window_resize_handlers=(), on_window_activate_handlers=(), on_window_show_handlers=(),
            on_window_deactivate_handlers=(), on_window_hide_handlers=()
    ):
        self.on_window_resize_handlers.extend(on_window_resize_handlers)
        self.on_window_activate_handlers.extend(on_window_activate_handlers)
        self.on_window_show_handlers.extend(on_window_show_handlers)
        self.on_window_deactivate_handlers.extend(on_window_deactivate_handlers)
        self.on_window_hide_handlers.extend(on_window_hide_handlers)
        try:
            self.parent_controller.on_append_window_handlers(
                on_window_resize_handlers=on_window_resize_handlers,
                on_window_activate_handlers=on_window_activate_handlers,
                on_window_show_handlers=on_window_show_handlers,
                on_window_deactivate_handlers=on_window_deactivate_handlers,
                on_window_hide_handlers=on_window_hide_handlers
            )
        except AttributeError:
            pass

    @final
    def on_detach_window_handlers(
            self, on_window_resize_handlers=(), on_window_activate_handlers=(), on_window_show_handlers=(),
            on_window_deactivate_handlers=(), on_window_hide_handlers=()
    ):
        for handler in on_window_resize_handlers:
            self.on_window_resize_handlers.remove(handler)

        for handler in on_window_activate_handlers:
            self.on_window_activate_handlers.remove(handler)

        for handler in on_window_show_handlers:
            self.on_window_show_handlers.remove(handler)

        for handler in on_window_deactivate_handlers:
            self.on_window_deactivate_handlers.remove(handler)

        for handler in on_window_hide_handlers:
            self.on_window_hide_handlers.remove(handler)

        try:
            self.parent_controller.on_detach_window_handlers(
                on_window_resize_handlers=on_window_resize_handlers,
                on_window_activate_handlers=on_window_activate_handlers,
                on_window_show_handlers=on_window_show_handlers,
                on_window_deactivate_handlers=on_window_deactivate_handlers,
                on_window_hide_handlers=on_window_hide_handlers
            )
        except AttributeError:
            pass


class GameBaseController(AppBaseController, ABC):
    def __init__(self, parent_controller=None, logger=None):
        super().__init__(parent_controller, logger)

    def on_update_time(self, dt):
        self.model.on_update_time(dt)
        for controller in self.child_controllers:
            controller.on_update_time(dt)

    def on_level_up(self):
        self.model.on_level_up()
        for controller in self.child_controllers:
            controller.on_level_up()

    @final
    def on_dt_multiplier_update(self, dt_multiplier):
        self.model.on_dt_multiplier_update(dt_multiplier)
        for controller in self.child_controllers:
            controller.on_dt_multiplier_update(dt_multiplier)

    @final
    def on_add_money(self, money):
        self.model.on_add_money(money)
        for controller in self.child_controllers:
            controller.on_add_money(money)

    @final
    def on_pay_money(self, money):
        self.model.on_pay_money(money)
        for controller in self.child_controllers:
            controller.on_pay_money(money)

    @final
    def on_activate_exp_bonus_code(self, value):
        self.model.on_activate_exp_bonus_code(value)
        for controller in self.child_controllers:
            controller.on_activate_exp_bonus_code(value)

    @final
    def on_activate_money_bonus_code(self, value):
        self.model.on_activate_money_bonus_code(value)
        for controller in self.child_controllers:
            controller.on_activate_money_bonus_code(value)

    @final
    def on_activate_construction_speed_bonus_code(self, value):
        self.model.on_activate_construction_speed_bonus_code(value)
        for controller in self.child_controllers:
            controller.on_activate_construction_speed_bonus_code(value)

    @final
    def on_deactivate_exp_bonus_code(self):
        self.model.on_deactivate_exp_bonus_code()
        for controller in self.child_controllers:
            controller.on_deactivate_exp_bonus_code()

    @final
    def on_deactivate_money_bonus_code(self):
        self.model.on_deactivate_money_bonus_code()
        for controller in self.child_controllers:
            controller.on_deactivate_money_bonus_code()

    @final
    def on_deactivate_construction_speed_bonus_code(self):
        self.model.on_deactivate_construction_speed_bonus_code()
        for controller in self.child_controllers:
            controller.on_deactivate_construction_speed_bonus_code()


class MapBaseController(GameBaseController, ABC):
    def __init__(self, map_id, parent_controller=None, logger=None):
        super().__init__(parent_controller, logger)
        self.map_id = map_id
        self.map_element_controllers = []

    @abstractmethod
    def create_view_and_model(self, *args, **kwargs):
        pass

    def on_unlock(self):
        self.model.on_unlock()
