from logging import getLogger

from pyglet.gl import GL_QUADS
from pyshaders import from_files_names

from view import *
from ui.page_control.license_page_control import LicensePageControl
from ui.button.close_license_button import CloseLicenseButton


class LicenseView(View):
    def __init__(self):
        def on_close_license(button):
            self.controller.on_deactivate_view()

        super().__init__(logger=getLogger('root.app.main_menu.license.view'))
        self.license_page_control = LicensePageControl(current_locale=self.current_locale)
        self.close_license_button = CloseLicenseButton(on_click_action=on_close_license)
        self.buttons = [*self.license_page_control.buttons, self.close_license_button]
        self.on_init_graphics()

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)

    def on_update(self):
        """
        Updates fade-in/fade-out animations.
        """
        if self.is_activated and self.opacity < 255:
            self.opacity += 15

        if not self.is_activated and self.opacity > 0:
            self.opacity -= 15

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.license_page_control.on_activate()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.license_page_control.on_deactivate()
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.license_page_control.on_change_screen_resolution(screen_resolution)
        self.close_license_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.license_page_control.on_update_current_locale(new_locale)
