from logging import getLogger

from ui import *
from database import USER_DB_CURSOR
from i18n import I18N_RESOURCES
from ui.label.schedule_row_24h_main_label import ScheduleRow24HMainLabel
from ui.label.schedule_row_12h_main_label import ScheduleRow12HMainLabel
from ui.label.schedule_row_arrival_label import ScheduleRowArrivalLabel


def row_is_active(fn):
    def _handle_if_row_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_row_is_activated


def row_is_not_active(fn):
    def _handle_if_row_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_row_is_not_activated


@final
class ScheduleRow:
    def __init__(self, map_id, column, row, parent_viewport):
        self.logger = getLogger(f'root.app.game.map.scheduler.view.row.{column}.{row}')
        self.map_id, self.column, self.row = map_id, column, row
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.data = None
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = USER_DB_CURSOR.fetchone()[0]
        self.main_sprite_24h = ScheduleRow24HMainLabel(self.column, self.row, parent_viewport=self.viewport)
        self.main_sprite_12h = ScheduleRow12HMainLabel(self.column, self.row, parent_viewport=self.viewport)
        self.arrival_sprite = ScheduleRowArrivalLabel(self.map_id, self.column, self.row, parent_viewport=self.viewport)
        self.screen_resolution = (0, 0)
        self.is_activated = False
        self.opacity = 0
        self.on_window_resize_handlers = [
            self.on_window_resize, self.arrival_sprite.on_window_resize,
            self.main_sprite_24h.on_window_resize, self.main_sprite_12h.on_window_resize
        ]

    def on_activate(self):
        self.is_activated = True

    @row_is_active
    def on_deactivate(self, instant=True):
        self.is_activated = False
        self.data = []
        if instant:
            self.opacity = 0
            self.main_sprite_24h.delete()
            self.main_sprite_12h.delete()
            self.arrival_sprite.delete()

    def on_assign_data(self, data):
        self.data = data
        self.on_update_main_sprite_args()
        if self.clock_24h_enabled:
            self.main_sprite_24h.create()
            self.main_sprite_12h.delete()
        else:
            self.main_sprite_12h.create()
            self.main_sprite_24h.delete()

        self.arrival_sprite.on_update_args((self.data[DIRECTION], ))
        self.arrival_sprite.create()

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 = self.parent_viewport.x1 + get_inner_area_rect(self.screen_resolution)[0] + (
            int(6.875 * get_bottom_bar_height(self.screen_resolution))
            + get_bottom_bar_height(self.screen_resolution) // 4
        ) * self.column
        self.viewport.x2 = self.viewport.x1 + int(6.875 * get_bottom_bar_height(self.screen_resolution))
        self.viewport.y2 \
            = self.parent_viewport.y1 + get_inner_area_rect(self.screen_resolution)[1] \
            + get_inner_area_rect(self.screen_resolution)[3] \
            - (get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)) * (self.row + 1)
        self.viewport.y1 = self.viewport.y2 - get_inner_area_rect(self.screen_resolution)[3] // (SCHEDULE_ROWS + 1)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.on_update_main_sprite_args()
        self.main_sprite_24h.on_update_current_locale(self.current_locale)
        self.main_sprite_12h.on_update_current_locale(self.current_locale)
        self.arrival_sprite.on_update_current_locale(self.current_locale)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        self.main_sprite_24h.on_update_opacity(self.opacity)
        self.main_sprite_12h.on_update_opacity(self.opacity)
        self.arrival_sprite.on_update_opacity(self.opacity)

    @row_is_active
    def on_update_main_sprite_args(self):
        self.main_sprite_24h.on_update_args(
            (
                self.data[TRAIN_ID], (self.data[ARRIVAL_TIME] // SECONDS_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY,
                (self.data[ARRIVAL_TIME] // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR, self.data[CARS]
            )
        )
        am_pm_index = ((self.data[ARRIVAL_TIME] // SECONDS_IN_ONE_HOUR) // 12 + 1) % 2
        self.main_sprite_12h.on_update_args(
            (
                self.data[TRAIN_ID], (self.data[ARRIVAL_TIME] // SECONDS_IN_ONE_HOUR + 11) % 12 + 1,
                (self.data[ARRIVAL_TIME] // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR,
                I18N_RESOURCES['am_pm_string'][self.current_locale][am_pm_index], self.data[CARS]
            )
        )

    def on_update_clock_state(self, clock_24h_enabled):
        self.clock_24h_enabled = clock_24h_enabled
        if self.is_activated:
            if self.clock_24h_enabled:
                self.main_sprite_24h.create()
                self.main_sprite_12h.delete()
            else:
                self.main_sprite_12h.create()
                self.main_sprite_24h.delete()
