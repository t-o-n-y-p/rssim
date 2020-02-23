from logging import getLogger
from math import cos, sin, radians

from ui import *
from ui.knob import Knob


@final
class TimeSpeedKnob(Knob):
    def __init__(self, parent_viewport):
        super().__init__(parent_viewport=parent_viewport, logger=getLogger('root.app.game.view.time_speed_knob'))
        self.main_color = YELLOW_RGB
        self.background_color = YELLOW_GREY_RGB
        # self.value_label = None
        # self.on_window_resize_handlers.append(self.value_label.on_window_resize)
        self.start_value = 1.0
        self.maximum_steps = 32
        self.circle_segments_per_step = 3
        self.value_step = pow(16.0, 1 / self.maximum_steps)
        self.on_current_step_update(29)

    def current_value_formula(self):
        return self.start_value * pow(self.value_step, self.current_step)

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
        pass
        self.circle_vertices = [
            round(middle_point[0] + circle_radius * cos(radians(210))),
            round(middle_point[1] + circle_radius * sin(radians(210)))
        ]
        for i in range(self.maximum_steps * self.circle_segments_per_step):
            self.circle_vertices.append(
                round(middle_point[0] + circle_radius * cos(
                    radians(210 - i / (self.maximum_steps * self.circle_segments_per_step) * 240)
                ))
            )
            self.circle_vertices.append(
                round(middle_point[1] + circle_radius * sin(
                    radians(210 - i / (self.maximum_steps * self.circle_segments_per_step) * 240)
                ))
            )

        self.circle_vertices.append(round(middle_point[0] + circle_radius * cos(radians(-30))))
        self.circle_vertices.append(round(middle_point[1] + circle_radius * sin(radians(-30))))
        self.circle_vertices.append(round(middle_point[0] + circle_radius * cos(radians(-30))))
        self.circle_vertices.append(round(middle_point[1] + circle_radius * sin(radians(-30))))
        if self.circle is not None:
            self.circle.vertices = self.circle_vertices
