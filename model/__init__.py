def model_is_active(fn):
    def _handle_if_model_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_activated


def model_is_not_active(fn):
    def _handle_if_model_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_model_is_not_activated


def fullscreen_mode_available(fn):
    def _turn_fullscren_mode_on_if_available(*args, **kwargs):
        if args[0].fullscreen_mode_available:
            fn(*args, **kwargs)

    return _turn_fullscren_mode_on_if_available


def maximum_money_not_reached(fn):
    def _add_money_if_maximum_money_is_not_reached(*args, **kwargs):
        if args[0].money < 99999999.0:
            fn(*args, **kwargs)

    return _add_money_if_maximum_money_is_not_reached


def maximum_level_not_reached(fn):
    def _add_exp_if_max_level_not_reached(*args, **kwargs):
        if args[0].level < args[0].maximum_level:
            fn(*args, **kwargs)

    return _add_exp_if_max_level_not_reached


def money_target_exists(fn):
    def _update_money_progress_if_money_target_exists(*args, **kwargs):
        if args[0].money_target > 0:
            fn(*args, **kwargs)

    return _update_money_progress_if_money_target_exists


def train_has_passed_train_route_section(fn):
    def _allow_other_trains_to_pass_if_train_has_passed_train_route_section(*args, **kwargs):
        if args[1] >= args[0].checkpoints_v2[args[0].current_checkpoint]:
            fn(*args, **kwargs)

    return _allow_other_trains_to_pass_if_train_has_passed_train_route_section


def train_route_is_opened(fn):
    def _handle_if_train_route_is_opened(*args, **kwargs):
        if args[0].opened:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_opened


def not_approaching_route(fn):
    def _handle_if_train_route_is_not_approaching_route(*args, **kwargs):
        if len(args[0].train_route_sections) > 1:
            fn(*args, **kwargs)

    return _handle_if_train_route_is_not_approaching_route


class Model:
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        self.view = None
        self.controller = None
        self.is_activated = False
        self.user_db_connection = user_db_connection
        self.user_db_cursor = user_db_cursor
        self.config_db_cursor = config_db_cursor

    def on_activate(self):
        pass

    def on_deactivate(self):
        pass

    def on_save_state(self):
        pass
