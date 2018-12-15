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
        self.signals = ()

    def on_update_view(self):
        self.view.on_update()
        self.scheduler.on_update_view()
        for s in self.signals:
            s.on_update_view()

    @_controller_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.model.on_activate()
        self.scheduler.on_activate()
        for s in self.signals:
            s.on_activate()

    @_controller_is_active
    def on_deactivate(self):
        self.is_activated = False
        self.model.on_deactivate()
        self.view.on_deactivate()
        self.scheduler.on_deactivate()
        for s in self.signals:
            s.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.view.on_change_screen_resolution(screen_resolution)
        self.scheduler.on_change_screen_resolution(screen_resolution)
        for s in self.signals:
            s.on_change_screen_resolution(screen_resolution)

    def on_change_base_offset(self, new_base_offset):
        self.view.on_change_base_offset(new_base_offset)
        for s in self.signals:
            s.on_change_base_offset(new_base_offset)

    def on_unlock_track(self, track_number):
        self.model.on_unlock_track(track_number)
        self.scheduler.on_unlock_track(track_number)
        for s in self.signals:
            s.on_unlock(track_number)

    def on_activate_view(self):
        self.view.on_activate()
        for s in self.signals:
            s.on_activate_view()

    def on_deactivate_view(self):
        self.view.on_deactivate()
        self.scheduler.on_deactivate_view()
        for s in self.signals:
            s.on_deactivate_view()

    def on_zoom_in(self):
        self.view.on_change_zoom_factor(1.0, zoom_out_activated=False)
        for s in self.signals:
            s.on_zoom_in()

    def on_zoom_out(self):
        self.view.on_change_zoom_factor(0.5, zoom_out_activated=True)
        for s in self.signals:
            s.on_zoom_out()

    def on_save_state(self):
        self.model.on_save_state()
        self.scheduler.on_save_state()
        for s in self.signals:
            s.on_save_state()

    def on_update_time(self, game_time):
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
