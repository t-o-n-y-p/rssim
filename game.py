from configparser import RawConfigParser
from io import StringIO
from logging import StreamHandler, Formatter, getLogger
from os import path, mkdir
from time import time, perf_counter
from ctypes import c_long

from win32api import GetCursorPos
from win32gui import GetActiveWindow, GetWindowRect, SetWindowPos
from win32con import HWND_TOP, SWP_NOREDRAW
from pyglet import gl
from pyglet.image import load
from pyglet.text import Label
from pyglet.graphics import Batch, OrderedGroup
from pyglet.window import Window, mouse

from mini_map import MiniMap
from exceptions import VideoAdapterNotSupportedException
from game_config import GameConfig


def _game_window_is_active(fn):
    def _handle_if_game_window_is_active(*args, **kwargs):
        if args[0].surface.visible:
            fn(*args, **kwargs)

    return _handle_if_game_window_is_active


def _left_button(fn):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            fn(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


class Game:
    def __init__(self, caption):
        max_texture_size = c_long(0)
        gl.glGetIntegerv(gl.GL_MAX_TEXTURE_SIZE, max_texture_size)
        if max_texture_size.value < 8192:
            raise VideoAdapterNotSupportedException

        self.logs_config = RawConfigParser()
        self.logger = getLogger('game')
        self.logs_stream = StringIO()
        self.logs_file = None
        self.manage_logs_config()
        self.logger.debug('main logger created')
        self.c = GameConfig()
        self.main_map = None
        self.scheduler = None
        # since map can be moved, all objects should also be moved, that's why we need base offset here
        self.base_offset = self.c.base_offset
        self.logger.debug('base offset set: {} {}'.format(self.base_offset[0], self.base_offset[1]))
        self.game_paused = False
        self.logger.debug('game paused set: {}'.format(self.game_paused))
        self.objects = []
        surface = Window(width=self.c.screen_resolution[0], height=self.c.screen_resolution[1],
                         caption=caption, style='borderless', vsync=self.c.vsync)
        self.surface = surface
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        self.batch = Batch()
        self.map_ordered_group = OrderedGroup(0)
        self.signals_and_trains_ordered_group = OrderedGroup(1)
        self.boarding_lights_ordered_group = OrderedGroup(2)
        self.twilight_ordered_group = OrderedGroup(3)  # reserved for future use
        self.twilight_artifacts_ordered_group = OrderedGroup(4)  # reserved for future use
        self.top_bottom_bars_ordered_group = OrderedGroup(5)
        self.buttons_general_borders_day_text_ordered_group = OrderedGroup(6)
        self.buttons_text_and_borders_ordered_group = OrderedGroup(7)
        self.loading_shadow_ordered_group = OrderedGroup(8)
        self.surface.dispatch_event('on_draw')
        self.surface.flip()
        self.game_window_handler = GetActiveWindow()
        self.game_window_position = GetWindowRect(self.game_window_handler)
        self.absolute_mouse_pos = GetCursorPos()
        self.fps_display_label = None
        if self.c.fps_display_enabled:
            self.fps_display_label = Label(text='0 FPS', font_name='Courier New',
                                           font_size=self.c.iconify_close_button_font_size,
                                           x=self.c.screen_resolution[0] - 75,
                                           y=self.c.screen_resolution[1] - self.c.top_bar_height // 2,
                                           anchor_x='right', anchor_y='center',
                                           batch=self.batch, group=self.buttons_text_and_borders_ordered_group)
        self.surface.set_icon(load('icon.ico'))
        self.logger.debug('created screen with resolution {}'
                          .format(self.c.screen_resolution))
        self.logger.debug('caption set: {}'.format(caption))
        # pyglet.clock.set_fps_limit(self.c.frame_rate)
        # self.logger.debug('clock created')
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.surface.set_location(0, 0)
        self.app_window_move_mode = False
        self.map_move_mode = [False, ]
        self.app_window_move_offset = ()
        mini_map_image = load('img/mini_map/4/mini_map.png')
        self.mini_map_tip = MiniMap(image=mini_map_image,
                                    x=self.c.screen_resolution[0] - mini_map_image.width,
                                    y=self.c.screen_resolution[1] - self.c.top_bar_height - 4 - mini_map_image.height,
                                    batch=self.batch, group=self.top_bottom_bars_ordered_group,
                                    viewport_border_group=self.buttons_general_borders_day_text_ordered_group,
                                    game_config=self.c)
        self.mini_map_timer = 0
        self.dispatcher = None
        self.logger.warning('game init completed')

        @surface.event
        def on_draw():
            time_1 = perf_counter()
            for o in self.objects:
                o.update_sprite(self.base_offset)

            time_2 = perf_counter()
            self.surface.clear()
            self.batch.draw()
            time_3 = perf_counter()
            self.logger.warning('updating sprites: {} sec'.format(time_2 - time_1))
            self.logger.warning('drawing sprites: {} sec'.format(time_3 - time_2))

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

        @surface.event
        def on_mouse_leave(x, y):
            for i in self.on_mouse_leave_handlers:
                i(x, y)

    def manage_logs_config(self):
        self.logs_config.read('logs_config.ini')
        if not path.exists('logs'):
            mkdir('logs')

        self.logger.setLevel(self.logs_config['logs_config']['level'])
        session = self.logs_config['logs_config'].getint('session')
        logs_handler = StreamHandler(stream=self.logs_stream)
        # logs_handler = logging.FileHandler('logs/logs_session_{}.log'.format(session))
        logs_handler.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(logs_handler)
        self.logs_file = open('logs/session_{}.log'.format(session), 'w')
        session += 1
        self.logs_config['logs_config']['session'] = str(session)

        with open('logs_config.ini', 'w') as configfile:
            self.logs_config.write(configfile)

    def update(self):
        time_1 = perf_counter()
        for o in self.objects:
            o.update(self.game_paused)

        if self.mini_map_tip.condition_met and not self.map_move_mode[0]:
            if time() - self.mini_map_timer > 1:
                self.mini_map_tip.on_condition_not_met()

        time_2 = perf_counter()
        self.logger.warning('updating: {} sec'.format(time_2 - time_1))

    @_game_window_is_active
    @_left_button
    def handle_mouse_press(self, x, y, button, modifiers):
        y = self.c.screen_resolution[1] - y
        if x in range(0, self.c.screen_resolution[0] - 70) and y in range(0, self.c.top_bar_height):
            self.app_window_move_mode = True
            self.app_window_move_offset = (x, y)

        if not self.scheduler.is_activated and x in range(0, self.c.screen_resolution[0]) \
                and y in range(self.c.top_bar_height, self.c.screen_resolution[1] - self.c.bottom_bar_height):
            self.map_move_mode[0] = True
            self.mini_map_tip.on_condition_met()

    @_game_window_is_active
    @_left_button
    def handle_mouse_release(self, x, y, button, modifiers):
        self.app_window_move_mode = False
        self.map_move_mode[0] = False
        self.mini_map_timer = time()

    @_game_window_is_active
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.map_move_mode[0]:
            # if left mouse button is pressed and user moves mouse, we move entire map with all its content
            self.logger.debug('user drags map')
            self.logger.debug('old offset: {}'.format(self.base_offset))
            self.base_offset = (self.base_offset[0] + dx, self.base_offset[1] + dy)
            self.logger.debug('new offset: {}'.format(self.base_offset))
            # but not beyond limits
            if self.base_offset[0] > self.c.base_offset_lower_right_limit[0]:
                self.base_offset = (self.c.base_offset_lower_right_limit[0], self.base_offset[1])
            if self.base_offset[0] < self.c.base_offset_upper_left_limit[0]:
                self.base_offset = (self.c.base_offset_upper_left_limit[0], self.base_offset[1])
            if self.base_offset[1] > self.c.base_offset_lower_right_limit[1]:
                self.base_offset = (self.base_offset[0], self.c.base_offset_lower_right_limit[1])
            if self.base_offset[1] < self.c.base_offset_upper_left_limit[1]:
                self.base_offset = (self.base_offset[0], self.c.base_offset_upper_left_limit[1])

            self.logger.debug('new limited offset: {}'.format(self.base_offset))
            self.main_map.update_sprite(self.base_offset)
            for s in self.dispatcher.signals:
                s.update_sprite(self.base_offset)

        if self.app_window_move_mode:
            self.absolute_mouse_pos = GetCursorPos()
            self.game_window_position = GetWindowRect(self.game_window_handler)
            SetWindowPos(self.game_window_handler, HWND_TOP,
                         self.absolute_mouse_pos[0] - self.app_window_move_offset[0],
                         self.absolute_mouse_pos[1] - self.app_window_move_offset[1],
                         self.game_window_position[2] - self.game_window_position[0],
                         self.game_window_position[3] - self.game_window_position[1],
                         SWP_NOREDRAW)

    def run(self):
        fps_timer = 0.0
        while True:
            self.logger.info('frame begins')
            time_1 = perf_counter()
            # pyglet.clock.tick()
            self.surface.dispatch_events()
            self.update()
            self.surface.dispatch_event('on_draw')
            time_4 = perf_counter()
            self.surface.flip()
            self.logger.info('frame ends')
            if self.fps_display_label is not None \
                    and perf_counter() - fps_timer > self.c.fps_display_update_interval:
                self.fps_display_label.text = str(round(float(1/(time_4 - time_1)))) + ' FPS'
                fps_timer = perf_counter()

            new_lines = self.logs_stream.getvalue()
            self.logs_stream.seek(0, 0)
            self.logs_stream.truncate(0)
            if new_lines is not None:
                self.logs_file.write(new_lines)
