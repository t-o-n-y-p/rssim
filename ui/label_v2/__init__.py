from inspect import getfullargspec
from abc import ABC, abstractmethod
from math import log10
from typing import final

from pyglet.text import Label as PygletLabel
from pyglet.window.key import MOD_CTRL, BACKSPACE, V
from win32clipboard import CloseClipboard, GetClipboardData, OpenClipboard

from database import MINUTES_IN_ONE_HOUR, SECONDS_IN_ONE_HOUR, HOURS_IN_ONE_DAY, SECONDS_IN_ONE_MINUTE
from i18n import I18N_RESOURCES
from ui import UIObject, is_not_active, window_size_has_changed, localizable, is_active, BATCHES, GROUPS


def _create_label(cls, parent_object):
    label_name_snake_case = ''.join('_' + c.lower() if c.isupper() else c for c in cls.__name__).lstrip('_')
    cls_resource_keys = getfullargspec(cls).args[3:]
    parent_object.__setattr__(
        label_name_snake_case,
        cls(
            parent_object.logger.getChild(label_name_snake_case), parent_object.parent_viewport,
            *(parent_object.__getattribute__(a) for a in cls_resource_keys)
        )
    )
    label_object = parent_object.__getattribute__(label_name_snake_case)
    parent_object.ui_objects.append(label_object)
    parent_object.fade_out_animation.child_animations.append(label_object.fade_out_animation)
    parent_object.on_window_resize_handlers.extend(label_object.on_window_resize_handlers)
    if issubclass(cls, InteractiveLabelV2):
        parent_object.on_key_press_handlers.extend(label_object.on_key_press_handlers)
        parent_object.on_text_handlers.extend(label_object.on_text_handlers)

    return label_object


def default_label(cls):
    def _default_label(f):
        def _add_default_label(*args, **kwargs):
            f(*args, **kwargs)
            if issubclass(cls, (LabelV2, InteractiveLabelV2)):
                label_object = _create_label(cls, args[0])
                args[0].fade_in_animation.child_animations.append(label_object.fade_in_animation)

        return _add_default_label

    return _default_label


def label(cls):
    def _label(f):
        def _add_label(*args, **kwargs):
            f(*args, **kwargs)
            if issubclass(cls, (LabelV2, InteractiveLabelV2)):
                _create_label(cls, args[0])

        return _add_label

    return _label


def argument(name):
    def _argument(f):
        def _add_argument(*args, **kwargs):
            def on_argument_update(value):
                if value != args[0].arguments[args[0].__getattribute__(f'{name}_index')]:
                    args[0].arguments[args[0].__getattribute__(f'{name}_index')] = value
                    if args[0].text_label:
                        args[0].text_label.text = args[0].get_formatted_text()

            def on_argument_update_24h_time(value):
                if (value // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR \
                        != args[0].arguments[args[0].__getattribute__(f'{name}_index') + 1]:
                    args[0].arguments[args[0].__getattribute__(f'{name}_index')] \
                        = (value // SECONDS_IN_ONE_HOUR + 12) % HOURS_IN_ONE_DAY
                    args[0].arguments[args[0].__getattribute__(f'{name}_index') + 1] \
                        = (value // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR
                    if args[0].text_label:
                        args[0].text_label.text = args[0].get_formatted_text()

            def on_argument_update_12h_time(value):
                if (value // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR \
                        != args[0].arguments[args[0].__getattribute__(f'{name}_index') + 1]:
                    args[0].arguments[args[0].__getattribute__(f'{name}_index')] \
                        = (value // SECONDS_IN_ONE_HOUR + 11) % 12 + 1
                    args[0].arguments[args[0].__getattribute__(f'{name}_index') + 1] \
                        = (value // SECONDS_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR
                    args[0].arguments[args[0].__getattribute__(f'{name}_index') + 2] \
                        = I18N_RESOURCES['am_pm_string'][args[0].current_locale][
                            ((value // SECONDS_IN_ONE_HOUR) // 12 + 1) % 2
                        ]
                    if args[0].text_label:
                        args[0].text_label.text = args[0].get_formatted_text()

            def on_argument_update_price(value):
                if '{0:,}'.format(value).replace(',', ' ') \
                        != args[0].arguments[args[0].__getattribute__(f'{name}_index')]:
                    args[0].arguments[args[0].__getattribute__(f'{name}_index')] \
                        = '{0:,}'.format(value).replace(',', ' ')
                    if args[0].text_label:
                        args[0].text_label.text = args[0].get_formatted_text()

            def on_argument_update_screen_resolution(value):
                if list(value) != args[0].arguments[
                            args[0].__getattribute__(f'{name}_index')
                            :args[0].__getattribute__(f'{name}_index') + 2
                        ]:
                    args[0].arguments[
                        args[0].__getattribute__(f'{name}_index')
                        :args[0].__getattribute__(f'{name}_index') + 2
                    ] = list(value)
                    if args[0].text_label:
                        args[0].text_label.text = args[0].get_formatted_text()

            f(*args, **kwargs)
            shift_value = 3 if name.find('12h') >= 0 \
                else 2 if name.find('24h') >= 0 or name.find('resolution') >= 0 \
                else 1
            for a in [a for a in dir(args[0]) if a.endswith('_index')]:
                args[0].__setattr__(a, args[0].__getattribute__(a) + shift_value)

            args[0].__setattr__(f'{name}_index', 0)
            if name.find('price') >= 0 or name.find('storage') >= 0:
                args[0].__setattr__(f'on_{name}_update', on_argument_update_price)
            elif name.find('12h') >= 0:
                args[0].__setattr__(f'on_{name}_update', on_argument_update_12h_time)
            elif name.find('24h') >= 0:
                args[0].__setattr__(f'on_{name}_update', on_argument_update_24h_time)
            elif name.find('resolution') >= 0:
                args[0].__setattr__(f'on_{name}_update', on_argument_update_screen_resolution)
            else:
                args[0].__setattr__(f'on_{name}_update', on_argument_update)

            args[0].arguments = [None for i in range(shift_value)] + args[0].arguments

        return _add_argument

    return _argument


class LabelV2(UIObject, ABC):
    font_name: str
    base_color: (int, int, int)

    def __init__(self, logger, parent_viewport, *resource_list_keys):
        super().__init__(logger, parent_viewport)
        self.arguments = []
        self.resource_list_keys = resource_list_keys
        self.text_label = None
        self.bold = False
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']

    @abstractmethod
    def get_x(self):
        pass

    @abstractmethod
    def get_y(self):
        pass

    @abstractmethod
    def get_font_size(self):
        pass

    def get_width(self):
        return None

    @abstractmethod
    def get_formatted_text(self):
        pass

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.text_label:
            self.text_label = PygletLabel(
                self.get_formatted_text(), font_name=self.font_name, bold=self.bold, font_size=self.get_font_size(),
                color=(*self.base_color, self.opacity), x=self.get_x(), y=self.get_y(), width=self.get_width(),
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
        if self.text_label:
            self.text_label.begin_update()
            self.text_label.x = self.get_x()
            self.text_label.y = self.get_y()
            self.text_label.font_size = self.get_font_size()
            self.text_label.width = self.get_width()
            self.text_label.end_update()

    @final
    @is_active
    def on_position_changed(self):
        self.text_label.begin_update()
        self.text_label.x = self.get_x()
        self.text_label.y = self.get_y()
        self.text_label.end_update()


class InteractiveLabelV2(UIObject, ABC):
    font_name: str
    base_color: (int, int, int)
    placeholder_color: (int, int, int)

    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.arguments = []
        self.text_label = None
        self.placeholder_label = None
        self.bold = False
        self.anchor_x = 'center'
        self.anchor_y = 'center'
        self.align = 'left'
        self.multiline = False
        self.batch = BATCHES['ui_batch']
        self.group = GROUPS['button_text']
        self.text_length_limit = 25
        self.on_key_press_handlers = [self.on_key_press]
        self.on_text_handlers = [self.on_text]

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
    def get_formatted_text(self):
        pass

    @final
    @is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.placeholder_label:
            self.placeholder_label = PygletLabel(
                self.get_formatted_text(), font_name=self.font_name, bold=self.bold, font_size=self.get_font_size(),
                color=(*self.placeholder_color, self.opacity), x=self.get_x(), y=self.get_y(),
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
        if self.text_label:
            self.text_label.begin_update()
            self.text_label.x = self.get_x()
            self.text_label.y = self.get_y()
            self.text_label.font_size = self.get_font_size()
            self.text_label.end_update()

        if self.placeholder_label:
            self.placeholder_label.begin_update()
            self.placeholder_label.x = self.get_x()
            self.placeholder_label.y = self.get_y()
            self.placeholder_label.font_size = self.get_font_size()
            self.placeholder_label.end_update()

    @final
    def on_text(self, text):
        if not self.text_label:
            self.placeholder_label.delete()
            self.placeholder_label = None
            self.text_label = PygletLabel(
                text[:self.text_length_limit], font_name=self.font_name, bold=self.bold, font_size=self.get_font_size(),
                color=(*self.base_color, self.opacity), x=self.get_x(), y=self.get_y(),
                anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align, multiline=self.multiline,
                batch=self.batch, group=self.group
            )
        else:
            self.text_label.text = (self.text_label.text + text)[:self.text_length_limit]

    @final
    def on_key_press(self, symbol, modifiers):
        if symbol == BACKSPACE and self.text_label:
            if len(self.text_label.text) > 0:
                self.text_label.text = self.text_label.text[:-1]
            else:
                self.text_label.delete()
                self.text_label = None
                self.placeholder_label = PygletLabel(
                    self.get_formatted_text(), font_name=self.font_name, bold=self.bold, font_size=self.get_font_size(),
                    color=(*self.placeholder_color, self.opacity), x=self.get_x(), y=self.get_y(),
                    anchor_x=self.anchor_x, anchor_y=self.anchor_y, align=self.align,
                    multiline=self.multiline, batch=self.batch, group=self.group
                )

        elif modifiers & MOD_CTRL and symbol == V:
            OpenClipboard()
            try:
                self.on_text(GetClipboardData())
            except TypeError:
                pass

            CloseClipboard()


class MultiplierLabelV2(LabelV2, ABC):
    @localizable
    def __init__(self, logger, parent_viewport, max_precision):
        super().__init__(logger, parent_viewport)
        self.max_precision = max_precision
        self.arguments = [0, 1]

    @final
    def on_multiplier_update(self, new_value):
        if new_value >= 10 ** self.max_precision:
            self.arguments = [None, int(new_value)]
        else:
            module = 10 ** (self.max_precision - int(log10(new_value)))
            fractional_part_format = f'{{0:0>{self.max_precision - int(log10(new_value))}}}'
            self.arguments = [
                fractional_part_format.format(round(new_value * module) % module),
                round(new_value * module) // module
            ]

        if self.text_label:
            self.text_label.text = self.get_formatted_text()

    @final
    def get_formatted_text(self):
        return f'x{int(self.arguments[1])}' if self.arguments[0] is None \
            else I18N_RESOURCES['multiplier_value_string'][self.current_locale].format(*self.arguments)         # noqa
