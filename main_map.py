import logging

import pyglet

from game_object import GameObject


class MainMap(GameObject):
    def __init__(self, batch, group):
        super().__init__()
        self.logger = logging.getLogger('game.main_map')
        self.logger.debug('------- START INIT -------')
        # load background texture tile
        self.sprites = []
        for i in range(5):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i].append(pyglet.sprite.Sprite(pyglet.image.load('img/map/4/{}-{}.png'.format(i, j)),
                                                            x=self.c['graphics']['base_offset'][0]+i*200,
                                                            y=self.c['graphics']['base_offset'][1]+j*300,
                                                            batch=batch, group=group))

        for i in range(5, 11):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i].append(pyglet.sprite.Sprite(pyglet.image.load('img/map/4/{}-{}.png'.format(i, j)),
                                                            x=self.c['graphics']['base_offset'][0]+1000+(i-5)*100,
                                                            y=self.c['graphics']['base_offset'][1]+j*300,
                                                            batch=batch, group=group))

        for i in range(11, 16):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i].append(pyglet.sprite.Sprite(pyglet.image.load('img/map/4/{}-{}.png'.format(i, j)),
                                                            x=self.c['graphics']['base_offset'][0]+1600+(i-11)*200,
                                                            y=self.c['graphics']['base_offset'][1]+j*300,
                                                            batch=batch, group=group))

        for i in range(16, 22):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i].append(pyglet.sprite.Sprite(pyglet.image.load('img/map/4/{}-{}.png'.format(i, j)),
                                                            x=self.c['graphics']['base_offset'][0]+2600+(i-16)*100,
                                                            y=self.c['graphics']['base_offset'][1]+j*300,
                                                            batch=batch, group=group))

        for i in range(22, 27):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i].append(pyglet.sprite.Sprite(pyglet.image.load('img/map/4/{}-{}.png'.format(i, j)),
                                                            x=self.c['graphics']['base_offset'][0]+3200+(i-22)*200,
                                                            y=self.c['graphics']['base_offset'][1]+j*300,
                                                            batch=batch, group=group))

        self.logger.debug('main map loaded')
        self.logger.debug('------- END INIT -------')
        self.logger.warning('main map init completed')

    def update_sprite(self, base_offset):
        for i in range(5):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i][j].position = (base_offset[0] + i * 200, base_offset[1] + j * 300)

        for i in range(5, 11):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i][j].position = (base_offset[0] + 1000 + (i - 5) * 100, base_offset[1] + j * 300)

        for i in range(11, 16):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i][j].position = (base_offset[0] + 1600 + (i - 11) * 200, base_offset[1] + j * 300)

        for i in range(16, 22):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i][j].position = (base_offset[0] + 2600 + (i - 16) * 100, base_offset[1] + j * 300)

        for i in range(22, 27):
            self.sprites.append([])
            for j in range(6):
                self.sprites[i][j].position = (base_offset[0] + 3200 + (i - 22) * 200, base_offset[1] + j * 300)
