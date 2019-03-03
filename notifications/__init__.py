from win32api import GetModuleHandle
from win32con import CW_USEDEFAULT, IMAGE_ICON, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_USER, \
    WS_OVERLAPPED, WS_SYSMENU
from win32gui import CreateWindow, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, \
    NIM_MODIFY, RegisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

from i18n import I18N_RESOURCES


_wnd_class = WNDCLASS()
_wnd_class.hInstance = GetModuleHandle(None)
_wnd_class.lpszClassName = 'Railway_Station_Simulator'
_wnd_class.lpfnWndProc = {}
_wnd_class_instance = RegisterClass(_wnd_class)
_icon_path = 'icon.ico'


class Notification:
    """
    Implements base class system notification which is displayed if triggered by some in-game event.
    """
    def __init__(self, logger):
        """
        Properties:
            logger                              telemetry instance
            caption_key                         i18n resource key for system notification caption
            message_key                         i18n resource key for system notification message

        :param logger:                          telemetry instance
        """
        self.logger = logger
        self.caption_key = None
        self.message_key = None

    def send(self, current_locale, caption_args=(), message_args=()):
        """
        Creates system notification with predefined caption and message using appropriate locale
        if app window is not active.

        :param current_locale:                  currently selected locale
        :param caption_args:                    arguments for caption string in case they are required
        :param message_args:                    arguments for message string in case they are required
        """
        handler = CreateWindow(_wnd_class_instance, "Taskbar", WS_OVERLAPPED | WS_SYSMENU,
                               0, 0, CW_USEDEFAULT, CW_USEDEFAULT,
                               0, 0, _wnd_class.hInstance, None)
        UpdateWindow(handler)
        icon_handler = LoadImage(_wnd_class.hInstance, _icon_path, IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE)
        Shell_NotifyIcon(NIM_ADD, (handler, 0, NIF_ICON | NIF_MESSAGE | NIF_TIP, WM_USER + 20, icon_handler,
                                   I18N_RESOURCES['game_title_string'][current_locale]))
        Shell_NotifyIcon(NIM_MODIFY, (handler, 0, NIF_INFO, WM_USER + 20,
                                      icon_handler, I18N_RESOURCES['game_title_string'][current_locale],
                                      I18N_RESOURCES[self.message_key][current_locale].format(*message_args), 200,
                                      I18N_RESOURCES[self.caption_key][current_locale].format(*caption_args)))
