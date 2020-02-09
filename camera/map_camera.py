from fractions import Fraction

from camera import Camera


class MapCamera(Camera):
    def __init__(self):
        super().__init__(min_zoom=Fraction(1, 2), max_zoom=Fraction(1, 1))
