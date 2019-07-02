from logging import getLogger

from view import *
from ui.page_control.license_page_control import LicensePageControl
from ui.button.close_license_button import CloseLicenseButton
from ui.shader_sprite.license_view_shader_sprite import LicenseViewShaderSprite


class LicenseView(View):
    """
    Implements License view.
    License object is responsible for properties, UI and events related to the license screen.
    """
    def __init__(self):
        """
        Button click handlers:
            on_close_license                    on_click handler for close license button

        Properties:
            license_page_control                LicensePageControl object
            close_license_button                CloseLicenseButton object
            buttons                             list of all buttons

        """
        def on_close_license(button):
            """
            Notifies the controller to deactivate the view.

            :param button:                      button that was clicked
            """
            self.controller.parent_controller.on_close_license()

        super().__init__(logger=getLogger('root.app.license.view'))
        self.license_page_control = LicensePageControl()
        self.close_license_button = CloseLicenseButton(on_click_action=on_close_license)
        self.buttons = [*self.license_page_control.buttons, self.close_license_button]
        self.shader_sprite = LicenseViewShaderSprite(view=self)
        self.on_mouse_scroll_handlers = self.license_page_control.on_mouse_scroll_handlers
        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        self.license_page_control.on_update_opacity(new_opacity)
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.shader_sprite.create()
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
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
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

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader_sprite.draw()
