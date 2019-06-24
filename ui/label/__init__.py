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


def arguments_have_changed(fn):
    def _update_label_if_args_have_changed(*args, **kwargs):
        if len(kwargs) > 0:
            if args[0].arguments != kwargs['new_args']:
                fn(*args, **kwargs)
        else:
            if args[0].arguments != args[1]:
                fn(*args, **kwargs)

    return _update_label_if_args_have_changed


class Label:
    def __init__(self, logger, parent_viewport):
        self.logger = logger
        self.arguments = ()
        self.text_label = None
        self.text = 'Default text'
        self.font_name = 'Arial'
        self.bold = False
        self.font_size = 20
        self.base_color = WHITE_RGB
        self.opacity = 0
        self.x = 0
        self.y = 0
        self.width = None
        self.parent_viewport = parent_viewport
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = None
        self.group = None
        self.screen_resolution = (1280, 720)

    def get_x(self):
        pass

    def get_y(self):
        pass

    def get_font_size(self):
        pass

    def get_width(self):
        pass

    def get_formatted_text(self):
        pass

    @text_label_does_not_exist
    def create(self):
        self.text_label = pyglet.text.Label(self.get_formatted_text(), font_name=self.font_name, bold=self.bold,
                                            font_size=self.font_size, color=(*self.base_color, self.opacity),
                                            x=self.x, y=self.y, width=self.width,
                                            anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align,
                                            multiline=self.multiline, batch=self.batch, group=self.group)

    @text_label_exists
    def delete(self):
        self.text_label.delete()
        self.text_label = None

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.x = self.get_x()
        self.y = self.get_y()
        self.font_size = self.get_font_size()
        self.width = self.get_width()
        if self.text_label is not None:
            self.text_label.begin_update()
            self.text_label.x = self.x
            self.text_label.y = self.y
            self.text_label.font_size = self.font_size
            self.text_label.width = self.width
            self.text_label.end_update()

    def on_position_changed(self):
        self.x = self.get_x()
        self.y = self.get_y()
        if self.text_label is not None:
            self.text_label.begin_update()
            self.text_label.x = self.x
            self.text_label.y = self.y
            self.text_label.end_update()

    def on_change_base_color(self, new_base_color):
        self.base_color = new_base_color
        if self.text_label is not None:
            self.text_label.color = (*self.base_color, self.opacity)

    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.text_label is not None:
            self.text_label.color = (*self.base_color, self.opacity)

    @arguments_have_changed
    def on_update_args(self, new_args):
        self.arguments = new_args
        if self.text_label is not None:
            self.text_label.text = self.get_formatted_text()


class LocalizedLabel(Label):
    def __init__(self, logger, i18n_resources_key, parent_viewport):
        super().__init__(logger=logger, parent_viewport=parent_viewport)
        self.i18n_resources_key = i18n_resources_key
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.text = I18N_RESOURCES[self.i18n_resources_key][self.current_locale]

    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.text = I18N_RESOURCES[self.i18n_resources_key][self.current_locale]
        if self.text_label is not None:
            self.text_label.text = self.get_formatted_text()
