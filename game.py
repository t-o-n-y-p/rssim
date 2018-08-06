import pygame
import sys
import colors

from collections import defaultdict


class Game:
    def __init__(self, caption, screen_resolution, frame_rate, base_offset):
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

    def update(self):
        for o in self.objects:
            o.update(self.game_paused)

    def draw(self):
        self.surface.fill(colors.BLACK)
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
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.frame_rate)
