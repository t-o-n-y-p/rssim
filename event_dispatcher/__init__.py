from ctypes import windll
from typing import final, Final

from pyglet.window.win32 import Win32Window

from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, on_commit


@final
class Window(Win32Window):
    MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME: Final = 1
    MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME: Final = 1
    MAXIMUM_MOUSE_SCROLL_EVENTS_PER_FRAME: Final = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_mouse_press_handlers = []
        self.on_mouse_release_handlers = []
        self.on_mouse_motion_handlers = []
        self.on_mouse_drag_handlers = []
        self.on_mouse_leave_handlers = []
        self.on_mouse_scroll_handlers = []
        self.on_key_press_handlers = []
        self.on_text_handlers = []
        self.on_window_resize_handlers = []
        self.on_window_activate_handlers = []
        self.on_window_show_handlers = []
        self.on_window_deactivate_handlers = []
        self.on_window_hide_handlers = []
        self.on_mouse_motion_event_counter = 0
        self.on_mouse_motion_cached_movement = [0, 0]
        self.on_mouse_drag_event_counter = 0
        self.on_mouse_drag_cached_movement = [0, 0]
        self.on_mouse_scroll_event_counter = 0
        self.on_mouse_scroll_cached_movement = [0, 0]
        self.fullscreen_resolution = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
        USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
        self.windowed_resolution = USER_DB_CURSOR.fetchone()

    @staticmethod
    def on_fullscreen():
        WINDOW.set_size(*WINDOW.fullscreen_resolution)
        WINDOW.set_fullscreen(fullscreen=True)
        USER_DB_CURSOR.execute('UPDATE graphics SET fullscreen = 1')
        on_commit()

    @staticmethod
    def on_restore():
        WINDOW.set_fullscreen(fullscreen=False)
        WINDOW.set_size(*WINDOW.windowed_resolution)
        USER_DB_CURSOR.execute('UPDATE graphics SET fullscreen = 0')
        on_commit()


Window.register_event_type('on_fullscreen')
Window.register_event_type('on_restore')


def _create_window():
    CONFIG_DB_CURSOR.execute('SELECT app_width, app_height FROM screen_resolution_config')
    screen_resolution_config = CONFIG_DB_CURSOR.fetchall()
    monitor_resolution_config = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    USER_DB_CURSOR.execute('SELECT fullscreen FROM graphics')
    if bool(USER_DB_CURSOR.fetchone()[0]) and monitor_resolution_config in screen_resolution_config:
        window = Window(width=monitor_resolution_config[0], height=monitor_resolution_config[1],
                        caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)
        window.set_fullscreen(True)
        return window

    USER_DB_CURSOR.execute('SELECT app_width, app_height FROM graphics')
    screen_resolution = USER_DB_CURSOR.fetchone()
    return Window(width=screen_resolution[0], height=screen_resolution[1],
                  caption='Railway Station Simulator', style='borderless', fullscreen=False, vsync=False)


WINDOW: Final = _create_window()
# flip the surface so user knows game has launched and is loading now
WINDOW.flip()


@WINDOW.event
def on_activate():
    for h in WINDOW.on_window_activate_handlers:
        h()


@WINDOW.event
def on_show():
    for h in WINDOW.on_window_show_handlers:
        h()


@WINDOW.event
def on_deactivate():
    for h in WINDOW.on_window_deactivate_handlers:
        h()


@WINDOW.event
def on_hide():
    for h in WINDOW.on_window_hide_handlers:
        h()


@WINDOW.event
def on_mouse_press(x, y, button, modifiers):
    for h in WINDOW.on_mouse_press_handlers:
        h(x, y, button, modifiers)


@WINDOW.event
def on_mouse_release(x, y, button, modifiers):
    for h in WINDOW.on_mouse_release_handlers:
        h(x, y, button, modifiers)


@WINDOW.event
def on_mouse_motion(x, y, dx, dy):
    if WINDOW.on_mouse_motion_event_counter < WINDOW.MAXIMUM_MOUSE_MOTION_EVENTS_PER_FRAME:
        WINDOW.on_mouse_motion_event_counter += 1
        dx += WINDOW.on_mouse_motion_cached_movement[0]
        dy += WINDOW.on_mouse_motion_cached_movement[1]
        WINDOW.on_mouse_motion_cached_movement = [0, 0]
        for h in WINDOW.on_mouse_motion_handlers:
            h(x, y, dx, dy)

    else:
        WINDOW.on_mouse_motion_cached_movement[0] += dx
        WINDOW.on_mouse_motion_cached_movement[1] += dy


@WINDOW.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    if WINDOW.on_mouse_drag_event_counter < WINDOW.MAXIMUM_MOUSE_DRAG_EVENTS_PER_FRAME:
        WINDOW.on_mouse_drag_event_counter += 1
        dx += WINDOW.on_mouse_drag_cached_movement[0]
        dy += WINDOW.on_mouse_drag_cached_movement[1]
        WINDOW.on_mouse_drag_cached_movement = [0, 0]
        for h in WINDOW.on_mouse_drag_handlers:
            h(x, y, dx, dy, buttons, modifiers)

    else:
        WINDOW.on_mouse_drag_cached_movement[0] += dx
        WINDOW.on_mouse_drag_cached_movement[1] += dy


@WINDOW.event
def on_mouse_leave(x, y):
    for h in WINDOW.on_mouse_leave_handlers:
        h(x, y)


@WINDOW.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if WINDOW.on_mouse_scroll_event_counter < WINDOW.MAXIMUM_MOUSE_SCROLL_EVENTS_PER_FRAME:
        WINDOW.on_mouse_scroll_event_counter += 1
        scroll_x += WINDOW.on_mouse_scroll_cached_movement[0]
        scroll_y += WINDOW.on_mouse_scroll_cached_movement[1]
        WINDOW.on_mouse_scroll_cached_movement = [0, 0]
        for h in WINDOW.on_mouse_scroll_handlers:
            h(x, y, scroll_x, scroll_y)

    else:
        WINDOW.on_mouse_scroll_cached_movement[0] += scroll_x
        WINDOW.on_mouse_scroll_cached_movement[1] += scroll_y


@WINDOW.event
def on_key_press(symbol, modifiers):
    for h in WINDOW.on_key_press_handlers:
        h(symbol, modifiers)


@WINDOW.event
def on_text(text):
    for h in WINDOW.on_text_handlers:
        h(text)


@WINDOW.event
def on_resize(width, height):
    for h in WINDOW.on_window_resize_handlers:
        h(width, height)
