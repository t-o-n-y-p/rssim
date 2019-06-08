from logging import getLogger

from pyglet.text import Label

from view import *
from i18n import I18N_RESOURCES


class ShopPlaceholderView(View):
    def __init__(self, map_id, shop_id):
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.lock_label = None
        self.description_label = None
        self.config_db_cursor.execute('''SELECT level_required FROM shops_config
                                         WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.level_required = self.config_db_cursor.fetchone()[0]
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
        if self.lock_label is None:
            self.lock_label = Label('', font_name='Webdings', font_size=3 * self.bottom_bar_height // 4,
                                    color=(*GREY_RGB, self.opacity), x=self.screen_resolution[0] // 2,
                                    y=self.screen_resolution[1] // 2 + self.bottom_bar_height // 2,
                                    anchor_x='center', anchor_y='center',
                                    batch=self.batches['ui_batch'], group=self.groups['button_text'])

        if self.description_label is None:
            self.description_label = Label(I18N_RESOURCES['shop_placeholder_description_string'][self.current_locale]
                                           .format(self.level_required), font_name='Arial',
                                           font_size=self.bottom_bar_height // 5,
                                           color=(*GREY_RGB, self.opacity), x=self.screen_resolution[0] // 2,
                                           y=self.screen_resolution[1] // 2 - self.top_bar_height // 2,
                                           anchor_x='center', anchor_y='center',
                                           batch=self.batches['ui_batch'], group=self.groups['button_text'])

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        if self.is_activated:
            self.lock_label.x = self.screen_resolution[0] // 2
            self.lock_label.y = self.screen_resolution[1] // 2 + self.bottom_bar_height // 2
            self.description_label.x = self.screen_resolution[0] // 2
            self.description_label.y = self.screen_resolution[1] // 2 - self.top_bar_height // 2

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
            self.lock_label.delete()
            self.lock_label = None
            self.description_label.delete()
            self.description_label = None
        else:
            self.lock_label.color = (*GREY_RGB, self.opacity)
            self.description_label.color = (*GREY_RGB, self.opacity)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.description_label.text = I18N_RESOURCES['shop_placeholder_description_string'][self.current_locale]\
                .format(self.level_required)
