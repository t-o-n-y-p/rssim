from abc import ABC, abstractmethod
from typing import final

from pyglet.text import Label as PygletLabel
from win32clipboard import OpenClipboard, CloseClipboard, GetClipboardData
from pyglet.window.key import BACKSPACE, V, MOD_CTRL

from i18n import I18N_RESOURCES
from database import USER_DB_CURSOR
from ui import WHITE_RGB, GREY_RGB


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


def interactive_label_does_not_exist(fn):
    def _handle_if_interactive_label_does_not_exist(*args, **kwargs):
        if args[0].text_label is None and args[0].placeholder_label is None:
            fn(*args, **kwargs)

    return _handle_if_interactive_label_does_not_exist


def interactive_label_exists(fn):
    def _handle_if_interactive_label_exists(*args, **kwargs):
        if args[0].text_label is not None or args[0].placeholder_label is not None:
            fn(*args, **kwargs)

    return _handle_if_interactive_label_exists


def arguments_have_changed(fn):
    def _update_label_if_args_have_changed(*args, **kwargs):
        if len(kwargs) > 0:
            if args[0].arguments != kwargs['new_args']:
                fn(*args, **kwargs)
        else:
            if args[0].arguments != args[1]:
                fn(*args, **kwargs)

    return _update_label_if_args_have_changed


class Label(ABC):
    def __init__(self, logger, parent_viewport):
        self.logger = logger
        self.parent_viewport = parent_viewport
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
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = None
        self.group = None
        self.screen_resolution = (1280, 720)

    @abstractmethod
    def get_x(self):
        pass

    @abstractmethod
    def get_y(self):
        pass

    @abstractmethod
    def get_font_size(self):
        pass

    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_formatted_text(self):
        pass

    @final
    @text_label_does_not_exist
    def create(self):
        self.text_label = PygletLabel(self.get_formatted_text(), font_name=self.font_name, bold=self.bold,
                                      font_size=self.font_size, color=(*self.base_color, self.opacity),
                                      x=self.x, y=self.y, width=self.width,
                                      anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align,
                                      multiline=self.multiline, batch=self.batch, group=self.group)

    @final
    @text_label_exists
    def delete(self):
        self.text_label.delete()
        self.text_label = None

    @final
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

    @final
    def on_position_changed(self):
        self.x = self.get_x()
        self.y = self.get_y()
        if self.text_label is not None:
            self.text_label.begin_update()
            self.text_label.x = self.x
            self.text_label.y = self.y
            self.text_label.end_update()

    @final
    def on_change_base_color(self, new_base_color):
        self.base_color = new_base_color
        if self.text_label is not None:
            self.text_label.color = (*self.base_color, self.opacity)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.text_label is not None:
            if self.opacity > 0:
                self.text_label.color = (*self.base_color, self.opacity)
            else:
                self.delete()

    @final
    @arguments_have_changed
    def on_update_args(self, new_args):
        self.arguments = new_args
        if self.text_label is not None:
            self.text_label.text = self.get_formatted_text()


class LocalizedLabel(Label, ABC):
    def __init__(self, logger, i18n_resources_key, parent_viewport):
        super().__init__(logger=logger, parent_viewport=parent_viewport)
        self.i18n_resources_key = i18n_resources_key
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.text = I18N_RESOURCES[self.i18n_resources_key][self.current_locale]

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.text = I18N_RESOURCES[self.i18n_resources_key][self.current_locale]
        if self.text_label is not None:
            self.text_label.text = self.get_formatted_text()


class InteractiveLabel(ABC):
    def __init__(self, logger, parent_viewport):
        self.logger = logger
        self.parent_viewport = parent_viewport
        self.arguments = ()
        self.text_label = None
        self.placeholder_label = None
        self.text = ''
        self.placeholder_text_i18n_resources_key = None
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.font_name = 'Arial'
        self.bold = False
        self.font_size = 20
        self.base_color = WHITE_RGB
        self.placeholder_color = GREY_RGB
        self.opacity = 0
        self.x = 0
        self.y = 0
        self.width = None
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = None
        self.group = None
        self.screen_resolution = (1280, 720)
        self.text_length_limit = 25

    @final
    def __len__(self):
        return len(self.text)

    @abstractmethod
    def get_x(self):
        pass

    @abstractmethod
    def get_y(self):
        pass

    @abstractmethod
    def get_font_size(self):
        pass

    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_formatted_placeholder_text(self):
        pass

    @final
    @interactive_label_does_not_exist
    def create(self):
        self.placeholder_label = pyglet.text.Label(self.get_formatted_placeholder_text(),
                                                   font_name=self.font_name, bold=self.bold, font_size=self.font_size,
                                                   color=(*self.placeholder_color, self.opacity),
                                                   x=self.x, y=self.y, width=self.width,
                                                   anchor_x=self.anchor_x, anchor_y=self.anchor_y,
                                                   align=self.align, multiline=self.multiline,
                                                   batch=self.batch, group=self.group)

    @final
    @interactive_label_exists
    def delete(self):
        self.text = ''
        if self.text_label is not None:
            self.text_label.delete()
            self.text_label = None
        else:
            self.placeholder_label.delete()
            self.placeholder_label = None

    @final
    def on_text(self, text):
        if len(self.text) == 0:
            self.placeholder_label.delete()
            self.placeholder_label = None
            self.text = text[:self.text_length_limit]
            self.text_label = pyglet.text.Label(self.text, font_name=self.font_name, bold=self.bold,
                                                font_size=self.font_size, color=(*self.base_color, self.opacity),
                                                x=self.x, y=self.y, width=self.width,
                                                anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align,
                                                multiline=self.multiline, batch=self.batch, group=self.group)
        else:
            self.text = (self.text + text)[:self.text_length_limit]
            self.text_label.text = self.text

    @final
    def on_key_press(self, symbol, modifiers):
        if symbol == BACKSPACE:
            if len(self.text) == 1:
                self.text_label.delete()
                self.text_label = None
                self.text = ''
                self.placeholder_label = pyglet.text.Label(self.get_formatted_placeholder_text(),
                                                           font_name=self.font_name, bold=self.bold,
                                                           font_size=self.font_size,
                                                           color=(*self.placeholder_color, self.opacity),
                                                           x=self.x, y=self.y, width=self.width,
                                                           anchor_x=self.anchor_x, anchor_y=self.anchor_y,
                                                           align=self.align, multiline=self.multiline,
                                                           batch=self.batch, group=self.group)
            elif len(self.text) > 1:
                self.text = self.text[:-1]
                self.text_label.text = self.text

        elif modifiers & MOD_CTRL and symbol == V:
            OpenClipboard()
            try:
                self.on_text(GetClipboardData())
            except TypeError:
                pass

            CloseClipboard()

    @final
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

        if self.placeholder_label is not None:
            self.placeholder_label.begin_update()
            self.placeholder_label.x = self.x
            self.placeholder_label.y = self.y
            self.placeholder_label.font_size = self.font_size
            self.placeholder_label.width = self.width
            self.placeholder_label.end_update()

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.opacity > 0:
            if self.text_label is not None:
                self.text_label.color = (*self.base_color, self.opacity)

            if self.placeholder_label is not None:
                self.placeholder_label.color = (*self.placeholder_color, self.opacity)
        else:
            self.delete()

    @final
    @arguments_have_changed
    def on_update_args(self, new_args):
        self.arguments = new_args
        if self.placeholder_label is not None:
            self.placeholder_label.text = self.get_formatted_placeholder_text()

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        if self.placeholder_label is not None:
            self.placeholder_label.text = self.get_formatted_placeholder_text()
