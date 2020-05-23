from abc import ABC, abstractmethod
from typing import final

from pyglet.text import Label as PygletLabel

from ui import UIObject, WHITE_RGB, is_not_active, window_size_has_changed, GREY_RGB


def arguments_have_changed(fn):
    def _update_label_if_args_have_changed(*args, **kwargs):
        if len(kwargs) > 0:
            if args[0].arguments != kwargs['new_args']:
                fn(*args, **kwargs)
        else:
            if args[0].arguments != args[1]:
                fn(*args, **kwargs)

    return _update_label_if_args_have_changed


class LabelV2(UIObject, ABC):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.arguments = ()
        self.text_label = None
        self.font_name = 'Arial'
        self.bold = False
        self.font_size = 20
        self.base_color = WHITE_RGB
        self.x = 0
        self.y = 0
        self.width = None
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = None
        self.group = None

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
    @is_not_active
    def on_activate(self):
        super().on_activate()
        self.text_label = PygletLabel(
            self.get_formatted_text(), font_name=self.font_name, bold=self.bold, font_size=self.font_size,
            color=(*self.base_color, self.opacity), x=self.x, y=self.y, width=self.width,
            anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align, multiline=self.multiline,
            batch=self.batch, group=self.group
        )

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        if self.text_label:
            if self.opacity > 0:
                self.text_label.color = (*self.base_color, self.opacity)
            else:
                self.text_label.delete()
                self.text_label = None

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.x = self.get_x()
        self.y = self.get_y()
        self.font_size = self.get_font_size()
        self.width = self.get_width()
        if self.text_label:
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
        if self.text_label:
            self.text_label.begin_update()
            self.text_label.x = self.x
            self.text_label.y = self.y
            self.text_label.end_update()

    @final
    def on_change_base_color(self, new_base_color):
        self.base_color = new_base_color
        if self.text_label:
            self.text_label.color = (*self.base_color, self.opacity)

    @final
    @arguments_have_changed
    def on_update_args(self, new_args):
        self.arguments = new_args
        if self.text_label:
            self.text_label.text = self.get_formatted_text()


class InteractiveLabelV2(UIObject, ABC):
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.arguments = ()
        self.text_label = None
        self.placeholder_label = None
        self.font_name = 'Arial'
        self.bold = False
        self.font_size = 20
        self.base_color = WHITE_RGB
        self.placeholder_color = GREY_RGB
        self.x = 0
        self.y = 0
        self.width = None
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = None
        self.group = None
        self.text_length_limit = 25

    @final
    def __len__(self):
        return len(self.text_label.text) if self.text_label else 0

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
    @is_not_active
    def on_activate(self):
        super().on_activate()
        self.placeholder_label = PygletLabel(
            self.get_formatted_text(), font_name=self.font_name, bold=self.bold, font_size=self.font_size,
            color=(*self.placeholder_color, self.opacity), x=self.x, y=self.y, width=self.width,
            anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align, multiline=self.multiline,
            batch=self.batch, group=self.group
        )

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        if self.text_label:
            if self.opacity > 0:
                self.text_label.color = (*self.base_color, self.opacity)
            else:
                self.text_label.delete()
                self.text_label = None

        if self.placeholder_label:
            if self.opacity > 0:
                self.placeholder_label.color = (*self.placeholder_color, self.opacity)
            else:
                self.placeholder_label.delete()
                self.placeholder_label = None

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.x = self.get_x()
        self.y = self.get_y()
        self.font_size = self.get_font_size()
        self.width = self.get_width()
        if self.text_label:
            self.text_label.begin_update()
            self.text_label.x = self.x
            self.text_label.y = self.y
            self.text_label.font_size = self.font_size
            self.text_label.width = self.width
            self.text_label.end_update()

        if self.placeholder_label:
            self.placeholder_label.begin_update()
            self.placeholder_label.x = self.x
            self.placeholder_label.y = self.y
            self.placeholder_label.font_size = self.font_size
            self.placeholder_label.width = self.width
            self.placeholder_label.end_update()

    @final
    @arguments_have_changed
    def on_update_args(self, new_args):
        self.arguments = new_args
        if self.text_label is not None:
            self.text_label.text = self.get_formatted_text()
