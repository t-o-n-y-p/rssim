from camera import Camera


class MapCamera(Camera):
    def __init__(self):
        super().__init__(min_zoom=0.5, max_zoom=1.0)
