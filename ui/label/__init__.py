import pyglet.text

from i18n import I18N_RESOURCES
from database import USER_DB_CURSOR
from ui import WHITE_RGB


def text_label_does_not_exist(fn):
    def _create_text_label_if_it_does_not_exist(*args, **kwargs):
        if args[0].text_label is None:
            fn(*args, **kwargs)

    return _create_text_label_if_it_does_not_exist


def text_label_exists(fn):
    def _delete_text_label_if_it_exists(*args, **kwargs):
        if args[0].text_label is not None:
            fn(*args, **kwargs)

    return _delete_text_label_if_it_exists


class Label:
    def __init__(self, logger, args=()):
        self.logger = logger
        self.args = args
        self.text_label = None
        self.text = 'Default text'
        self.font_name = 'Arial'
        self.bold = False
        self.font_size = 20
        self.base_color = WHITE_RGB
        self.opacity = 0
        self.x = 0
        self.y = 0
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.batch = None
        self.group = None

    @staticmethod
    def get_x(screen_resolution):
        pass

    @staticmethod
    def get_y(screen_resolution):
        pass

    @staticmethod
    def get_font_size(screen_resolution):
        pass

    @text_label_does_not_exist
    def create(self):
        self.text_label = pyglet.text.Label(self.text.format(*self.args), font_name=self.font_name, bold=self.bold,
                                            font_size=self.font_size, color=(*self.base_color, self.opacity),
                                            x=self.x, y=self.y, anchor_x=self.anchor_x, anchor_y=self.anchor_y,
                                            batch=self.batch, group=self.group)

    @text_label_exists
    def delete(self):
        self.text_label.delete()
        self.text_label = None

    def on_change_screen_resolution(self, screen_resolution):
        self.x = self.get_x(screen_resolution)
        self.y = self.get_y(screen_resolution)
        self.font_size = self.get_font_size(screen_resolution)
        if self.text_label is not None:
            self.text_label.begin_update()
            self.text_label.x = self.x
            self.text_label.y = self.y
            self.text_label.font_size = self.font_size
            self.text_label.end_update()

    def on_change_base_color(self, new_base_color):
        self.base_color = new_base_color
        if self.text_label is not None:
            self.text_label.color = (*self.base_color, self.opacity)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.text_label is not None:
            self.text_label.color = (*self.base_color, self.opacity)

    def on_update_args(self, new_args):
        self.args = new_args
        if self.text_label is not None:
            self.text_label.text = self.text.format(*self.args)


class LocalizedLabel(Label):
    def __init__(self, logger, i18n_resources_key, args=()):
        super().__init__(logger=logger, args=args)
        self.i18n_resources_key = i18n_resources_key
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.text = I18N_RESOURCES[self.i18n_resources_key][USER_DB_CURSOR.fetchone()[0]]

    def on_update_current_locale(self, new_locale):
        self.text = I18N_RESOURCES[self.i18n_resources_key][new_locale]
        if self.text_label is not None:
            self.text_label.text = self.text.format(*self.args)
