from logging import getLogger
from math import cos, sin, radians, log

from ui import *
from ui.knob import Knob
from ui.label.time_speed_value_label import TimeSpeedValueLabel


@final
class TimeSpeedKnob(Knob):
    def __init__(self, on_value_update_action, parent_viewport):
        super().__init__(on_value_update_action=on_value_update_action, parent_viewport=parent_viewport,
                         logger=getLogger('root.app.game.view.time_speed_knob'))
        self.main_color = YELLOW_RGB
        self.background_color = YELLOW_GREY_RGB
        self.value_label = TimeSpeedValueLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.value_label.on_window_resize)
        self.start_value = 1.0
        self.maximum_steps = 24
        self.value_step = pow(16.0, 1 / self.maximum_steps)
        USER_DB_CURSOR.execute('SELECT dt_multiplier FROM epoch_timestamp')
        current_value = USER_DB_CURSOR.fetchone()[0]
        self.value_label.on_update_args((current_value, ))
        self.on_current_step_update(round(log(current_value, self.value_step)))

    def current_value_formula(self):
        return self.start_value * pow(self.value_step, self.current_step)

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.value_label.on_update_current_locale(self.current_locale)

    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1 = self.parent_viewport.x2 - 2 * get_bottom_bar_height(self.screen_resolution)
        self.viewport.x2 = self.parent_viewport.x2 - get_bottom_bar_height(self.screen_resolution)
        self.viewport.y1 = self.parent_viewport.y1
        self.viewport.y2 = self.parent_viewport.y1 + get_bottom_bar_height(self.screen_resolution)
        circle_radius = 11 * get_bottom_bar_height(self.screen_resolution) / 32
        middle_point = (
            (self.viewport.x1 + self.viewport.x2) / 2,
            (self.viewport.y1 + self.viewport.y2) / 2 - circle_radius // 4
        )
        self.circle_vertices.clear()
        for i in range(self.maximum_steps):
            self.circle_vertices.append(
                middle_point[0] + circle_radius * cos(
                    radians(210 - i / self.maximum_steps * 240)
                )
            )
            self.circle_vertices.append(
                middle_point[1] + circle_radius * sin(
                    radians(210 - i / self.maximum_steps * 240)
                )
            )

        self.circle_vertices.append(middle_point[0] + circle_radius * cos(radians(-30)))
        self.circle_vertices.append(middle_point[1] + circle_radius * sin(radians(-30)))
        if self.circle is not None:
            self.circle.vertices = self.circle_vertices