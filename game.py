import configparser
import io
import logging
import os
import time
import ctypes

import win32api
import win32gui
import win32con
import pyglet

from onboarding_tips import OnboardingTips
from main_map import NotSupportedVideoAdapterException


def _game_window_is_active(fn):
    def _handle_if_game_window_is_active(*args, **kwargs):
        if args[0].surface.visible:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_active


class Game:
    def __init__(self, caption):
        max_texture_size = ctypes.c_long(0)
        pyglet.gl.glGetIntegerv(pyglet.gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < 8192:
            raise NotSupportedVideoAdapterException

        self.logs_config = configparser.RawConfigParser()
        self.logger = logging.getLogger('game')
        self.logs_stream = io.StringIO()
        self.logs_file = None
        self.manage_logs_config()
        self.logger.debug('main logger created')
        self.c = {}
        self.game_config = configparser.RawConfigParser()
        self.game_config.read('game_config.ini')
        self.parse_game_config()
        # since map can be moved, all objects should also be moved, that's why we need base offset here
        self.base_offset = self.c['graphics']['base_offset']
        self.logger.debug('base offset set: {} {}'.format(self.base_offset[0], self.base_offset[1]))
        self.game_paused = False
        self.logger.debug('game paused set: {}'.format(self.game_paused))
        self.objects = []
        surface = pyglet.window.Window(width=self.c['graphics']['screen_resolution'][0],
                                       height=self.c['graphics']['screen_resolution'][1],
                                       caption=caption, style='borderless', vsync=False)
        self.surface = surface
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        self.batch = pyglet.graphics.Batch()
        self.map_ordered_group = pyglet.graphics.OrderedGroup(0)
        self.signals_and_trains_ordered_group = pyglet.graphics.OrderedGroup(1)
        self.boarding_lights_ordered_group = pyglet.graphics.OrderedGroup(2)
        self.twilight_ordered_group = pyglet.graphics.OrderedGroup(3)  # reserved for future use
        self.top_bottom_bars_clock_face_ordered_group = pyglet.graphics.OrderedGroup(4)
        self.buttons_general_borders_day_text_ordered_group = pyglet.graphics.OrderedGroup(5)
        self.buttons_text_minute_hand_ordered_group = pyglet.graphics.OrderedGroup(6)
        self.buttons_borders_hour_hand_ordered_group = pyglet.graphics.OrderedGroup(7)
        self.loading_shadow_ordered_group = pyglet.graphics.OrderedGroup(8)
        self.fade_vertex = self.batch.add(4, pyglet.gl.GL_QUADS, self.loading_shadow_ordered_group,
                                          ('v2i/static', (0, 0, self.c['graphics']['screen_resolution'][0], 0,
                                                          self.c['graphics']['screen_resolution'][0],
                                                          self.c['graphics']['screen_resolution'][1],
                                                          0, self.c['graphics']['screen_resolution'][1])),
                                          ('c4B', (0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255))
                                          )
        self.fade_vertex_opacity = 255
        self.surface.dispatch_event('on_draw')
        self.surface.flip()
        self.game_window_handler = win32gui.GetActiveWindow()
        self.game_window_position = win32gui.GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = win32api.GetCursorPos()
        self.fps_display_label = None
        if self.c['graphics']['fps_display_enabled']:
            self.fps_display_label \
                = pyglet.text.Label(text='0', font_name='Courier New',
                                    font_size=self.c['graphics']['button_font_size'],
                                    x=self.c['graphics']['screen_resolution'][0] - 75,
                                    y=self.c['graphics']['screen_resolution'][1]
                                    - self.c['graphics']['top_bar_height'] // 2,
                                    anchor_x='right', anchor_y='center',
                                    batch=self.batch, group=self.buttons_text_minute_hand_ordered_group)

        self.surface.set_icon(pyglet.image.load('icon.ico'))
        self.logger.debug('created screen with resolution {}'
                          .format(self.c['graphics']['screen_resolution']))
        self.logger.debug('caption set: {}'.format(caption))
        # pyglet.clock.set_fps_limit(self.c['graphics']['frame_rate'])
        self.logger.debug('clock created')
        self.main_map_tiles = None
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.surface.set_location(0, 0)
        self.app_window_move_mode = False
        self.map_move_mode = False
        self.app_window_move_offset = ()
        mini_map_image = pyglet.image.load('img/mini_map/5/mini_map.png')
        self.mini_map_tip \
            = OnboardingTips(image=mini_map_image,
                             x=self.c['graphics']['screen_resolution'][0] - mini_map_image.width,
                             y=self.c['graphics']['screen_resolution'][1] - self.c['graphics']['top_bar_height']
                             - 4 - mini_map_image.height,
                             tip_type='mini_map', batch=self.batch,
                             group=self.top_bottom_bars_clock_face_ordered_group,
                             viewport_border_group=self.buttons_general_borders_day_text_ordered_group)
        self.mini_map_timer = 0
        self.dispatcher = None
        self.logger.warning('game init completed')

        @surface.event
        def on_draw():
            self.logger.critical('start update sprites')
            for o in self.objects:
                o.update_sprite(self.base_offset)

            if self.fade_vertex is not None:
                if self.fade_vertex_opacity > 0:
                    self.fade_vertex_opacity -= 17
                    self.fade_vertex.colors = (0, 0, 0, self.fade_vertex_opacity,
                                               0, 0, 0, self.fade_vertex_opacity,
                                               0, 0, 0, self.fade_vertex_opacity,
                                               0, 0, 0, self.fade_vertex_opacity)
                else:
                    self.fade_vertex.delete()
                    self.fade_vertex = None

            self.logger.critical('end update sprites')

            self.surface.clear()
            self.batch.invalidate()
            self.batch.draw()

        @surface.event
        def on_mouse_press(x, y, button, modifiers):
            for i in self.on_mouse_press_handlers:
                i(x, y, button, modifiers)

        @surface.event
        def on_mouse_release(x, y, button, modifiers):
            for i in self.on_mouse_release_handlers:
                i(x, y, button, modifiers)

        @surface.event
        def on_mouse_motion(x, y, dx, dy):
            for i in self.on_mouse_motion_handlers:
                i(x, y, dx, dy)

        @surface.event
        def on_mouse_drag(x, y, dx, dy, button, modifiers):
            for i in self.on_mouse_drag_handlers:
                i(x, y, dx, dy, button, modifiers)

    def manage_logs_config(self):
        self.logs_config.read('logs_config.ini')
        if not os.path.exists('logs'):
            os.mkdir('logs')

        self.logger.setLevel(self.logs_config['logs_config']['level'])
        session = self.logs_config['logs_config'].getint('session')
        logs_handler = logging.StreamHandler(stream=self.logs_stream)
        # logs_handler = logging.FileHandler('logs/logs_session_{}.log'.format(session))
        logs_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(logs_handler)
        self.logs_file = open('logs/session_{}.log'.format(session), 'w')
        session += 1
        self.logs_config['logs_config']['session'] = str(session)

        with open('logs_config.ini', 'w') as configfile:
            self.logs_config.write(configfile)

    def parse_game_config(self):
        self.c['graphics'] = {}
        screen_resolution = self.game_config['graphics']['screen_resolution'].split(',')
        self.c['graphics']['screen_resolution'] = (int(screen_resolution[0]), int(screen_resolution[1]))
        self.c['graphics']['frame_rate'] = self.game_config['graphics'].getint('frame_rate')
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
        self.c['graphics']['fps_display_update_interval'] \
            = self.game_config['graphics'].getfloat('fps_display_update_interval')

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
        self.c['dispatcher_config']['tracks_ready'] = self.game_config['dispatcher_config'].getint('tracks_ready')
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

    def update(self):
        for o in self.objects:
            o.update(self.game_paused)

        if self.mini_map_tip.condition_met and not self.map_move_mode:
            if time.time() - self.mini_map_timer > 1:
                self.mini_map_tip.condition_met = False

    @_game_window_is_active
    def handle_mouse_press(self, x, y, button, modifiers):
        y = self.c['graphics']['screen_resolution'][1] - y
        if x in range(0, self.c['graphics']['screen_resolution'][0] - 70) \
                and y in range(0, self.c['graphics']['top_bar_height']) and button == pyglet.window.mouse.LEFT:
            self.app_window_move_mode = True
            self.app_window_move_offset = (x, y)

        if x in range(0, self.c['graphics']['screen_resolution'][0]) \
                and y in range(self.c['graphics']['top_bar_height'],
                               self.c['graphics']['screen_resolution'][1]
                               - self.c['graphics']['bottom_bar_height']) and button == pyglet.window.mouse.LEFT:
            self.map_move_mode = True
            self.mini_map_tip.condition_met = True

    @_game_window_is_active
    def handle_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.app_window_move_mode = False
            self.map_move_mode = False
            self.mini_map_timer = time.time()

    @_game_window_is_active
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.map_move_mode:
            # if left mouse button is pressed and user moves mouse, we move entire map with all its content
            self.logger.debug('user drags map')
            self.logger.debug('old offset: {}'.format(self.base_offset))
            self.base_offset = (self.base_offset[0] + dx, self.base_offset[1] + dy)
            self.logger.debug('new offset: {}'.format(self.base_offset))
            # but not beyond limits
            if self.base_offset[0] > self.c['graphics']['base_offset_lower_right_limit'][0]:
                self.base_offset = (self.c['graphics']['base_offset_lower_right_limit'][0], self.base_offset[1])
            if self.base_offset[0] < self.c['graphics']['base_offset_upper_left_limit'][0]:
                self.base_offset = (self.c['graphics']['base_offset_upper_left_limit'][0], self.base_offset[1])
            if self.base_offset[1] > self.c['graphics']['base_offset_lower_right_limit'][1]:
                self.base_offset = (self.base_offset[0], self.c['graphics']['base_offset_lower_right_limit'][1])
            if self.base_offset[1] < self.c['graphics']['base_offset_upper_left_limit'][1]:
                self.base_offset = (self.base_offset[0], self.c['graphics']['base_offset_upper_left_limit'][1])

            self.logger.debug('new limited offset: {}'.format(self.base_offset))
            self.main_map_tiles.update_sprite(self.base_offset)
            for s in self.dispatcher.signals:
                s.update_sprite(self.base_offset)

        if self.app_window_move_mode:
            self.absolute_mouse_pos = win32api.GetCursorPos()
            self.game_window_position = win32gui.GetWindowRect(self.game_window_handler)
            win32gui.SetWindowPos(self.game_window_handler, win32con.HWND_TOP,
                                  self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
                                  self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
                                  self.game_window_position[2] - self.game_window_position[0],
                                  self.game_window_position[3] - self.game_window_position[1],
                                  win32con.SWP_NOREDRAW)

    def run(self):
        # pyglet.app.run()
        fps_timer = 0.0
        while True:
            self.logger.warning('frame begins')
            time_1 = time.perf_counter()
            # pyglet.clock.tick()
            self.surface.dispatch_events()
            time_2 = time.perf_counter()
            self.update()
            time_3 = time.perf_counter()
            self.surface.dispatch_event('on_draw')
            time_4 = time.perf_counter()
            self.surface.flip()
            self.logger.warning('frame ends')
            self.logger.critical('handling events: {} sec'.format(time_2 - time_1))
            self.logger.critical('updating: {} sec'.format(time_3 - time_2))
            self.logger.critical('drawing: {} sec'.format(time_4 - time_3))
            if self.fps_display_label is not None \
                    and time.perf_counter() - fps_timer > self.c['graphics']['fps_display_update_interval']:
                self.fps_display_label.text = str(round(float(1/(time_4 - time_1)))) + ' FPS'
                fps_timer = time.perf_counter()

            new_lines = self.logs_stream.getvalue()
            self.logs_stream.seek(0, 0)
            self.logs_stream.truncate(0)
            if new_lines is not None:
                self.logs_file.write(new_lines)
