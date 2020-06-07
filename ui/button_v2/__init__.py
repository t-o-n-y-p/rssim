from abc import ABC, abstractmethod
from typing import Final, final

from pyglet import gl
from pyglet.text import Label
from pyglet.window import mouse

from ui import GROUPS, WHITE_RGB, GREY_RGB, WINDOW, HAND_CURSOR, DEFAULT_CURSOR, window_size_has_changed, BATCHES, \
    MAP_CAMERA, PRESSED, NORMAL, HOVER, UIObject, is_not_active, is_active


def is_active_or_disabled(f):
    def _handle_if_is_active_or_disabled(*args, **kwargs):
        if args[0].is_activated or args[0].disabled_state:
            f(*args, **kwargs)

    return _handle_if_is_active_or_disabled


def left_mouse_button(f):
    def _handle_mouse_if_left_button_was_clicked(*args, **kwargs):
        if args[3] == mouse.LEFT:
            f(*args, **kwargs)

    return _handle_mouse_if_left_button_was_clicked


def cursor_is_over_the_button(f):
    def _handle_if_cursor_is_over_the_button(*args, **kwargs):
        if isinstance(args[0], MapButtonV2):
            if args[1] in range(int((args[0].x * MAP_CAMERA.zoom + 2) - MAP_CAMERA.offset_x),
                                int((args[0].x * MAP_CAMERA.zoom + args[0].width - 2) - MAP_CAMERA.offset_x)) \
                    and args[2] in range(int((args[0].y * MAP_CAMERA.zoom + 2) - MAP_CAMERA.offset_y),
                                         int((args[0].y * MAP_CAMERA.zoom + args[0].height - 2) - MAP_CAMERA.offset_y)):
                f(*args, **kwargs)
        else:
            if args[1] in range(args[0].x + 2, args[0].x + args[0].width - 2) \
                    and args[2] in range(args[0].y + 2, args[0].y + args[0].height - 2):
                f(*args, **kwargs)

    return _handle_if_cursor_is_over_the_button


def button_is_pressed(f):
    def _handle_if_button_is_pressed(*args, **kwargs):
        if args[0].state == PRESSED:
            f(*args, **kwargs)

    return _handle_if_button_is_pressed


# button background RGB color for non-transparent and transparent button
BUTTON_BACKGROUND_RGB: Final = {
    NORMAL: ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    HOVER: ((0.375, 0.0, 0.0), (0.5, 0.0, 0.0)),
    PRESSED: ((0.5625, 0.0, 0.0), (0.75, 0.0, 0.0))
}
# button background alpha for non-transparent and transparent button
BUTTON_BACKGROUND_ALPHA: Final = {
    NORMAL: (1.0, 0.0),
    HOVER: (1.0, 0.75),
    PRESSED: (1.0, 0.75)
}


class ButtonV2(UIObject, ABC):
    def __init__(self, logger, parent_viewport, on_click_action, on_hover_action, on_leave_action):
        super().__init__(logger, parent_viewport)
        self.on_click_action = on_click_action
        self.on_hover_action = on_hover_action
        self.on_leave_action = on_leave_action
        self.state = NORMAL
        self.on_mouse_press_handlers = [self.on_mouse_press]
        self.on_mouse_release_handlers = [self.on_mouse_release]
        self.on_mouse_motion_handlers = [self.on_mouse_motion]
        self.on_mouse_leave_handlers = [self.on_mouse_leave]
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    @abstractmethod
    def get_width(self):
        pass

    @abstractmethod
    def get_height(self):
        pass

    @abstractmethod
    def on_mouse_motion(self, x, y, dx, dy):
        pass

    @abstractmethod
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    @abstractmethod
    def on_mouse_release(self, x, y, button, modifiers):
        pass

    @abstractmethod
    def on_mouse_leave(self, x, y):
        pass


class UIButtonV2(ButtonV2, ABC):
    def __init__(self, logger, parent_viewport, on_click_action, on_hover_action, on_leave_action):
        super().__init__(logger, parent_viewport, on_click_action, on_hover_action, on_leave_action)
        self.transparent = True
        self.paired_button = None
        self.vertex_list = None
        self.text_label = None
        self.font_name = 'Webdings'
        self.is_bold = False
        self.disabled_state = False
        self.arguments = []

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
        self.disabled_state = False
        # gl.glEnable(gl.GL_BLEND)
        # gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        if not self.vertex_list:
            self.vertex_list = BATCHES['ui_batch'].add(
                20, gl.GL_QUADS, GROUPS['button_background'],
                ('v2i', self._get_vertices()),
                ('c4f', self._get_main_colors() + ((1.0, 0.0, 0.0, self.opacity / 255) * 16))
            )

        if not self.text_label:
            if (text := self.get_formatted_text()) not in (None, ''):
                self.text_label = Label(
                    text, font_name=self.font_name, bold=self.is_bold,
                    font_size=self.get_font_size(), color=(*WHITE_RGB, self.opacity),
                    x=self.x + self.width // 2, y=self.y + self.height // 2,
                    anchor_x='center', anchor_y='center', batch=BATCHES['ui_batch'], group=GROUPS['button_text']
                )
        else:
            self.text_label.color = (*WHITE_RGB, self.opacity)

    @final
    @is_active_or_disabled
    def on_deactivate(self):
        self.is_activated = False
        self.disabled_state = False

    @final
    def on_disable(self):
        self.on_deactivate()
        self.disabled_state = True
        if self.vertex_list:
            self.vertex_list.delete()
            self.vertex_list = None

        if not self.text_label:
            if (text := self.get_formatted_text()) not in (None, ''):
                self.text_label = Label(
                    text, font_name=self.font_name, bold=self.is_bold,
                    font_size=self.get_font_size(), color=(*GREY_RGB, self.opacity),
                    x=self.x + self.width // 2, y=self.y + self.height // 2,
                    anchor_x='center', anchor_y='center', batch=BATCHES['ui_batch'], group=GROUPS['button_text']
                )
        else:
            self.text_label.color = (*GREY_RGB, self.opacity)

    @final
    @is_active
    def on_mouse_motion(self, x, y, dx, dy):
        # if cursor is on the button and button is not pressed, it means cursor was just moved over the button,
        # state and background color are changed to "hover" state
        if x in range(self.x + 2, self.x + self.width - 2) and y in range(self.y + 2, self.y + self.height - 2):
            if self.state not in (PRESSED, HOVER):
                self.state = HOVER
                if self.vertex_list:
                    self.vertex_list.colors[:16] = self._get_main_colors()

                WINDOW.set_mouse_cursor(HAND_CURSOR)
                if self.on_hover_action:
                    self.on_hover_action()
        # if cursor is not on the button and button is not normal, it means cursor has just left the button,
        # state and background color are changed to "normal" state
        else:
            if self.state != NORMAL:
                self.state = NORMAL
                if self.vertex_list:
                    self.vertex_list.colors[:16] = self._get_main_colors()

                WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
                if self.on_leave_action:
                    self.on_leave_action()

    @final
    @is_active
    @cursor_is_over_the_button
    @left_mouse_button
    def on_mouse_press(self, x, y, button, modifiers):
        self.state = PRESSED
        if self.vertex_list:
            self.vertex_list.colors[:16] = self._get_main_colors()

    @final
    @is_active
    @cursor_is_over_the_button
    @button_is_pressed
    @left_mouse_button
    def on_mouse_release(self, x, y, button, modifiers):
        self.state = HOVER
        if self.vertex_list:
            self.vertex_list.colors[:16] = self._get_main_colors()

        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
        self.on_click_action(self)

    @final
    @is_active
    def on_mouse_leave(self, x, y):
        self.state = NORMAL
        if self.vertex_list:
            self.vertex_list.colors[:16] = self._get_main_colors()

        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
        if self.on_leave_action:
            self.on_leave_action()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        if self.opacity <= 0:
            if self.vertex_list:
                self.vertex_list.delete()
                self.vertex_list = None

            if self.text_label:
                self.text_label.delete()
                self.text_label = None

        else:
            if self.vertex_list:
                self.vertex_list.colors[3:16:4] = (
                    (BUTTON_BACKGROUND_ALPHA[self.state][int(self.transparent)] * float(self.opacity) / 255.0,) * 4
                )
                self.vertex_list.colors[19::4] = ((self.opacity / 255, ) * 16)

            if self.text_label:
                self.text_label.color = (*self.text_label.color[:3], self.opacity)

    @final
    def _get_vertices(self):
        return (
            # inside
            self.x + 2, self.y + 2,
            self.x + self.width - 2, self.y + 2,
            self.x + self.width - 2, self.y + self.height - 2,
            self.x + 2, self.y + self.height - 2,
            # left border
            self.x, self.y, self.x + 2, self.y,
            self.x + 2, self.y + self.height, self.x, self.y + self.height,
            # right border
            self.x + self.width - 2, self.y, self.x + self.width, self.y,
            self.x + self.width, self.y + self.height, self.x + self.width - 2, self.y + self.height,
            # bottom border
            self.x + 2, self.y, self.x + self.width - 2, self.y,
            self.x + self.width - 2, self.y + 2, self.x + 2, self.y + 2,
            # top border
            self.x + 2, self.y + self.height - 2, self.x + self.width - 2, self.y + self.height - 2,
            self.x + self.width - 2, self.y + self.height, self.x + 2, self.y + self.height
        )

    @final
    def _get_main_colors(self):
        return (
            (
                *BUTTON_BACKGROUND_RGB[self.state][int(self.transparent)],
                BUTTON_BACKGROUND_ALPHA[self.state][int(self.transparent)] * float(self.opacity) / 255.0
            ) * 4
        )

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.width = self.get_width()
        self.height = self.get_height()
        self.x = self.get_x()
        self.y = self.get_y()
        if self.vertex_list:
            self.vertex_list.vertices = self._get_vertices()

        if self.text_label:
            self.text_label.begin_update()
            self.text_label.x = self.x + self.width // 2
            self.text_label.y = self.y + self.height // 2
            self.text_label.font_size = self.get_font_size()
            self.text_label.end_update()

    @final
    @is_active
    def on_position_changed(self):
        self.x = self.get_x()
        self.y = self.get_y()
        if self.vertex_list:
            self.vertex_list.vertices = self._get_vertices()

        if self.text_label:
            self.text_label.begin_update()
            self.text_label.x = self.x + self.width // 2
            self.text_label.y = self.y + self.height // 2
            self.text_label.end_update()


class MapButtonV2(ButtonV2, ABC):
    @final
    @is_active
    def on_mouse_motion(self, x, y, dx, dy):
        # if cursor is on the button and button is not pressed, it means cursor was just moved over the button,
        # state and background color are changed to "hover" state
        if x in range(int((self.x * MAP_CAMERA.zoom + 2) - MAP_CAMERA.offset_x),
                      int((self.x * MAP_CAMERA.zoom + self.width - 2) - MAP_CAMERA.offset_x)) \
                and y in range(int((self.y * MAP_CAMERA.zoom + 2) - MAP_CAMERA.offset_y),
                               int((self.y * MAP_CAMERA.zoom + self.height - 2) - MAP_CAMERA.offset_y)):
            if self.state not in (PRESSED, HOVER):
                self.state = HOVER
                WINDOW.set_mouse_cursor(HAND_CURSOR)
                self.on_hover_action()
        # if cursor is not on the button and button is not normal, it means cursor has just left the button,
        # state and background color are changed to "normal" state
        else:
            if self.state != NORMAL:
                self.state = NORMAL
                WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
                self.on_leave_action()

    @final
    @is_active
    @cursor_is_over_the_button
    @left_mouse_button
    def on_mouse_press(self, x, y, button, modifiers):
        self.state = PRESSED

    @final
    @is_active
    @cursor_is_over_the_button
    @button_is_pressed
    @left_mouse_button
    def on_mouse_release(self, x, y, button, modifiers):
        self.state = HOVER
        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
        self.on_click_action(self)

    @final
    @is_active
    def on_mouse_leave(self, x, y):
        self.state = NORMAL
        WINDOW.set_mouse_cursor(DEFAULT_CURSOR)
        self.on_leave_action()

    @final
    def on_change_scale(self):
        self.width = self.get_width()
        self.height = self.get_height()
