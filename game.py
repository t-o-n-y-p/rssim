import sys
import logging
from collections import defaultdict
import configparser
import os
import io

import pygame


class Game:
    def __init__(self, caption, screen_resolution, frame_rate, base_offset):
        self.logs_config = configparser.RawConfigParser()
        self.logger = logging.getLogger('game')
        self.logs_stream = None
        self.logs_file = None
        self.manage_logs_config()
        # since map can be moved, all objects should also be moved, that's why we need base offset here
        self.base_offset = base_offset
        self.frame_rate = frame_rate
        self.game_paused = False
        self.objects = []
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # is not used at the moment
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode(screen_resolution, pygame.SRCALPHA)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.key_down_handlers = defaultdict(list)
        self.key_up_handlers = defaultdict(list)
        self.mouse_handlers = []

    def manage_logs_config(self):
        if os.path.exists('user_cfg/logs_config.ini'):
            self.logs_config.read('user_cfg/logs_config.ini')
        else:
            self.logs_config.read('default_cfg/logs_config.ini')

        if not os.path.exists('logs'):
            os.mkdir('logs')

        self.logger.setLevel(self.logs_config['logs_config'].getint('level'))
        session = self.logs_config['logs_config'].getint('session')
        # logs_handler = logging.FileHandler('logs/session_{}.log'.format(session))
        self.logs_stream = io.StringIO(initial_value='------- Session {} started -------'.format(session))
        logs_handler = logging.StreamHandler(stream=self.logs_stream)
        logs_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(logs_handler)
        self.logs_file = open('logs/session_{}.log'.format(session), 'w')
        session += 1
        self.logs_config['logs_config']['session'] = str(session)
        if not os.path.exists('user_cfg'):
            os.mkdir('user_cfg')

        with open('user_cfg/logs_config.ini', 'w') as configfile:
            self.logs_config.write(configfile)

    def update(self):
        for o in self.objects:
            # some objects should be updated even after game is paused
            o.update(self.game_paused)

    def draw(self):
        for o in self.objects:
            o.draw(self.surface, self.base_offset)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.key_down_handlers[event.key]:
                    handler(event.key)
            elif event.type == pygame.KEYUP:
                for handler in self.key_up_handlers[event.key]:
                    handler(event.key)
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        while True:
            self.logger.info('frame begins')
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.logger.info('frame ends')
            new_lines = self.logs_stream.getvalue()
            self.logs_stream.seek(0, 0)
            self.logs_stream.truncate(0)
            if new_lines is not None:
                self.logs_file.write(new_lines)

            self.clock.tick(self.frame_rate)
            if self.clock.get_fps() > 0:
                self.logger.critical('FPS: {}'.format(round(self.clock.get_fps())))
