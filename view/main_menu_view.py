from logging import getLogger

from pyglet.text import Label
from pyglet.gl import GL_QUADS
from pyshaders import from_files_names

from view import *
from ui.button.create_station_button import CreateStationButton
from ui.button.open_license_button import OpenLicenseButton
from i18n import I18N_RESOURCES


class MainMenuView(View):
    def __init__(self):
        def on_create_station(button):
            button.on_deactivate()
            self.controller.on_deactivate()
            self.controller.parent_controller.on_resume_game()
            self.controller.parent_controller.on_activate_game_view()

        def on_open_license(button):
            button.on_deactivate()
            self.controller.parent_controller.on_open_license()

        super().__init__(logger=getLogger('root.app.main_menu.view'))
        self.create_station_button = CreateStationButton(on_click_action=on_create_station)
        self.open_license_button = OpenLicenseButton(on_click_action=on_open_license)
        self.buttons = [self.create_station_button, self.open_license_button]
        self.create_station_button_label = None
        self.shader = from_files_names('shaders/shader.vert', 'shaders/main_menu_view/shader.frag')
        self.shader_sprite = None
        self.on_init_graphics()

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)

    def on_update(self):
        self.on_update_opacity()
        for b in self.buttons:
            b.on_update_opacity()

    def on_update_sprite_opacity(self):
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.shader_sprite = None
            self.create_station_button_label.delete()
            self.create_station_button_label = None
        else:
            self.create_station_button_label.color = (*WHITE_RGB, self.opacity)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        if self.shader_sprite is None:
            self.shader_sprite\
                = self.batches['main_frame'].add(4, GL_QUADS, self.groups['main_frame'],
                                                 ('v2f/static', (-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, 1.0, -1.0)))

        if self.create_station_button_label is None:
            self.create_station_button_label \
                = Label(I18N_RESOURCES['create_station_label_string'][self.current_locale],
                        font_name='Perfo', bold=True, font_size=3 * self.bottom_bar_height // 8,
                        color=(*WHITE_RGB, self.opacity), x=self.screen_resolution[0] // 2,
                        y=self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4,
                        anchor_x='center', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        medium_line = self.screen_resolution[1] // 2 + int(72 / 1280 * self.screen_resolution[0]) // 4
        if self.is_activated:
            self.create_station_button_label.x = self.screen_resolution[0] // 2
            self.create_station_button_label.y = medium_line
            self.create_station_button_label.font_size = 3 * self.bottom_bar_height // 8

        self.open_license_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.create_station_button.on_size_changed((self.bottom_bar_height * 7, self.bottom_bar_height))
        self.create_station_button.x_margin = self.screen_resolution[0] // 2 - self.bottom_bar_height * 7 // 2
        self.create_station_button.y_margin = medium_line - self.bottom_bar_height // 2
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.create_station_button_label.text = I18N_RESOURCES['create_station_label_string'][self.current_locale]

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.main_menu_opacity = self.opacity
        is_button_activated = []
        button_x = []
        button_y = []
        button_w = []
        button_h = []
        for b in self.buttons:
            is_button_activated.append(int(b.is_activated))
            button_x.append(b.position[0])
            button_y.append(b.position[1])
            button_w.append(b.button_size[0])
            button_h.append(b.button_size[1])

        self.shader.uniforms.is_button_activated = is_button_activated
        self.shader.uniforms.button_x = button_x
        self.shader.uniforms.button_y = button_y
        self.shader.uniforms.button_w = button_w
        self.shader.uniforms.button_h = button_h
        self.shader.uniforms.number_of_buttons = len(self.buttons)
        self.shader_sprite.draw(GL_QUADS)
        self.shader.clear()
