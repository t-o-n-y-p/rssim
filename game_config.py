import configparser


class GameConfig:
    def __init__(self):
        self.game_config = configparser.RawConfigParser()
        self.game_config.read('game_config.ini')

        screen_resolution_parsed = self.game_config['graphics']['screen_resolution'].split(',')
        self.screen_resolution = (int(screen_resolution_parsed[0]), int(screen_resolution_parsed[1]))
        self.frame_rate = 60
        self.vsync = False
        self.map_resolution = (8400, 3600)
        self.base_offset_upper_left_limit = (-7000, -2880)
        self.base_offset_lower_right_limit = (-120, 0)
        self.base_offset = (-3560, -1440)
        self.top_bar_height = 34
        self.bottom_bar_height = 54
        self.bottom_bar_width = 1000
        self.font_name = 'Arial'
        self.button_font_size = 16
        self.day_font_size = 24
        self.button_text_color = (255, 255, 255, 255)
        self.day_text_color = (205, 0, 0, 255)
        self.fps_display_enabled = self.game_config['graphics'].getboolean('fps_display_enabled')
        self.fps_display_update_interval = self.game_config['graphics'].getfloat('fps_display_update_interval')

        self.direction_from_left_to_right = 0
        self.direction_from_right_to_left = 1
        self.direction_from_left_to_right_side = 2
        self.direction_from_right_to_left_side = 3

        self.entry_train_route = ('left_entry', 'right_entry', 'left_side_entry', 'right_side_entry')
        self.exit_train_route = ('right_exit', 'left_exit', 'right_side_exit', 'left_side_exit')
        self.approaching_train_route = ('left_approaching', 'right_approaching',
                                        'left_side_approaching', 'right_side_approaching')

        self.train_acceleration_factor = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                          1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7,
                                          8, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12, 13, 13, 14, 14, 15, 15, 16, 16,
                                          17, 17, 18, 19, 19, 20, 20, 21, 21, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28,
                                          29, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 37, 38, 39, 40, 41, 41, 42,
                                          43, 44, 45, 46, 47, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
                                          61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80,
                                          81, 83, 84, 85, 86, 88, 89, 90, 92, 93, 94, 96, 97, 98, 100, 101, 103, 104,
                                          105, 107, 108, 110, 111, 113, 114, 116, 117, 119, 120, 122, 124, 125, 127,
                                          128, 130, 132, 133, 135, 137, 138, 140, 142, 144, 145, 147, 149, 151, 153,
                                          154, 156, 158, 160, 162, 164, 165, 167, 169, 171, 173, 175, 177, 179, 181,
                                          183, 185, 187, 189, 191, 193, 195, 198, 200, 202, 204, 206, 209, 211, 213,
                                          215, 218, 220, 222, 225, 227, 230, 232, 235, 237, 240, 242, 245, 247, 250,
                                          252, 255, 258, 260, 263, 266, 268, 271, 274, 277, 279, 282, 285, 288, 291,
                                          294, 297, 300, 303, 306, 309, 312, 315, 318, 321, 324, 327, 330, 334, 337,
                                          340, 344, 347, 350, 354, 357, 361, 364, 368, 371, 375, 379, 382, 386, 390,
                                          394, 397, 401, 405, 409, 413, 417, 421, 425, 429, 433, 438, 442, 446, 450,
                                          455, 459, 464, 468, 473, 478, 482, 487, 492, 497, 502, 507, 512, 517)
        self.train_maximum_speed = 5
        self.main_priority_tracks = (((20, 18, 16, 24, 22, 14, 12, 10, 8, 6, 4, 19, 17, 15, 23, 21, 13, 11, 9, 7, 5, 3),
                                      (20, 18, 16, 24, 22, 14, 12, 10, 8, 6, 4, 19, 17, 15, 23, 21, 13, 11, 9, 7, 5, 3),
                                      (32, 30, 28, 26, 24, 22), (23, 21)),
                                     ((19, 17, 15, 23, 21, 13, 11, 9, 7, 5, 3, 20, 18, 16, 24, 22, 14, 12, 10, 8, 6, 4),
                                      (19, 17, 15, 23, 21, 13, 11, 9, 7, 5, 3, 20, 18, 16, 24, 22, 14, 12, 10, 8, 6, 4),
                                      (24, 22), (31, 29, 27, 25, 23, 21)),
                                     ((31, 29, 27, 25, 23, 21), (23, 21), (0,), (31, 29, 27, 25, 23, 21)),
                                     ((24, 22), (32, 30, 28, 26, 24, 22), (32, 30, 28, 26, 24, 22), (0,)))
        self.pass_through_priority_tracks = ((2, 1), (1, 2))
        self.train_creation_timeout = (0, 0, 0, 0)

    def save_state(self):
        self.game_config['graphics']['screen_resolution'] = str(self.screen_resolution[0]) + ',' \
                                                          + str(self.screen_resolution[1])
        self.game_config['graphics']['fps_display_enabled'] = str(self.fps_display_enabled)
        self.game_config['graphics']['fps_display_update_interval'] = str(self.fps_display_update_interval)

        with open('game_config.ini', 'w') as configfile:
            self.game_config.write(configfile)