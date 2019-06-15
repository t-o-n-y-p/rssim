from logging import getLogger

from pyshaders import from_files_names
from pyglet.gl import GL_QUADS
from pyglet.text import Label
from pyglet.image import load
from pyglet.sprite import Sprite

from view import *
from i18n import I18N_RESOURCES
from ui.button.clear_shop_storage_button import ClearShopStorageButton


class ShopConstructorView(View):
    def __init__(self, map_id, shop_id):
        def on_clear_storage(button):
            self.controller.on_clear_storage()

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.shop.{shop_id}.constructor.view'))
        self.map_id = map_id
        self.shop_id = shop_id
        self.shop_stages_state_matrix = {}
        self.user_db_cursor.execute('''SELECT current_stage, shop_storage_money
                                       FROM shops WHERE map_id = ? AND shop_id = ?''', (self.map_id, self.shop_id))
        self.current_stage, self.shop_storage_money = self.user_db_cursor.fetchone()
        self.shop_stages_cells_position = (0, 0)
        self.shop_stages_cells_size = (0, 0)
        self.shop_details_window_position = (0, 0)
        self.shop_details_window_size = (0, 0)
        self.shader = from_files_names('shaders/shader.vert', 'shaders/shop_constructor_view/shader.frag')
        self.shop_view_shader_bottom_limit = 0.0
        self.shop_view_shader_upper_limit = 0.0
        self.current_hourly_profit_label = None
        self.current_exp_bonus_label = None
        self.hourly_profit_value_label = None
        self.exp_bonus_value_label = None
        self.progress_bar_money_inactive_image = load('img/game_progress_bars/progress_bar_inactive.png')
        self.progress_bar_money_inactive = None
        self.progress_bar_money_active_image = load('img/game_progress_bars/progress_bar_money_active.png')
        self.progress_bar_money_active = None
        self.money_progress_bar_position = (0, 0)
        self.storage_money_label = None
        self.storage_money_percent = 0
        self.clear_shop_storage_button = ClearShopStorageButton(on_click_action=on_clear_storage)
        self.buttons = [self.clear_shop_storage_button, ]
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

        if self.current_hourly_profit_label is None:
            self.current_hourly_profit_label \
                = Label(I18N_RESOURCES['current_hourly_profit_string'][self.current_locale],
                        font_size=self.bottom_bar_height // 5, color=(*WHITE_RGB, self.opacity),
                        x=self.shop_details_window_position[0] + self.bottom_bar_height // 8,
                        y=self.shop_details_window_position[1] + self.bottom_bar_height // 8
                          + 3 * self.bottom_bar_height + 2 * self.bottom_bar_height // 3,
                        anchor_x='left', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])

        if self.current_exp_bonus_label is None:
            self.current_exp_bonus_label \
                = Label(I18N_RESOURCES['current_exp_bonus_string'][self.current_locale],
                        font_size=self.bottom_bar_height // 5, color=(*WHITE_RGB, self.opacity),
                        x=self.shop_details_window_position[0] + self.bottom_bar_height // 8,
                        y=self.shop_details_window_position[1] + self.bottom_bar_height // 8
                          + 3 * self.bottom_bar_height + self.bottom_bar_height // 3,
                        anchor_x='left', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])

        if self.hourly_profit_value_label is None:
            if self.current_stage == 0:
                hourly_profit_value_text = '0  ¤'
            else:
                hourly_profit_value_text = f'{self.shop_stages_state_matrix[self.current_stage][HOURLY_PROFIT]}  ¤'

            self.hourly_profit_value_label \
                = Label(hourly_profit_value_text, font_size=self.bottom_bar_height // 5,
                        color=(*GREEN_RGB, self.opacity),
                        x=self.shop_details_window_position[0] + self.bottom_bar_height // 8
                          + 3 * self.bottom_bar_height,
                        y=self.shop_details_window_position[1] + self.bottom_bar_height // 8
                          + 3 * self.bottom_bar_height + 2 * self.bottom_bar_height // 3,
                        anchor_x='left', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])

        if self.exp_bonus_value_label is None:
            if self.current_stage == 0:
                exp_bonus_value_text = '0  %'
            else:
                exp_bonus_value_text = f'{self.shop_stages_state_matrix[self.current_stage][EXP_BONUS]}  %'

            self.exp_bonus_value_label \
                = Label(exp_bonus_value_text, font_size=self.bottom_bar_height // 5,
                        color=(*ORANGE_RGB, self.opacity),
                        x=self.shop_details_window_position[0] + self.bottom_bar_height // 8
                          + 3 * self.bottom_bar_height,
                        y=self.shop_details_window_position[1] + self.bottom_bar_height // 8
                          + 3 * self.bottom_bar_height + self.bottom_bar_height // 3,
                        anchor_x='left', anchor_y='center',
                        batch=self.batches['ui_batch'], group=self.groups['button_text'])

        if self.progress_bar_money_inactive is None:
            self.progress_bar_money_inactive = Sprite(self.progress_bar_money_inactive_image,
                                                      x=self.money_progress_bar_position[0],
                                                      y=self.money_progress_bar_position[1],
                                                      batch=self.batches['ui_batch'],
                                                      group=self.groups['button_background'])
            self.progress_bar_money_inactive.scale = self.bottom_bar_height / 80
            self.progress_bar_money_inactive.opacity = self.opacity

        if self.progress_bar_money_active is None:
            self.progress_bar_money_active = Sprite(self.progress_bar_money_active_image,
                                                    x=self.money_progress_bar_position[0],
                                                    y=self.money_progress_bar_position[1],
                                                    batch=self.batches['ui_batch'],
                                                    group=self.groups['button_text'])
            self.progress_bar_money_active.scale = self.bottom_bar_height / 80
            self.progress_bar_money_active.opacity = self.opacity

        if self.storage_money_label is None:
            self.storage_money_label = Label('0', font_name='Perfo', bold=True, color=(*GREEN_RGB, self.opacity),
                                             font_size=int(22 / 80 * self.bottom_bar_height),
                                             x=self.money_progress_bar_position[0]
                                               + int(self.progress_bar_money_inactive_image.width / 2 / 80
                                                     * self.bottom_bar_height),
                                             y=self.money_progress_bar_position[1] - self.bottom_bar_height // 8
                                               + self.bottom_bar_height // 2,
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
            b.state = 'normal'

    def on_change_screen_resolution(self, screen_resolution):
        self.on_recalculate_ui_properties(screen_resolution)
        self.shop_view_shader_bottom_limit = self.bottom_bar_height / self.screen_resolution[1] * 2 - 1
        self.shop_view_shader_upper_limit = 1 - self.top_bar_height / self.screen_resolution[1] * 2

        self.shop_details_window_size = (int(6.875 * self.bottom_bar_height) * 2 + self.bottom_bar_height // 4,
                                         19 * self.bottom_bar_height // 4)
        self.shop_details_window_position = ((self.screen_resolution[0] - self.shop_details_window_size[0]) // 2,
                                             (self.screen_resolution[1] - self.shop_details_window_size[1]
                                              - 3 * self.bottom_bar_height // 2) // 2 + self.bottom_bar_height)
        self.shop_stages_cells_position = (self.shop_details_window_position[0] + self.top_bar_height // 4,
                                           self.shop_details_window_position[1]
                                           + (self.shop_details_window_size[1] - self.top_bar_height
                                              - 4 * self.bottom_bar_height) // 2)
        self.shop_stages_cells_size = (self.shop_details_window_size[0] - self.top_bar_height // 2,
                                       3 * self.bottom_bar_height - self.bottom_bar_height // 8)
        self.money_progress_bar_position \
            = (self.shop_details_window_position[0] + self.shop_details_window_size[0] - self.bottom_bar_height // 8
               - int(self.progress_bar_money_inactive_image.width * self.bottom_bar_height / 80)
               - self.bottom_bar_height // 8 - self.bottom_bar_height,
               self.shop_details_window_position[1] + self.bottom_bar_height // 8
               + 3 * self.bottom_bar_height + self.bottom_bar_height // 8)
        self.clear_shop_storage_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        self.clear_shop_storage_button.x_margin = self.shop_details_window_position[0] \
                                                  + self.shop_details_window_size[0] \
                                                  - self.bottom_bar_height // 8 - self.bottom_bar_height
        self.clear_shop_storage_button.y_margin = self.shop_details_window_position[1] + self.bottom_bar_height // 8 \
                                                  + 3 * self.bottom_bar_height
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

        if self.is_activated:
            self.shader_sprite.vertices = (-1.0, self.shop_view_shader_bottom_limit,
                                           -1.0, self.shop_view_shader_upper_limit,
                                           1.0, self.shop_view_shader_upper_limit,
                                           1.0, self.shop_view_shader_bottom_limit)
            self.current_hourly_profit_label.x = self.shop_details_window_position[0] + self.bottom_bar_height // 8
            self.current_hourly_profit_label.y = self.shop_details_window_position[1] + self.bottom_bar_height // 8 \
                                                 + 3 * self.bottom_bar_height + 2 * self.bottom_bar_height // 3
            self.current_hourly_profit_label.font_size = self.bottom_bar_height // 5
            self.current_exp_bonus_label.x = self.shop_details_window_position[0] + self.bottom_bar_height // 8
            self.current_exp_bonus_label.y = self.shop_details_window_position[1] + self.bottom_bar_height // 8 \
                                                 + 3 * self.bottom_bar_height + self.bottom_bar_height // 3
            self.current_exp_bonus_label.font_size = self.bottom_bar_height // 5
            self.hourly_profit_value_label.x = self.shop_details_window_position[0] + self.bottom_bar_height // 8 \
                                               + 3 * self.bottom_bar_height
            self.hourly_profit_value_label.y = self.shop_details_window_position[1] + self.bottom_bar_height // 8 \
                                                 + 3 * self.bottom_bar_height + 2 * self.bottom_bar_height // 3
            self.hourly_profit_value_label.font_size = self.bottom_bar_height // 5
            self.exp_bonus_value_label.x = self.shop_details_window_position[0] + self.bottom_bar_height // 8 \
                                               + 3 * self.bottom_bar_height
            self.exp_bonus_value_label.y = self.shop_details_window_position[1] + self.bottom_bar_height // 8 \
                                                 + 3 * self.bottom_bar_height + self.bottom_bar_height // 3
            self.exp_bonus_value_label.font_size = self.bottom_bar_height // 5
            self.progress_bar_money_inactive.update(x=self.money_progress_bar_position[0],
                                                    y=self.money_progress_bar_position[1],
                                                    scale=self.bottom_bar_height / 80)
            self.progress_bar_money_active.update(x=self.money_progress_bar_position[0],
                                                  y=self.money_progress_bar_position[1],
                                                  scale=self.bottom_bar_height / 80)
            self.storage_money_label.x = self.money_progress_bar_position[0] \
                                         + int(self.progress_bar_money_inactive_image.width / 2 / 80
                                               * self.bottom_bar_height)
            self.storage_money_label.y = self.money_progress_bar_position[1] - self.bottom_bar_height // 8 \
                                         + self.bottom_bar_height // 2
            self.storage_money_label.font_size = int(22 / 80 * self.bottom_bar_height)

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
            self.shader_sprite = None
            self.current_hourly_profit_label.delete()
            self.current_hourly_profit_label = None
            self.current_exp_bonus_label.delete()
            self.current_exp_bonus_label = None
            self.hourly_profit_value_label.delete()
            self.hourly_profit_value_label = None
            self.exp_bonus_value_label.delete()
            self.exp_bonus_value_label = None
            self.progress_bar_money_inactive.delete()
            self.progress_bar_money_inactive = None
            self.progress_bar_money_active.delete()
            self.progress_bar_money_active = None
            self.storage_money_label.delete()
            self.storage_money_label = None
        else:
            self.current_hourly_profit_label.color = (*WHITE_RGB, self.opacity)
            self.current_exp_bonus_label.color = (*WHITE_RGB, self.opacity)
            self.hourly_profit_value_label.color = (*GREEN_RGB, self.opacity)
            self.exp_bonus_value_label.color = (*ORANGE_RGB, self.opacity)
            self.progress_bar_money_inactive.opacity = self.opacity
            self.progress_bar_money_active.opacity = self.opacity
            self.storage_money_label.color = (*GREEN_RGB, self.opacity)

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.current_hourly_profit_label.text = I18N_RESOURCES['current_hourly_profit_string'][self.current_locale]
            self.current_exp_bonus_label.text = I18N_RESOURCES['current_exp_bonus_string'][self.current_locale]

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.shop_constructor_opacity = self.opacity
        self.shader.uniforms.shop_stages_cells_position = self.shop_stages_cells_position
        self.shader.uniforms.shop_stages_cells_size = self.shop_stages_cells_size
        self.shader.uniforms.current_stage = self.current_stage
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

    def on_update_stage_state(self, shop_stages_state_matrix, stage_number):
        self.shop_stages_state_matrix = shop_stages_state_matrix

    def on_update_storage_money(self, storage_money):
        self.shop_storage_money = storage_money
        if self.is_activated:
            self.storage_money_label.text = '{0:,}  ¤'.format(self.shop_storage_money).replace(',', ' ')
            if self.current_stage == 0:
                self.storage_money_percent = 0
            else:
                self.storage_money_percent \
                    = int(self.shop_storage_money / self.shop_stages_state_matrix[self.current_stage][STORAGE_CAPACITY]
                          * 100)
                if self.storage_money_percent > 100:
                    self.storage_money_percent = 100

            if self.storage_money_percent == 0:
                image_region = self.progress_bar_money_active_image\
                    .get_region(self.progress_bar_money_active_image.height // 2,
                                self.progress_bar_money_active_image.height // 2, 1, 1)
            else:
                image_region = self.progress_bar_money_active_image\
                    .get_region(0, 0, self.storage_money_percent * self.progress_bar_money_active_image.width // 100,
                                self.progress_bar_money_active_image.height)

            self.progress_bar_money_active.image = image_region
