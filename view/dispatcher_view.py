from .view_base import View


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


class DispatcherView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.base_offset = (-3440, -1440)
        self.screen_resolution = (1280, 720)
        self.zoom_out_activated = False
        self.zoom_factor = 1.0

    def on_update(self):
        pass

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
