from typing import final

from database import USER_DB_CURSOR, CARS, ARRIVAL_TIME, TRAIN_ID, DIRECTION
from ui import SCHEDULE_ROWS, get_inner_area_rect, get_bottom_bar_height, window_size_has_changed, UIObject, \
    is_active, optional_object, localizable, SCHEDULE_COLUMNS
from ui.label_v2.schedule_row_12h_main_label_v2 import ScheduleRow12HMainLabelV2
from ui.label_v2.schedule_row_24h_main_label_v2 import ScheduleRow24HMainLabelV2
from ui.label_v2.schedule_row_arrival_label_v2 import ScheduleRowArrivalLabelV2


def schedule_rows(f):
    def _schedule_rows(*args, **kwargs):
        f(*args, **kwargs)
        schedule_rows_list = [
            [
                ScheduleRowV2(
                    logger=args[0].logger.getChild(f'schedule_row_v2.{i}.{j}'),
                    parent_viewport=args[0].viewport, map_id=args[0].map_id, column=i, row=j
                ) for j in range(SCHEDULE_ROWS)
            ] for i in range(SCHEDULE_COLUMNS)
        ]
        args[0].__setattr__('schedule_rows', schedule_rows_list)
        args[0].ui_objects.extend(schedule_rows_list)
        for column in schedule_rows_list:
            for row in column:
                args[0].fade_out_animation.child_animations.append(row.fade_out_animation)
                args[0].on_window_resize_handlers.extend(row.on_window_resize_handlers)

    return _schedule_rows


@final
class ScheduleRowV2(UIObject):
    @localizable
    @optional_object(ScheduleRow12HMainLabelV2)
    @optional_object(ScheduleRow24HMainLabelV2)
    @optional_object(ScheduleRowArrivalLabelV2)
    def __init__(self, logger, parent_viewport, map_id, column, row):
        super().__init__(logger, parent_viewport)
        self.map_id, self.column, self.row = map_id, column, row
        self.data = []
        USER_DB_CURSOR.execute('SELECT clock_24h FROM i18n')
        self.clock_24h_enabled = USER_DB_CURSOR.fetchone()[0]

    @is_active
    def on_deactivate(self):
        super().on_deactivate()
        self.data = []

    def on_assign_data(self, data):
        self.data = data
        self.on_update_main_sprite_args()
        self.schedule_row_arrival_label_v2.begin_update()                                                       # noqa
        self.schedule_row_arrival_label_v2.on_map_id_update(self.map_id)                                        # noqa
        self.schedule_row_arrival_label_v2.on_direction_update(self.data[DIRECTION])                            # noqa
        self.schedule_row_arrival_label_v2.end_update()                                                         # noqa
        if self.is_activated:
            self.schedule_row_arrival_label_v2.fade_in_animation.on_activate()                                  # noqa
            if self.clock_24h_enabled:
                self.schedule_row_24h_main_label_v2.fade_in_animation.on_activate()                             # noqa
                self.schedule_row_12h_main_label_v2.fade_out_animation.on_activate()                            # noqa
            else:
                self.schedule_row_12h_main_label_v2.fade_in_animation.on_activate()                             # noqa
                self.schedule_row_24h_main_label_v2.fade_out_animation.on_activate()                            # noqa

    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
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

    @is_active
    def on_update_main_sprite_args(self):
        self.schedule_row_24h_main_label_v2.begin_update()                                                      # noqa
        self.schedule_row_24h_main_label_v2.on_train_id_upate(self.data[TRAIN_ID])                              # noqa
        self.schedule_row_24h_main_label_v2.on_24h_time_upate(self.data[ARRIVAL_TIME])                          # noqa
        self.schedule_row_24h_main_label_v2.on_cars_update(self.data[CARS])                                     # noqa
        self.schedule_row_24h_main_label_v2.end_update()                                                        # noqa
        self.schedule_row_12h_main_label_v2.begin_update()                                                      # noqa
        self.schedule_row_12h_main_label_v2.on_train_id_upate(self.data[TRAIN_ID])                              # noqa
        self.schedule_row_12h_main_label_v2.on_12h_time_upate(self.data[ARRIVAL_TIME])                          # noqa
        self.schedule_row_12h_main_label_v2.on_cars_update(self.data[CARS])                                     # noqa
        self.schedule_row_12h_main_label_v2.end_update()                                                        # noqa

    def on_update_clock_state(self, clock_24h_enabled):
        self.clock_24h_enabled = clock_24h_enabled
        if self.is_activated:
            if self.clock_24h_enabled:
                self.schedule_row_24h_main_label_v2.fade_in_animation.on_activate()                             # noqa
                self.schedule_row_12h_main_label_v2.fade_out_animation.on_activate()                            # noqa
            else:
                self.schedule_row_12h_main_label_v2.fade_in_animation.on_activate()                             # noqa
                self.schedule_row_24h_main_label_v2.fade_out_animation.on_activate()                            # noqa
