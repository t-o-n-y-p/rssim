from .model_base import Model


class MapModel(Model):
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor):
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor)
        self.screen_resolution = (1280, 720)
        self.base_offset = (-3440, -1440)
        self.base_offset_lower_left_limit = (0, 0)
        self.base_offset_upper_right_limit = (-6880, -2880)
        self.game_paused = False
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]
        self.zoom_factor = 1.0

    def on_activate(self):
        self.is_activated = True

    def on_assign_view(self, view):
        self.view = view
        self.view.on_unlock_track(self.unlocked_tracks)

    def on_change_screen_resolution(self, screen_resolution):
        self.base_offset_upper_right_limit = (screen_resolution[0] - 8160, screen_resolution[1] - 3600)
        new_default_base_offset = (self.base_offset_upper_right_limit[0] // 2,
                                   self.base_offset_upper_right_limit[1] // 2)
        self.view.on_change_default_base_offset(new_default_base_offset)
        self.base_offset = (self.base_offset[0] + (screen_resolution[0] - self.screen_resolution[0]) // 2,
                            self.base_offset[1] + (screen_resolution[1] - self.screen_resolution[1]) // 2)
        self.check_base_offset_limits()

        self.screen_resolution = screen_resolution
        self.view.on_change_screen_resolution(screen_resolution)
        self.view.on_change_base_offset(self.base_offset)

    def on_unlock_track(self, track_number):
        self.unlocked_tracks = track_number
        self.view.on_unlock_track(track_number)

    def on_zoom_in(self):
        self.zoom_factor = 1.0
        self.base_offset_upper_right_limit = (self.screen_resolution[0] - 8160, self.screen_resolution[1] - 3600)
        self.base_offset = (self.base_offset[0] * 2 - self.screen_resolution[0] // 2,
                            self.base_offset[1] * 2 - self.screen_resolution[1] // 2)
        self.check_base_offset_limits()
        self.view.on_zoom_in()
        self.view.on_change_base_offset(self.base_offset)

    def on_zoom_out(self):
        self.zoom_factor = 0.5
        self.base_offset_upper_right_limit = (self.screen_resolution[0] - 4080, self.screen_resolution[1] - 1800)
        self.base_offset = (self.base_offset[0] // 2 + self.screen_resolution[0] // 4,
                            self.base_offset[1] // 2 + self.screen_resolution[1] // 4)
        self.check_base_offset_limits()
        self.view.on_zoom_out()
        self.view.on_change_base_offset(self.base_offset)

    def check_base_offset_limits(self):
        if self.base_offset[0] > self.base_offset_lower_left_limit[0]:
            self.base_offset = (self.base_offset_lower_left_limit[0], self.base_offset[1])

        if self.base_offset[0] < self.base_offset_upper_right_limit[0]:
            self.base_offset = (self.base_offset_upper_right_limit[0], self.base_offset[1])

        if self.base_offset[1] > self.base_offset_lower_left_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_lower_left_limit[1])

        if self.base_offset[1] < self.base_offset_upper_right_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_upper_right_limit[1])

    def on_change_base_offset(self, new_base_offset):
        self.base_offset = new_base_offset
        self.view.on_change_base_offset(new_base_offset)
