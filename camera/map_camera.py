from typing import final

from camera import Camera
from database import USER_DB_CURSOR


@final
class MapCamera(Camera):
    def __init__(self):
        super().__init__(min_zoom=0.5, max_zoom=1.0)
        USER_DB_CURSOR.execute(
            '''SELECT last_known_base_offset FROM map_position_settings 
            WHERE map_id IN (SELECT last_known_map_id FROM graphics)'''
        )
        self.offset_x, self.offset_y = (int(p) for p in USER_DB_CURSOR.fetchone()[0].split(','))
        USER_DB_CURSOR.execute(
            '''SELECT last_known_zoom FROM map_position_settings 
            WHERE map_id IN (SELECT last_known_map_id FROM graphics)'''
        )
        self.zoom = USER_DB_CURSOR.fetchone()[0]
