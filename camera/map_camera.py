from fractions import Fraction

from camera import Camera
from database import USER_DB_CURSOR


class MapCamera(Camera):
    def __init__(self):
        super().__init__(min_zoom=Fraction(1, 2), max_zoom=Fraction(1, 1))
        USER_DB_CURSOR.execute('''SELECT last_known_base_offset FROM map_position_settings 
                                  WHERE map_id IN (SELECT last_known_map_id FROM graphics)''')
        self.offset_x, self.offset_y = (-int(p) for p in USER_DB_CURSOR.fetchone()[0].split(','))
