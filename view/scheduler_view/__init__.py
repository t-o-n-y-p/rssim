from logging import getLogger

from pyglet.text import Label
from pyglet.gl import GL_QUADS
from pyshaders import from_files_names

from view import *
from ui.schedule import ScheduleRow
from ui.button.close_schedule_button import CloseScheduleButton
from i18n import I18N_RESOURCES


class SchedulerView(View):
    """
    Implements Scheduler view.
    Scheduler object is responsible for properties, UI and events related to the train schedule.
    """
    def __init__(self):
        """
        Button click handlers:
            on_close_schedule                       on_click handler for close schedule button

        Properties:
            schedule_opacity                        general opacity of the schedule screen
            schedule_left_caption_position          position for schedule table caption, left side
            schedule_right_caption_position         position for schedule table caption, right side
            schedule_caption_font_size              font size for schedule table caption
            base_schedule                           generated train queue sorted by arrival time within an hour
            game_time                               current in-game time
            left_schedule_caption_label             label from caption for left schedule column
            right_schedule_caption_label            label from caption for right schedule column
            close_schedule_button                   CloseScheduleButton object
            buttons                                 list of all buttons
            schedule_rows                           list of content rows on schedule screen
            scheduler_view_shader_sprite            sprite for scheduler view shader
            scheduler_view_shader                   shader for schedule screen area
            scheduler_view_shader_bottom_limit      bottom edge for scheduler_view_shader_sprite
            scheduler_view_shader_upper_limit       upper edge for scheduler_view_shader_sprite

        """
        def on_close_schedule(button):
            """
            Notifies controller that player has closed schedule screen.

            :param button:                      button that was clicked
            """
            self.controller.on_deactivate_view()

        self.map_id = None
        self.on_update_map_id()
        super().__init__(logger=getLogger(f'root.app.game.map.{self.map_id}.scheduler.view'))
        self.schedule_left_caption_position = (0, 0)
        self.schedule_right_caption_position = (0, 0)
        self.schedule_caption_font_size = 0
        self.on_read_ui_info()
        self.base_schedule = None
        self.game_time = None
        self.left_schedule_caption_label = None
        self.right_schedule_caption_label = None
        self.close_schedule_button = CloseScheduleButton(on_click_action=on_close_schedule)
        self.buttons.append(self.close_schedule_button)
        self.schedule_rows = []
        for i in range(SCHEDULE_COLUMNS):
            column = []
            for j in range(SCHEDULE_ROWS):
                column.append(ScheduleRow(i, j, self.current_locale))

            self.schedule_rows.append(column)

        self.shader_sprite = None
        self.shader = from_files_names('shaders/shader.vert', 'shaders/scheduler_view/shader.frag')
        self.scheduler_view_shader_bottom_limit = 0.0
        self.scheduler_view_shader_upper_limit = 0.0
        self.on_init_graphics()

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        if self.shader_sprite is None:
            self.shader_sprite \
                = self.batches['main_frame'].add(4, GL_QUADS, self.groups['main_frame'],
                                                 ('v2f/static', (-1.0, self.scheduler_view_shader_bottom_limit,
                                                                 -1.0, self.scheduler_view_shader_upper_limit,
                                                                 1.0, self.scheduler_view_shader_upper_limit,
                                                                 1.0, self.scheduler_view_shader_bottom_limit)))

        if self.left_schedule_caption_label is None:
            self.left_schedule_caption_label \
                = Label(I18N_RESOURCES['schedule_caption_string'][self.current_locale],
                        font_name='Perfo', bold=True, font_size=self.schedule_caption_font_size,
                        color=(*ORANGE_RGB, self.opacity),
                        x=self.schedule_left_caption_position[0], y=self.schedule_left_caption_position[1],
                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                        group=self.groups['button_text'])

        if self.right_schedule_caption_label is None:
            self.right_schedule_caption_label \
                = Label(I18N_RESOURCES['schedule_caption_string'][self.current_locale],
                        font_name='Perfo', bold=True, font_size=self.schedule_caption_font_size,
                        color=(*ORANGE_RGB, self.opacity),
                        x=self.schedule_right_caption_position[0], y=self.schedule_right_caption_position[1],
                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                        group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_deactivate()

        for b in self.buttons:
            b.on_deactivate()

    def on_update(self):
        if self.is_activated:
            for i in range(min(len(self.base_schedule), SCHEDULE_ROWS * SCHEDULE_COLUMNS)):
                if not self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].is_activated:
                    self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_activate()
                    self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_assign_data(self.base_schedule[i])
                    return

    def on_update_opacity(self, new_opacity):
        self.on_update_opacity(new_opacity)
        for b in self.buttons:
            b.on_update_opacity(new_opacity)

        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_opacity(new_opacity)

    def on_update_sprite_opacity(self):
        if self.opacity <= 0:
            self.shader_sprite.delete()
            self.shader_sprite = None
            self.left_schedule_caption_label.delete()
            self.left_schedule_caption_label = None
            self.right_schedule_caption_label.delete()
            self.right_schedule_caption_label = None
        else:
            self.left_schedule_caption_label.color = (*ORANGE_RGB, self.opacity)
            self.right_schedule_caption_label.color = (*ORANGE_RGB, self.opacity)

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        self.scheduler_view_shader_bottom_limit = self.bottom_bar_height / self.screen_resolution[1] * 2 - 1
        self.scheduler_view_shader_upper_limit = 1 - self.top_bar_height / self.screen_resolution[1] * 2
        if self.is_activated:
            self.shader_sprite.vertices = (-1.0, self.scheduler_view_shader_bottom_limit,
                                           -1.0, self.scheduler_view_shader_upper_limit,
                                           1.0, self.scheduler_view_shader_upper_limit,
                                           1.0, self.scheduler_view_shader_bottom_limit)
        self.on_read_ui_info()
        if self.is_activated:
            self.left_schedule_caption_label.x = self.schedule_left_caption_position[0]
            self.left_schedule_caption_label.y = self.schedule_left_caption_position[1]
            self.left_schedule_caption_label.font_size = self.schedule_caption_font_size
            self.right_schedule_caption_label.x = self.schedule_right_caption_position[0]
            self.right_schedule_caption_label.y = self.schedule_right_caption_position[1]
            self.right_schedule_caption_label.font_size = self.schedule_caption_font_size

        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_change_screen_resolution(screen_resolution)

        self.close_schedule_button.x_margin = self.screen_resolution[0] - 11 * self.bottom_bar_height // 2 + 2
        self.close_schedule_button.y_margin = 0
        self.close_schedule_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin,  b.y_margin))

    def on_update_live_schedule(self, base_schedule):
        """
        Updates base schedule matrix and game time for on_update() method.

        :param base_schedule                       generated train queue sorted by arrival time
        """
        self.base_schedule = base_schedule

    @view_is_active
    def on_release_train(self, index):
        """
        Removes train from schedule table once it has arrived to the station entry.

        :param index:                               train position in table (from 0)
        """
        last_row_number = min(len(self.base_schedule), SCHEDULE_ROWS * SCHEDULE_COLUMNS) - 1
        for i in range(index, last_row_number):
            self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS]\
                .on_assign_data(self.base_schedule[i + 1])

        self.schedule_rows[last_row_number // SCHEDULE_ROWS][last_row_number % SCHEDULE_ROWS].on_deactivate()
        self.base_schedule.pop(index)

    def on_read_ui_info(self):
        """
        Calculates all offsets and font sizes.
        """
        general_height = 4 * int(72 / 1280 * self.screen_resolution[0]) \
                         + 3 * int(72 / 1280 * self.screen_resolution[0]) // 4
        size = (int(6.875 * int(72 / 1280 * self.screen_resolution[0])),
                general_height // (SCHEDULE_ROWS + 1))
        schedule_interval_between_columns = int(72 / 1280 * self.screen_resolution[0]) // 4
        top_left_row_position = (self.screen_resolution[0] // 2
                                 - int(6.875 * int(72 / 1280 * self.screen_resolution[0])) // 2
                                 - schedule_interval_between_columns // 2,
                                 self.screen_resolution[1]
                                 - ((self.screen_resolution[1] - int(72 / 1280 * self.screen_resolution[0]) // 2
                                     - int(72 / 1280 * self.screen_resolution[0]) - general_height) // 2
                                    + size[1] // 2 * 3)
                                 - int(72 / 1280 * self.screen_resolution[0]) // 2)
        self.schedule_left_caption_position = (top_left_row_position[0], top_left_row_position[1] + size[1])
        self.schedule_right_caption_position = (top_left_row_position[0] + size[0] + schedule_interval_between_columns,
                                                top_left_row_position[1] + size[1])
        self.schedule_caption_font_size = size[1] // 5 * 3

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.left_schedule_caption_label.text = I18N_RESOURCES['schedule_caption_string'][self.current_locale]
            self.right_schedule_caption_label.text = I18N_RESOURCES['schedule_caption_string'][self.current_locale]

        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_current_locale(new_locale)

    @shader_sprite_exists
    def on_apply_shaders_and_draw_vertices(self):
        """
        Activates the shader, initializes all shader uniforms, draws shader sprite and deactivates the shader.
        """
        self.shader.use()
        self.shader.uniforms.screen_resolution = self.screen_resolution
        self.shader.uniforms.schedule_opacity = self.opacity
        self.shader_sprite.draw(GL_QUADS)
        self.shader.clear()

    def on_update_map_id(self):
        pass

    def on_init_graphics(self):
        self.on_change_screen_resolution(self.screen_resolution)
