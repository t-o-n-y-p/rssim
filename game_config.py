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
        self.bottom_bar_height = 80
        self.bottom_bar_width = 1000
        self.font_name = 'Arial'
        self.iconify_close_button_font_size = 16
        self.play_pause_button_font_size = 32
        self.day_font_size = 22
        self.level_font_size = 22
        self.button_text_color = (255, 255, 255, 255)
        self.day_text_color = (255, 255, 255, 255)
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

        self.accumulated_player_progress = (0, 55, 275, 770, 1650, 3050, 5060, 7825, 11465, 16100, 21850, 28890, 37290,
                                            47235, 58855, 72355, 87795, 105390, 125280, 147605, 172605, 200430, 231230,
                                            265270, 302710, 343835, 388815, 437955, 491435, 549580, 612580, 680625,
                                            754225, 833590, 919100, 1011150, 1110150, 1216340, 1330150, 1452220,
                                            1582820, 1722630, 1872150, 2031895, 2202615, 2384865, 2579215, 2786485,
                                            3007525, 3242970, 3493720, 3760960, 4045400, 4348295, 4670675, 5013875,
                                            5378995, 5767450, 6180990, 6620835, 7088835, 7603021, 8167447, 8786080,
                                            9463831, 10205936, 11017569, 11904609, 12873288, 13930648, 15083692,
                                            16340773, 17778723, 19419056, 21285921, 23405084, 25805305, 28517911,
                                            31578623, 35025492, 38900762, 43251306, 48128003, 53585955, 59688435,
                                            66501447, 74100425, 82565318, 91984060, 102454644, 114142944, 127537143,
                                            142470215, 159083828, 177531140, 197979890, 220611122, 245617334, 273213742,
                                            303626245, 0)
        self.player_progress = (0, 55, 220, 495, 880, 1400, 2010, 2765, 3640, 4635, 5750, 7040, 8400, 9945, 11620,
                                13500, 15440, 17595, 19890, 22325, 25000, 27825, 30800, 34040, 37440, 41125, 44980,
                                49140, 53480, 58145, 63000, 68045, 73600, 79365, 85510, 92050, 99000, 106190, 113810,
                                122070, 130600, 139810, 149520, 159745, 170720, 182250, 194350, 207270, 221040, 235445,
                                250750, 267240, 284440, 302895, 322380, 343200, 365120, 388455, 413540, 439845, 468000,
                                514186, 564426, 618633, 677751, 742105, 811633, 887040, 968679, 1057360, 1153044,
                                1257081, 1437950, 1640333, 1866865, 2119163, 2400221, 2712606, 3060712, 3446869,
                                3875270, 4350544, 4876697, 5457952, 6102480, 6813012, 7598978, 8464893, 9418742,
                                10470584, 11688300, 13394199, 14933072, 16613613, 18447312, 20448750, 22631232,
                                25006212, 27596408, 30412503, 0)

    def save_state(self):
        self.game_config['graphics']['screen_resolution'] = str(self.screen_resolution[0]) + ',' \
                                                          + str(self.screen_resolution[1])
        self.game_config['graphics']['fps_display_enabled'] = str(self.fps_display_enabled)
        self.game_config['graphics']['fps_display_update_interval'] = str(self.fps_display_update_interval)

        with open('game_config.ini', 'w') as configfile:
            self.game_config.write(configfile)
