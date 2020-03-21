from logging import getLogger

from view import *
from ui.schedule_row import ScheduleRow
from ui.button.close_schedule_button import CloseScheduleButton
from ui.shader_sprite.scheduler_view_shader_sprite import SchedulerViewShaderSprite
from ui.label.schedule_left_caption_label import ScheduleLeftCaptionLabel
from ui.label.schedule_right_caption_label import ScheduleRightCaptionLabel


class SchedulerView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        def on_close_schedule(button):
            self.controller.fade_out_animation.on_activate()
            self.controller.parent_controller.on_close_schedule()

        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.scheduler.view'))
        self.arrival_time_threshold = SCHEDULE_ARRIVAL_TIME_THRESHOLD[self.map_id]
        self.left_schedule_caption_label = ScheduleLeftCaptionLabel(parent_viewport=self.viewport)
        self.right_schedule_caption_label = ScheduleRightCaptionLabel(parent_viewport=self.viewport)
        self.close_schedule_button = CloseScheduleButton(on_click_action=on_close_schedule,
                                                         parent_viewport=self.viewport)
        self.buttons.append(self.close_schedule_button)
        self.schedule_rows = []
        for i in range(SCHEDULE_COLUMNS):
            column = []
            for j in range(SCHEDULE_ROWS):
                new_schedule_row = ScheduleRow(self.map_id, i, j, parent_viewport=self.viewport)
                column.append(new_schedule_row)
                self.on_window_resize_handlers.extend(new_schedule_row.on_window_resize_handlers)

            self.schedule_rows.append(column)

        self.shader_sprite = SchedulerViewShaderSprite(view=self)
        self.on_window_resize_handlers.extend([
            self.left_schedule_caption_label.on_window_resize, self.right_schedule_caption_label.on_window_resize,
            self.shader_sprite.on_window_resize
        ])
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.left_schedule_caption_label.create()
        self.right_schedule_caption_label.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_deactivate()

    @final
    @view_is_active
    def on_update(self):
        for i in range(min(len(BASE_SCHEDULE[self.map_id]), SCHEDULE_ROWS * SCHEDULE_COLUMNS)):
            if not self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].is_activated \
                    and BASE_SCHEDULE[self.map_id][i][ARRIVAL_TIME] <= self.game_time + self.arrival_time_threshold:
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].opacity = self.opacity
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_activate()
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_assign_data(BASE_SCHEDULE[self.map_id][i])
                return

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.left_schedule_caption_label.on_update_current_locale(self.current_locale)
        self.right_schedule_caption_label.on_update_current_locale(self.current_locale)
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_current_locale(self.current_locale)

    @final
    def on_update_clock_state(self, clock_24h_enabled):
        super().on_update_clock_state(clock_24h_enabled)
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_clock_state(clock_24h_enabled)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.left_schedule_caption_label.on_update_opacity(self.opacity)
        self.right_schedule_caption_label.on_update_opacity(self.opacity)
        for i in range(SCHEDULE_COLUMNS):
            for j in range(SCHEDULE_ROWS):
                self.schedule_rows[i][j].on_update_opacity(self.opacity)

    @final
    @view_is_active
    def on_release_train(self, index):
        for i in range(index, SCHEDULE_ROWS * SCHEDULE_COLUMNS - 1):
            if self.schedule_rows[(i + 1) // SCHEDULE_ROWS][(i + 1) % SCHEDULE_ROWS].is_activated:
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS]\
                    .on_assign_data(BASE_SCHEDULE[self.map_id][i + 1])
            else:
                self.schedule_rows[i // SCHEDULE_ROWS][i % SCHEDULE_ROWS].on_deactivate(instant=True)
                break

        if self.schedule_rows[SCHEDULE_COLUMNS - 1][SCHEDULE_ROWS - 1].is_activated:
            self.schedule_rows[SCHEDULE_COLUMNS - 1][SCHEDULE_ROWS - 1]\
                .on_assign_data(BASE_SCHEDULE[self.map_id][SCHEDULE_ROWS * SCHEDULE_COLUMNS])
