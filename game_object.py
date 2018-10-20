import configparser


class GameObject:
    def __init__(self):
        self.c = {}
        self.game_config = configparser.RawConfigParser()
        self.game_config.read('game_config.ini')
        self.parse_game_config()

    def parse_game_config(self):
        self.c['graphics'] = {}
        screen_resolution = self.game_config['graphics']['screen_resolution'].split(',')
        self.c['graphics']['screen_resolution'] = (int(screen_resolution[0]), int(screen_resolution[1]))
        self.c['graphics']['frame_rate'] = self.game_config['graphics'].getint('frame_rate')
        self.c['graphics']['vsync'] = self.game_config['graphics'].getboolean('vsync')
        map_resolution = self.game_config['graphics']['map_resolution'].split(',')
        self.c['graphics']['map_resolution'] = (int(map_resolution[0]), int(map_resolution[1]))
        base_offset_upper_left_limit = self.game_config['graphics']['base_offset_upper_left_limit'].split(',')
        self.c['graphics']['base_offset_upper_left_limit'] = (int(base_offset_upper_left_limit[0]),
                                                              int(base_offset_upper_left_limit[1]))
        base_offset_lower_right_limit = self.game_config['graphics']['base_offset_lower_right_limit'].split(',')
        self.c['graphics']['base_offset_lower_right_limit'] = (int(base_offset_lower_right_limit[0]),
                                                               int(base_offset_lower_right_limit[1]))
        base_offset = self.game_config['graphics']['base_offset'].split(',')
        self.c['graphics']['base_offset'] = (int(base_offset[0]), int(base_offset[1]))
        self.c['graphics']['top_bar_height'] = self.game_config['graphics'].getint('top_bar_height')
        self.c['graphics']['bottom_bar_height'] = self.game_config['graphics'].getint('bottom_bar_height')
        self.c['graphics']['bottom_bar_width'] = self.game_config['graphics'].getint('bottom_bar_width')
        self.c['graphics']['font_name'] = self.game_config['graphics']['font_name']
        self.c['graphics']['button_font_size'] = self.game_config['graphics'].getint('button_font_size')
        self.c['graphics']['day_font_size'] = self.game_config['graphics'].getint('day_font_size')
        button_text_color = self.game_config['graphics']['button_text_color'].split(',')
        for i in range(len(button_text_color)):
            button_text_color[i] = int(button_text_color[i])

        self.c['graphics']['button_text_color'] = tuple(button_text_color)
        bottom_bar_color = self.game_config['graphics']['bottom_bar_color'].split(',')
        for i in range(len(bottom_bar_color)):
            bottom_bar_color[i] = int(bottom_bar_color[i])

        self.c['graphics']['bottom_bar_color'] = tuple(bottom_bar_color)
        day_text_color = self.game_config['graphics']['day_text_color'].split(',')
        for i in range(len(day_text_color)):
            day_text_color[i] = int(day_text_color[i])

        self.c['graphics']['day_text_color'] = tuple(day_text_color)
        self.c['graphics']['fps_display_enabled'] = self.game_config['graphics'].getboolean('fps_display_enabled')

        self.c['direction'] = {}
        self.c['direction']['left'] = self.game_config['direction'].getint('left')
        self.c['direction']['right'] = self.game_config['direction'].getint('right')
        self.c['direction']['left_side'] = self.game_config['direction'].getint('left_side')
        self.c['direction']['right_side'] = self.game_config['direction'].getint('right_side')

        self.c['train_route_types'] = {}
        self.c['train_route_types']['entry_train_route'] \
            = self.game_config['train_route_types']['entry_train_route'].split(',')
        self.c['train_route_types']['exit_train_route'] \
            = self.game_config['train_route_types']['exit_train_route'].split(',')
        self.c['train_route_types']['approaching_train_route'] \
            = self.game_config['train_route_types']['approaching_train_route'].split(',')

        self.c['signal_config'] = {}
        self.c['signal_config']['red_signal'] = self.game_config['signal_config']['red_signal']
        self.c['signal_config']['green_signal'] = self.game_config['signal_config']['green_signal']
        self.c['signal_config']['signal_image_base_path'] = self.game_config['signal_config']['signal_image_base_path']

        self.c['signal_image_path'] = {}
        self.c['signal_image_path'][self.c['signal_config']['red_signal']] \
            = self.game_config['signal_image_path']['red_signal']
        self.c['signal_image_path'][self.c['signal_config']['green_signal']] \
            = self.game_config['signal_image_path']['green_signal']

        self.c['train_config'] = {}
        self.c['train_config']['train_cart_image_path'] = self.game_config['train_config']['train_cart_image_path']
        train_acceleration_factor = self.game_config['train_config']['train_acceleration_factor'].split(',')
        for i in range(len(train_acceleration_factor)):
            train_acceleration_factor[i] = int(train_acceleration_factor[i])

        self.c['train_config']['train_acceleration_factor'] = tuple(train_acceleration_factor)
        self.c['train_config']['train_acceleration_factor_length'] \
            = self.game_config['train_config'].getint('train_acceleration_factor_length')
        self.c['train_config']['train_maximum_speed'] = self.game_config['train_config'].getint('train_maximum_speed')

        self.c['dispatcher_config'] = {}
        self.c['dispatcher_config']['tracks_ready'] = self.game_config['dispatcher_config'].getint('tracks_ready')
        main_priority_tracks_parsed = self.game_config['dispatcher_config']['main_priority_tracks'].split('|')
        for i in range(len(main_priority_tracks_parsed)):
            main_priority_tracks_parsed[i] = main_priority_tracks_parsed[i].split(',')
            for j in range(len(main_priority_tracks_parsed[i])):
                main_priority_tracks_parsed[i][j] = main_priority_tracks_parsed[i][j].split('-')
                for k in range(len(main_priority_tracks_parsed[i][j])):
                    main_priority_tracks_parsed[i][j][k] = int(main_priority_tracks_parsed[i][j][k])

                main_priority_tracks_parsed[i][j] = tuple(main_priority_tracks_parsed[i][j])

            main_priority_tracks_parsed[i] = tuple(main_priority_tracks_parsed[i])

        self.c['dispatcher_config']['main_priority_tracks'] = tuple(main_priority_tracks_parsed)
        pass_through_priority_tracks = self.game_config['dispatcher_config']['pass_through_priority_tracks'].split('|')
        for i in range(len(pass_through_priority_tracks)):
            pass_through_priority_tracks[i] = pass_through_priority_tracks[i].split(',')
            for j in range(len(pass_through_priority_tracks[i])):
                pass_through_priority_tracks[i][j] = int(pass_through_priority_tracks[i][j])

            pass_through_priority_tracks[i] = tuple(pass_through_priority_tracks[i])

        self.c['dispatcher_config']['pass_through_priority_tracks'] = tuple(pass_through_priority_tracks)
        train_creation_timeout = self.game_config['dispatcher_config']['train_creation_timeout'].split(',')
        self.c['dispatcher_config']['train_creation_timeout'] = (int(train_creation_timeout[0]),
                                                                 int(train_creation_timeout[1]),
                                                                 int(train_creation_timeout[2]),
                                                                 int(train_creation_timeout[3]))

        self.c['switch_types'] = {}
        self.c['switch_types']['left_entry_railroad_switch'] \
            = self.game_config['switch_types']['left_entry_railroad_switch']
        self.c['switch_types']['left_exit_railroad_switch'] \
            = self.game_config['switch_types']['left_exit_railroad_switch']
        self.c['switch_types']['right_entry_railroad_switch'] \
            = self.game_config['switch_types']['right_entry_railroad_switch']
        self.c['switch_types']['right_exit_railroad_switch'] \
            = self.game_config['switch_types']['right_exit_railroad_switch']

        self.c['crossover_types'] = {}
        self.c['crossover_types']['left_entry_crossover'] = self.game_config['crossover_types']['left_entry_crossover']
        self.c['crossover_types']['left_exit_crossover'] = self.game_config['crossover_types']['left_exit_crossover']
        self.c['crossover_types']['right_entry_crossover'] \
            = self.game_config['crossover_types']['right_entry_crossover']
        self.c['crossover_types']['right_exit_crossover'] = self.game_config['crossover_types']['right_exit_crossover']

    def read_state(self):
        pass

    def save_state(self):
        pass

    # simply pass this to be overridden by each object: "game_stopped" restricts objects that can be updated
    # after user paused the game
    def update(self, game_paused):
        pass

    def update_sprite(self, base_offset):
        pass
