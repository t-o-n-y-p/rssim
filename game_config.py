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

        self.maximum_level = 100
        self.accumulated_player_progress = (0.0, 55.0, 275.0, 770.0, 1650.0, 3050.0, 5060.0, 7825.0, 11465.0, 16100.0,
                                            21850.0, 28890.0, 37290.0, 47235.0, 58855.0, 72355.0, 87795.0, 105390.0,
                                            125280.0, 147605.0, 172605.0, 200430.0, 231230.0, 265270.0, 302710.0,
                                            343835.0, 388815.0, 437955.0, 491435.0, 549580.0, 612580.0, 680625.0,
                                            754225.0, 833590.0, 919100.0, 1011150.0, 1110150.0, 1216340.0, 1330150.0,
                                            1452220.0, 1582820.0, 1722630.0, 1872150.0, 2031895.0, 2202615.0, 2384865.0,
                                            2579215.0, 2786485.0, 3007525.0, 3242970.0, 3493720.0, 3760960.0, 4045400.0,
                                            4348295.0, 4670675.0, 5013875.0, 5378995.0, 5767450.0, 6180990.0, 6620835.0,
                                            7088835.0, 7603021.0, 8167447.0, 8786080.0, 9463831.0, 10205936.0,
                                            11017569.0, 11904609.0, 12873288.0, 13930648.0, 15083692.0, 16340773.0,
                                            17778723.0, 19419056.0, 21285921.0, 23405084.0, 25805305.0, 28517911.0,
                                            31578623.0, 35025492.0, 38900762.0, 43251306.0, 48128003.0, 53585955.0,
                                            59688435.0, 66501447.0, 74100425.0, 82565318.0, 91984060.0, 102454644.0,
                                            114142944.0, 127537143.0, 142470215.0, 159083828.0, 177531140.0,
                                            197979890.0, 220611122.0, 245617334.0, 273213742.0, 303626245.0, 0.0)
        self.player_progress = (0.0, 55.0, 220.0, 495.0, 880.0, 1400.0, 2010.0, 2765.0, 3640.0, 4635.0, 5750.0, 7040.0,
                                8400.0, 9945.0, 11620.0, 13500.0, 15440.0, 17595.0, 19890.0, 22325.0, 25000.0, 27825.0,
                                30800.0, 34040.0, 37440.0, 41125.0, 44980.0, 49140.0, 53480.0, 58145.0, 63000.0,
                                68045.0, 73600.0, 79365.0, 85510.0, 92050.0, 99000.0, 106190.0, 113810.0, 122070.0,
                                130600.0, 139810.0, 149520.0, 159745.0, 170720.0, 182250.0, 194350.0, 207270.0,
                                221040.0, 235445.0, 250750.0, 267240.0, 284440.0, 302895.0, 322380.0, 343200.0,
                                365120.0, 388455.0, 413540.0, 439845.0, 468000.0, 514186.0, 564426.0, 618633.0,
                                677751.0, 742105.0, 811633.0, 887040.0, 968679.0, 1057360.0, 1153044.0, 1257081.0,
                                1437950.0, 1640333.0, 1866865.0, 2119163.0, 2400221.0, 2712606.0, 3060712.0, 3446869.0,
                                3875270.0, 4350544.0, 4876697.0, 5457952.0, 6102480.0, 6813012.0, 7598978.0, 8464893.0,
                                9418742.0, 10470584.0, 11688300.0, 13394199.0, 14933072.0, 16613613.0, 18447312.0,
                                20448750.0, 22631232.0, 25006212.0, 27596408.0, 30412503.0, 0.0)

        self.frame_per_cart = (0, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 56,
                               59, 62, 65, 68, 71, 74, 77, 80, 83, 87, 91, 95, 99, 103, 107, 111, 115, 119, 123, 128,
                               133, 138, 143, 148, 153, 158, 163, 168, 173, 179, 185, 191, 197, 203, 209, 215, 221, 227,
                               233, 240, 247, 254, 261, 268, 275, 282, 289, 296, 303, 312, 321, 330, 339, 348, 357, 366,
                               375, 384, 393, 406, 419, 432, 445, 458, 471, 484, 497, 510, 523, 542, 561, 580, 599, 618,
                               637, 656, 675, 694, 720)
        self.exp_per_cart = (0.0, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.35, 0.37, 0.39, 0.41,
                             0.43, 0.45, 0.47, 0.49, 0.51, 0.53, 0.56, 0.59, 0.62, 0.65, 0.68, 0.71, 0.74, 0.77, 0.8,
                             0.83, 0.87, 0.91, 0.95, 0.99, 1.03, 1.07, 1.11, 1.15, 1.19, 1.23, 1.28, 1.33, 1.38, 1.43,
                             1.48, 1.53, 1.58, 1.63, 1.68, 1.73, 1.79, 1.85, 1.91, 1.97, 2.03, 2.09, 2.15, 2.21, 2.27,
                             2.33, 2.4, 2.47, 2.54, 2.61, 2.68, 2.75, 2.82, 2.89, 2.96, 3.03, 3.12, 3.21, 3.3, 3.39,
                             3.48, 3.57, 3.66, 3.75, 3.84, 3.93, 4.06, 4.19, 4.32, 4.45, 4.58, 4.71, 4.84, 4.97, 5.1,
                             5.23, 5.42, 5.61, 5.8, 5.99, 6.18, 6.37, 6.56, 6.75, 6.94, 7.2)
        self.money_per_cart = (0.0, 0.12, 0.125, 0.13, 0.135, 0.14, 0.145, 0.15, 0.155, 0.16, 0.165, 0.175, 0.185,
                               0.195, 0.205, 0.215, 0.225, 0.235, 0.245, 0.255, 0.265, 0.28, 0.295, 0.31, 0.325, 0.34,
                               0.355, 0.37, 0.385, 0.4, 0.415, 0.435, 0.455, 0.475, 0.495, 0.515, 0.535, 0.555, 0.575,
                               0.595, 0.615, 0.64, 0.665, 0.69, 0.715, 0.74, 0.765, 0.79, 0.815, 0.84, 0.865, 0.895,
                               0.925, 0.955, 0.985, 1.015, 1.045, 1.075, 1.105, 1.135, 1.165, 1.2, 1.235, 1.27, 1.305,
                               1.34, 1.375, 1.41, 1.445, 1.48, 1.515, 1.56, 1.605, 1.65, 1.695, 1.74, 1.785, 1.83,
                               1.875, 1.92, 1.965, 2.03, 2.095, 2.16, 2.225, 2.29, 2.355, 2.42, 2.485, 2.55, 2.615,
                               2.71, 2.805, 2.9, 2.995, 3.09, 3.185, 3.28, 3.375, 3.47, 3.6)

        self.unlocked_tracks = ([], [], [], [], [], [], [], [], [], [5, 6],
                                [], [], [], [], [], [], [], [], [], [7, 8],
                                [], [], [], [], [], [], [], [], [], [9, 10],
                                [], [], [], [], [], [], [], [], [], [11, 12],
                                [], [], [], [], [], [], [], [], [], [13, 14],
                                [], [], [], [], [15, 16], [], [], [], [], [17, 18],
                                [], [], [], [], [19, 20], [], [], [], [], [21, ],
                                [], [], [], [], [22, ], [], [], [], [], [23, 24],
                                [], [], [], [], [25, 26], [], [], [], [], [27, 28],
                                [], [], [], [], [29, 30], [], [], [], [], [31, 32])

    def save_state(self):
        self.game_config['graphics']['screen_resolution'] = str(self.screen_resolution[0]) + ',' \
                                                          + str(self.screen_resolution[1])
        self.game_config['graphics']['fps_display_enabled'] = str(self.fps_display_enabled)
        self.game_config['graphics']['fps_display_update_interval'] = str(self.fps_display_update_interval)

        with open('game_config.ini', 'w') as configfile:
            self.game_config.write(configfile)
