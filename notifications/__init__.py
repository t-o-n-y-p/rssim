from typing import final

from win32api import GetModuleHandle
from win32con import CW_USEDEFAULT, IMAGE_ICON, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_USER, \
    WS_OVERLAPPED, WS_SYSMENU
from win32gui import CreateWindow, DestroyWindow, LoadImage, NIF_ICON, NIF_INFO, NIF_MESSAGE, NIF_TIP, NIM_ADD, \
    NIM_MODIFY, NIM_DELETE, RegisterClass, Shell_NotifyIcon, UpdateWindow, WNDCLASS

from i18n import I18N_RESOURCES


_wnd_class = WNDCLASS()
_wnd_class.hInstance = GetModuleHandle(None)
_wnd_class.lpszClassName = 'Railway Station Simulator'
_wnd_class.lpfnWndProc = {}
_wnd_class_instance = RegisterClass(_wnd_class)


class Notification:
    def __init__(self, logger):
        self.logger = logger
        self.caption_key = None
        self.message_key = None
        self.handler = None
        self.icon_handler = LoadImage(_wnd_class.hInstance, 'icon.ico', IMAGE_ICON, 0, 0,
                                      LR_LOADFROMFILE | LR_DEFAULTSIZE)

    @final
    def send(self, current_locale, caption_args=(), message_args=()):
        self.handler = CreateWindow(_wnd_class_instance, "Taskbar", WS_OVERLAPPED | WS_SYSMENU,
                                    0, 0, CW_USEDEFAULT, CW_USEDEFAULT,
                                    0, 0, _wnd_class.hInstance, None)
        UpdateWindow(self.handler)
        Shell_NotifyIcon(NIM_ADD, (self.handler, 0, NIF_ICON | NIF_MESSAGE | NIF_TIP, WM_USER + 20, self.icon_handler,
                                   'Railway Station Simulator'))
        Shell_NotifyIcon(NIM_MODIFY, (self.handler, 0, NIF_INFO, WM_USER + 20,
                                      self.icon_handler, 'Railway Station Simulator',
                                      I18N_RESOURCES[self.message_key][current_locale].format(*message_args), 200,
                                      I18N_RESOURCES[self.caption_key][current_locale].format(*caption_args)))

    @final
    def destroy(self):
        Shell_NotifyIcon(NIM_DELETE, (self.handler, 0, NIF_ICON | NIF_MESSAGE | NIF_TIP, WM_USER + 20,
                                      self.icon_handler))
        DestroyWindow(self.handler)
