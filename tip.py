from logging import getLogger

from pyglet.image import load
from pyglet.sprite import Sprite
from pyglet.text import Label

from game_object import GameObject


def _condition_is_not_already_met(fn):
    def _set_condition_met_only_if_it_is_not_already_met(*args, **kwargs):
        if not args[0].condition_met:
            fn(*args, **kwargs)

    return _set_condition_met_only_if_it_is_not_already_met


class Tip(GameObject):
    def __init__(self, image, x, y, batch, group, viewport_border_group, game_config, texts_list, colors_list):
        super().__init__(game_config)
        self.logger = getLogger('game.tip')
        self.logger.debug('------- START INIT -------')
        self.image = image
        self.batch = batch
        self.group = group
        self.viewport_border_group = viewport_border_group
        self.x = x
        self.y = y
        self.sprite = None
        self.viewport_border = None
        self.viewport_border_image = load('img/viewport_border.png')
        self.logger.debug('image loaded: {}'.format(image))
        self.condition_met = False
        self.logger.debug('condition_met: {}'.format(self.condition_met))
        self.text_labels_list = []
        self.texts_list = texts_list
        self.colors_list = colors_list
        self.logger.debug('------- END INIT -------')
        self.logger.warning('tip init completed')

    def update_sprite(self, base_offset):
        self.logger.debug('------- START DRAWING -------')
        if self.condition_met:
            if self.sprite.opacity < 255:
                self.sprite.opacity += 15

        if not self.condition_met:
            if self.sprite is not None:
                self.sprite.opacity -= 15
                if self.sprite.opacity <= 0:
                    self.sprite.delete()
                    self.sprite = None

            self.logger.debug('condition not met, no need to show tip')

        self.logger.debug('------- END DRAWING -------')
        self.logger.info('tip drawing processed')

    @_condition_is_not_already_met
    def on_condition_met(self):
        self.condition_met = True
        self.sprite = Sprite(self.image, x=self.x, y=self.y, batch=self.batch, group=self.group)
        self.sprite.opacity = 0
        self.text_labels_list = []
        for i in range(len(self.texts_list)):
            self.text_labels_list.append(Label(self.texts_list[i], font_name=self.c.font_name,
                                               font_size=self.c.unlock_tip_font_size, color=self.colors_list[i],
                                               x=self.x + self.image.width // 2, y=self.y + self.image.height // 2,
                                               anchor_x='center', anchor_y='center', align='center', batch=self.batch,
                                               group=self.viewport_border_group))

    def on_condition_not_met(self):
        self.condition_met = False
        for i in self.text_labels_list:
            i.delete()

        self.text_labels_list.clear()

    def set_new_text(self, texts_list):
        self.texts_list = texts_list
        for i in range(len(self.text_labels_list)):
            self.text_labels_list[i].text = texts_list[i]
