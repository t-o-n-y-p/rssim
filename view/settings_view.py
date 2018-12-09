from .view_base import View
from .button import AcceptSettingsButton


class SettingsView(View):
    def __init__(self, surface, batch, groups):
        def on_accept_settings(button):
            self.controller.on_save_and_commit_state()
            self.controller.on_deactivate()

        super().__init__(surface, batch, groups)
        self.accept_settings_button = AcceptSettingsButton(surface=self.surface, batch=self.batch, groups=self.groups,
                                                           on_click_action=on_accept_settings)
        self.buttons.append(self.accept_settings_button)

    def on_activate(self):
        self.is_activated = True
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    def on_deactivate(self):
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        self.accept_settings_button.y_margin = screen_resolution[1]
        for b in self.buttons:
            b.on_position_changed((screen_resolution[0] - b.x_margin, screen_resolution[1] - b.y_margin))
