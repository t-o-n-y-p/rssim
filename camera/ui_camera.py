from typing import final

from camera import Camera


@final
class UICamera(Camera):
    def __init__(self):
        super().__init__(scroll_speed=0, min_zoom=1, max_zoom=1)
