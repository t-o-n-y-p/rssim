from logging import getLogger

from view import *
from ui.button.close_shop_details_button import CloseShopDetailsButton
from ui.label.shop_title_label import ShopTitleLabel
from ui.shader_sprite.shop_view_shader_sprite import ShopViewShaderSprite


class ShopView(View):
    def __init__(self, map_id, shop_id):
        def on_close_shop_details(button):
            self.controller.parent_controller.on_close_shop_details(self.shop_id)

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.user_db_cursor.execute('''SELECT last_known_shop_window_position FROM graphics''')
        self.viewport.x1, self.viewport.y1 = tuple(map(int, self.user_db_cursor.fetchone()[0].split(',')))
        self.viewport.x2 = self.viewport.x1 + self.inner_area_size[0]
        self.viewport.y2 = self.viewport.y1 + self.inner_area_size[1]
        self.shader_sprite = ShopViewShaderSprite(view=self)
        self.title_label = ShopTitleLabel(parent_viewport=self.viewport)
        self.title_label.on_update_args((self.shop_id + 1, ))
        self.close_shop_details_button = CloseShopDetailsButton(on_click_action=on_close_shop_details)
        self.buttons = [self.close_shop_details_button, ]
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
        self.shader_sprite.create()
        self.title_label.create()
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
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.viewport.x1 = self.inner_area_position[0]
        self.viewport.y1 = self.inner_area_position[1]
        self.viewport.x2 = self.viewport.x1 + self.inner_area_size[0]
        self.viewport.y2 = self.viewport.y1 + self.inner_area_size[1]
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        self.close_shop_details_button.on_size_changed((self.top_bar_height, self.top_bar_height))
        self.close_shop_details_button.x_margin = self.viewport.x2 - self.top_bar_height
        self.close_shop_details_button.y_margin = self.viewport.y2 - self.top_bar_height
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader_sprite.draw()

    def on_update_opacity(self, new_opacity):
        """
        Updates view opacity with given value.

        :param new_opacity:                     new opacity value
        """
        self.opacity = new_opacity
        self.on_update_sprite_opacity()
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        """
        Applies new opacity value to all sprites and labels.
        """
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.title_label.delete()
        else:
            self.title_label.on_update_opacity(self.opacity)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.title_label.on_update_current_locale(self.current_locale)
