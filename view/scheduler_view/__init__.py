from logging import getLogger
from ctypes import windll

from database import CONFIG_DB_CURSOR
from view import *
from ui.schedule import ScheduleRow
from ui.button.close_schedule_button import CloseScheduleButton
from ui.shader_sprite.scheduler_view_shader_sprite import SchedulerViewShaderSprite
from ui.label.schedule_left_caption_label import ScheduleLeftCaptionLabel
from ui.label.schedule_right_caption_label import ScheduleRightCaptionLabel


class SchedulerView(View):
    def __init__(self, map_id):
        def on_close_schedule(button):
            self.controller.fade_out_animation.on_activate()

        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.scheduler.view'))
        self.map_id = map_id
        self.base_schedule = None
        self.game_time = None
        self.left_schedule_caption_label = ScheduleLeftCaptionLabel(parent_viewport=self.viewport)
        self.right_schedule_caption_label = ScheduleRightCaptionLabel(parent_viewport=self.viewport)
        self.close_schedule_button = CloseScheduleButton(on_click_action=on_close_schedule,
                                                         parent_viewport=self.viewport)
        self.buttons.append(self.close_schedule_button)
        self.schedule_rows = []
        for i in range(SCHEDULE_COLUMNS):
            column = []
            for j in range(SCHEDULE_ROWS):
                column.append(ScheduleRow(i, j, parent_viewport=self.viewport))

            self.schedule_rows.append(column)

        self.shader_sprite = SchedulerViewShaderSprite(view=self)
        self.on_init_content()

    def on_init_content(self):
        CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
        screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
        monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
        if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
            self.on_change_screen_resolution(monitor_resolution_config)
        else:
            USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
            self.on_change_screen_resolution(USER_DB_CURSOR.fetchone())

    @view_is_not_active
    def on_activate(self):
        self.is_activated = True
        self.shader_sprite.create()
        self.left_schedule_caption_label.create()
        self.right_schedule_caption_label.create()
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_deactivate()

        for b in self.buttons:
            b.on_deactivate()
            b.state = 'normal'

    @view_is_active
    def on_update(self):
        for i in range(min(len(self.base_schedule), SCHEDULE_ROWS * SCHEDULE_COLUMNS)):
            if not self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].is_activated \
                    and self.base_schedule[i][ARRIVAL_TIME] <= self.game_time + FRAMES_IN_ONE_HOUR:
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].opacity = self.opacity
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_activate()
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_assign_data(self.base_schedule[i])
                return

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.viewport.x1, self.viewport.y1 = 0, 0
        self.viewport.x2, self.viewport.y2 = self.screen_resolution
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.left_schedule_caption_label.on_change_screen_resolution(self.screen_resolution)
        self.right_schedule_caption_label.on_change_screen_resolution(self.screen_resolution)
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_change_screen_resolution(self.screen_resolution)

        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.shader_sprite.on_update_opacity(self.opacity)
        self.left_schedule_caption_label.on_update_opacity(self.opacity)
        self.right_schedule_caption_label.on_update_opacity(self.opacity)
        for b in self.buttons:
            b.on_update_opacity(self.opacity)

        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_opacity(self.opacity)

    @view_is_active
    def on_release_train(self, index):
        for i in range(index, SCHEDULE_ROWS * SCHEDULE_COLUMNS - 1):
            if self.schedule_rows[(i + 1) // SCHEDULE_ROWS][(i + 1) % SCHEDULE_ROWS].is_activated:
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS]\
                    .on_assign_data(self.base_schedule[i + 1])
            else:
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_deactivate(instant=True)
                break

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.left_schedule_caption_label.on_update_current_locale(self.current_locale)
        self.right_schedule_caption_label.on_update_current_locale(self.current_locale)
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_current_locale(self.current_locale)

    def on_apply_shaders_and_draw_vertices(self):
        self.shader_sprite.draw()

    def on_update_clock_state(self, clock_24h_enabled):
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_clock_state(clock_24h_enabled)

    def on_update_time(self, game_time):
        self.game_time = game_time
