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
        self.c['graphics']['background_image'] = self.game_config['graphics']['background_image']
        background_tile_resolution = self.game_config['graphics']['background_tile_resolution'].split(',')
        self.c['graphics']['background_tile_resolution'] = (int(background_tile_resolution[0]),
                                                            int(background_tile_resolution[1]))
        number_of_background_tiles = self.game_config['graphics']['number_of_background_tiles'].split(',')
        self.c['graphics']['number_of_background_tiles'] = (int(number_of_background_tiles[0]),
                                                            int(number_of_background_tiles[1]))
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

        self.c['base_route_types'] = {}
        self.c['base_route_types']['left_entry_base_route'] \
            = self.game_config['base_route_types']['left_entry_base_route']
        self.c['base_route_types']['left_exit_base_route'] \
            = self.game_config['base_route_types']['left_exit_base_route']
        self.c['base_route_types']['right_entry_base_route'] \
            = self.game_config['base_route_types']['right_entry_base_route']
        self.c['base_route_types']['right_exit_base_route'] \
            = self.game_config['base_route_types']['right_exit_base_route']
        self.c['base_route_types']['left_entry_platform_base_route'] \
            = self.game_config['base_route_types']['left_entry_platform_base_route']
        self.c['base_route_types']['right_entry_platform_base_route'] \
            = self.game_config['base_route_types']['right_entry_platform_base_route']
        self.c['base_route_types']['right_exit_platform_base_route'] \
            = self.game_config['base_route_types']['right_exit_platform_base_route']
        self.c['base_route_types']['left_exit_platform_base_route'] \
            = self.game_config['base_route_types']['left_exit_platform_base_route']

        self.c['direction'] = {}
        self.c['direction']['left'] = self.game_config['direction'].getint('left')
        self.c['direction']['right'] = self.game_config['direction'].getint('right')

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
        self.c['train_config']['train_braking_distance'] \
            = self.game_config['train_config'].getint('train_braking_distance')

        self.c['train_state_types'] = {}
        self.c['train_state_types']['pass_through'] = self.game_config['train_state_types']['pass_through']
        self.c['train_state_types']['approaching'] = self.game_config['train_state_types']['approaching']
        self.c['train_state_types']['approaching_pass_through'] \
            = self.game_config['train_state_types']['approaching_pass_through']
        self.c['train_state_types']['pending_boarding'] = self.game_config['train_state_types']['pending_boarding']
        self.c['train_state_types']['boarding_in_progress'] \
            = self.game_config['train_state_types']['boarding_in_progress']
        self.c['train_state_types']['boarding_complete'] = self.game_config['train_state_types']['boarding_complete']

        self.c['train_speed_state_types'] = {}
        self.c['train_speed_state_types']['move'] = self.game_config['train_speed_state_types']['move']
        self.c['train_speed_state_types']['accelerate'] = self.game_config['train_speed_state_types']['accelerate']
        self.c['train_speed_state_types']['decelerate'] = self.game_config['train_speed_state_types']['decelerate']
        self.c['train_speed_state_types']['stop'] = self.game_config['train_speed_state_types']['stop']

        self.c['dispatcher_config'] = {}
        first_priority_tracks = self.game_config['dispatcher_config']['first_priority_tracks'].split('|')
        for i in range(len(first_priority_tracks)):
            first_priority_tracks[i] = first_priority_tracks[i].split(',')
            for j in range(len(first_priority_tracks[i])):
                first_priority_tracks[i][j] = int(first_priority_tracks[i][j])

            first_priority_tracks[i] = tuple(first_priority_tracks[i])

        self.c['dispatcher_config']['first_priority_tracks'] = tuple(first_priority_tracks)
        second_priority_tracks = self.game_config['dispatcher_config']['second_priority_tracks'].split('|')
        for i in range(len(second_priority_tracks)):
            second_priority_tracks[i] = second_priority_tracks[i].split(',')
            for j in range(len(second_priority_tracks[i])):
                second_priority_tracks[i][j] = int(second_priority_tracks[i][j])

            second_priority_tracks[i] = tuple(second_priority_tracks[i])

        self.c['dispatcher_config']['second_priority_tracks'] = tuple(second_priority_tracks)
        pass_through_priority_tracks = self.game_config['dispatcher_config']['pass_through_priority_tracks'].split('|')
        for i in range(len(pass_through_priority_tracks)):
            pass_through_priority_tracks[i] = pass_through_priority_tracks[i].split(',')
            for j in range(len(pass_through_priority_tracks[i])):
                pass_through_priority_tracks[i][j] = int(pass_through_priority_tracks[i][j])

            pass_through_priority_tracks[i] = tuple(pass_through_priority_tracks[i])

        self.c['dispatcher_config']['pass_through_priority_tracks'] = tuple(pass_through_priority_tracks)
        train_creation_timeout = self.game_config['dispatcher_config']['train_creation_timeout'].split(',')
        self.c['dispatcher_config']['train_creation_timeout'] = (int(train_creation_timeout[0]),
                                                                 int(train_creation_timeout[1]))

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

    # simply pass this to be overridden by each object: "surface" is generic game screen, "base_offset" stands for
    # top left corner of entire map (it can be moved)
    def draw(self, surface, base_offset):
        pass

    # simply pass this to be overridden by each object: "game_stopped" restricts objects that can be updated
    # after user paused the game
    def update(self, game_paused):
        pass
