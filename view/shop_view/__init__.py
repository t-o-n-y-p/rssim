from logging import getLogger

from pyshaders import from_files_names
from pyglet.gl import GL_QUADS
from pyglet.text import Label

from view import *
from i18n import I18N_RESOURCES


class ShopView(View):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.shop_details_window_position = (0, 0)
        self.shop_details_window_size = (0, 0)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/shop_view/shader.frag')
        self.shader_sprite = None
        self.shop_view_shader_bottom_limit = 0.0
        self.shop_view_shader_upper_limit = 0.0
        self.title_label = None
        self.on_init_graphics()

    def on_init_graphics(self):
        """
        Initializes the view based on saved screen resolution and base offset.
        """
        self.on_change_screen_resolution(self.screen_resolution)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        if self.shader_sprite is None:
            self.shader_sprite \
                = self.batches['main_frame'].add(4, GL_QUADS, self.groups['main_frame'],
                                                 ('v2f/static', (-1.0, self.shop_view_shader_bottom_limit,
                                                                 -1.0, self.shop_view_shader_upper_limit,
                                                                 1.0, self.shop_view_shader_upper_limit,
                                                                 1.0, self.shop_view_shader_bottom_limit)))

        if self.title_label is None:
            self.title_label = Label(I18N_RESOURCES['shop_details_title_string'][self.current_locale]
                                     .format(self.shop_id + 1),
                                     font_name='Arial', font_size=int(16 / 40 * self.top_bar_height),
                                     color=(*WHITE_RGB, self.opacity),
                                     x=self.shop_details_window_position[0] + self.top_bar_height // 4,
                                     y=self.shop_details_window_position[1] + self.shop_details_window_size[1]
                                       - self.top_bar_height // 2,
                                     anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                     group=self.groups['button_text'])

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.shop_view_shader_bottom_limit = self.bottom_bar_height / self.screen_resolution[1] * 2 - 1
        self.shop_view_shader_upper_limit = 1 - self.top_bar_height / self.screen_resolution[1] * 2
        self.shop_details_window_size = (int(6.875 * self.bottom_bar_height) * 2 + self.bottom_bar_height // 4,
                                         19 * self.bottom_bar_height // 4)
        self.shop_details_window_position = ((self.screen_resolution[0] - self.shop_details_window_size[0]) // 2,
                                             (self.screen_resolution[1] - self.shop_details_window_size[1]
                                              - 3 * self.bottom_bar_height // 2) // 2 + self.bottom_bar_height)
        if self.is_activated:
            self.title_label.x = self.shop_details_window_position[0] + self.top_bar_height // 4
            self.title_label.y = self.shop_details_window_position[1] + self.shop_details_window_size[1] \
                                 - self.top_bar_height // 2
            self.title_label.font_size = int(16 / 40 * self.top_bar_height)

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.shop_window_opacity = self.opacity
        self.shader.uniforms.shop_window_position = self.shop_details_window_position
        self.shader.uniforms.shop_window_size = self.shop_details_window_size
        self.shader.uniforms.top_bar_height = self.top_bar_height
        self.shader_sprite.draw(GL_QUADS)
        self.shader.clear()

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.shader_sprite = None
            self.title_label.delete()
            self.title_label = None
        else:
            self.title_label.color = (*WHITE_RGB, self.opacity)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.title_label.text = I18N_RESOURCES['shop_details_title_string'][self.current_locale]\
                .format(self.shop_id + 1)
