from pyglet.sprite import Sprite

from ui import *
from database import USER_DB_CURSOR


def progress_bar_is_active(fn):
    def _handle_if_progress_bar_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_progress_bar_is_activated


class RectangleProgressBar:
    def __init__(self, logger):
        self.logger = logger
        self.is_activated = False
        self.screen_resolution = (1280, 720)
        self.position = (0, 0)
        self.offset = (0, 0)
        self.inactive_image = None
        self.inactive_sprite = None
        self.active_image = None
        self.active_sprite = None
        self.text_label = None
        self.opacity = 0
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.current_percent = 0

    @staticmethod
    def get_position(screen_resolution):
        pass

    def on_activate(self):
        self.is_activated = True
        self.text_label.create()
        if self.inactive_sprite is None:
            self.inactive_sprite = Sprite(self.inactive_image, x=self.position[0], y=self.position[1],
                                          batch=BATCHES['ui_batch'], group=GROUPS['button_background'])
            self.inactive_sprite.scale = get_bottom_bar_height(self.screen_resolution) / 80
            self.inactive_sprite.opacity = self.opacity

        if self.active_sprite is None:
            self.active_sprite = Sprite(self.active_image, x=self.position[0], y=self.position[1],
                                        batch=BATCHES['ui_batch'], group=GROUPS['button_text'])
            self.active_sprite.scale = get_bottom_bar_height(self.screen_resolution) / 80
            self.active_sprite.opacity = self.opacity

    def on_deactivate(self):
        self.is_activated = False

    def on_change_screen_resolution(self, screen_resolution, new_offset=None):
        if new_offset is not None:
            self.offset = new_offset

        self.screen_resolution = screen_resolution
        rel_position = self.get_position(self.screen_resolution)
        self.position = (self.offset[0] + rel_position[0], self.offset[1] + rel_position[1])
        self.text_label.on_change_screen_resolution(screen_resolution, new_offset=self.position)
        if self.inactive_sprite is not None:
            self.inactive_sprite.position = self.position
            self.inactive_sprite.scale = get_bottom_bar_height(self.screen_resolution) / 80

        if self.active_sprite is not None:
            self.active_sprite.position = self.position
            self.active_sprite.scale = get_bottom_bar_height(self.screen_resolution) / 80

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity <= 0:
            self.text_label.delete()
            self.inactive_sprite.delete()
            self.inactive_sprite = None
            self.active_sprite.delete()
            self.active_sprite = None
        else:
            self.text_label.on_update_opacity(self.opacity)
            if self.inactive_sprite is not None:
                self.inactive_sprite.opacity = self.opacity

            if self.active_sprite is not None:
                self.active_sprite.opacity = self.opacity

    def on_update_text_label_args(self, new_args):
        self.text_label.on_update_args(new_args)

    @progress_bar_is_active
    def on_update_progress_bar_state(self, current_value, maximum_value):
        if maximum_value == 0:
            self.current_percent = 0
        else:
            self.current_percent = int(current_value / maximum_value * 100)
            if self.current_percent > 100:
                self.current_percent = 100

        if self.current_percent == 0:
            image_region = self.active_image\
                .get_region(self.active_image.height // 2,
                            self.active_image.height // 2, 1, 1)
        else:
            image_region = self.active_image\
                .get_region(0, 0, self.current_percent * self.active_image.width // 100,
                            self.active_image.height)

        self.active_sprite.image = image_region

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        self.text_label.on_update_current_locale(self.current_locale)
