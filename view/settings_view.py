from .view_base import View
from .button import AcceptSettingsButton, RejectSettingsButton


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


class SettingsView(View):
    def __init__(self, surface, batch, groups):
        def on_accept_settings(button):
            self.controller.on_save_and_commit_state()
            self.controller.on_deactivate()

        def on_reject_settings(button):
            self.controller.on_deactivate()

        super().__init__(surface, batch, groups)
        self.temp_windowed_resolution = (0, 0)
        self.temp_fullscreen_mode = False
        self.available_windowed_resolutions = []
        self.available_windowed_resolutions_position = 0
        self.accept_settings_button = AcceptSettingsButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                           on_click_action=on_accept_settings)
        self.buttons.append(self.accept_settings_button)
        self.reject_settings_button = RejectSettingsButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                           on_click_action=on_reject_settings)
        self.buttons.append(self.reject_settings_button)

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.accept_settings_button.y_margin = screen_resolution[1]
        self.reject_settings_button.y_margin = screen_resolution[1]
        for b in self.buttons:
            b.on_position_changed((screen_resolution[0] - b.x_margin, screen_resolution[1] - b.y_margin))

    def on_change_temp_windowed_resolution(self, windowed_resolution):
        self.temp_windowed_resolution = windowed_resolution

    def on_change_temp_fullscreen_mode(self, fullscreen_mode):
        self.temp_fullscreen_mode = fullscreen_mode

    def on_change_available_windowed_resolutions(self, available_windowed_resolutions):
        self.available_windowed_resolutions = available_windowed_resolutions
        self.available_windowed_resolutions_position \
            = self.available_windowed_resolutions.index(self.temp_windowed_resolution)
