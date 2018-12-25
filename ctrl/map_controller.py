from operator import attrgetter

from .controller_base import Controller


def _controller_is_active(fn):
    def _handle_if_controller_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_activated


def _controller_is_not_active(fn):
    def _handle_if_controller_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_controller_is_not_activated


def _map_view_is_active(fn):
    def _handle_if_map_view_is_activated(*args, **kwargs):
        if args[0].view.is_activated:
            fn(*args, **kwargs)

    return _handle_if_map_view_is_activated


class MapController(Controller):
    def __init__(self, game_controller):
        super().__init__(parent_controller=game_controller)
        self.scheduler = None
        self.signals = {}
        self.signals_list = []
        self.train_routes = {}
        self.train_routes_sorted_list = []

    def on_update_view(self):
        self.view.on_update()
        self.scheduler.on_update_view()
        for signal in self.signals_list:
            signal.on_update_view()

        # for route in self.train_routes_sorted_list:
        #     route.on_update_view()

    @_controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.scheduler.on_activate()
        for signal in self.signals_list:
            signal.on_activate()

        for route in self.train_routes_sorted_list:
            route.on_activate()

    @_controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.scheduler.on_deactivate()
        for signal in self.signals_list:
            signal.on_deactivate()

        for route in self.train_routes_sorted_list:
            route.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        self.scheduler.on_change_screen_resolution(screen_resolution)
        for signal in self.signals_list:
            signal.on_change_screen_resolution(screen_resolution)

        # for route in self.train_routes_sorted_list:
        #     route.on_change_screen_resolution(screen_resolution)

        self.on_change_base_offset(self.view.base_offset)

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)
        for signal in self.signals_list:
            signal.on_change_base_offset(new_base_offset)

        # for route in self.train_routes_sorted_list:
        #     route.on_change_base_offset(new_base_offset)

    def on_unlock_track(self, track_number):
        self.model.on_unlock_track(track_number)
        self.scheduler.on_unlock_track(track_number)
        for i in self.signals[track_number]:
            self.signals[track_number][i].on_unlock()

    def on_activate_view(self):
        self.view.on_activate()
        for signal in self.signals_list:
            signal.on_activate_view()

        # for route in self.train_routes_sorted_list:
        #     route.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.scheduler.on_deactivate_view()
        for signal in self.signals_list:
            signal.on_deactivate_view()

        # for route in self.train_routes_sorted_list:
        #     route.on_deactivate_view()

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)
        for signal in self.signals_list:
            signal.on_zoom_in()

        # for route in self.train_routes_sorted_list:
        #     route.on_zoom_in()

        self.on_change_base_offset(self.view.base_offset)

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)
        for signal in self.signals_list:
            signal.on_zoom_out()

        # for route in self.train_routes_sorted_list:
        #     route.on_zoom_out()

        self.on_change_base_offset(self.view.base_offset)

    def on_save_state(self):
        self.model.on_save_state()
        self.scheduler.on_save_state()
        for signal in self.signals_list:
            signal.on_save_state()

        for route in self.train_routes_sorted_list:
            route.on_save_state()

    def on_update_time(self, game_time):
        self.train_routes_sorted_list = sorted(self.train_routes_sorted_list,
                                               key=attrgetter('model.priority'), reverse=True)
        for route in self.train_routes_sorted_list:
            route.on_update_time(game_time)

        self.scheduler.on_update_time(game_time)

    def on_level_up(self):
        self.scheduler.on_level_up()

    def on_open_schedule(self):
        self.scheduler.on_activate_view()
        self.view.on_deactivate_zoom_buttons()

    @_map_view_is_active
    def on_close_schedule(self):
        self.view.on_activate_zoom_buttons()
        self.view.open_schedule_button.on_activate()

    def on_switch_signal_to_green(self, signal_track, signal_base_route):
        self.signals[signal_track][signal_base_route].on_switch_to_green()

    def on_switch_signal_to_red(self, signal_track, signal_base_route):
        self.signals[signal_track][signal_base_route].on_switch_to_red()
