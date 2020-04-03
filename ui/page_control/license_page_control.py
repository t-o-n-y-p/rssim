from logging import getLogger
from typing import final

from ui.page_control import PageControl
from ui.license_page.pyglet_licence_page import PygletLicensePage
from ui.license_page.pyshaders_license_page import PyshadersLicensePage
from ui.license_page.pywin32_license_page import Pywin32LicensePage
from ui.license_page.cx_freeze_license_page import CxFreezeLicensePage
from ui.license_page.keyring_license_page import KeyringLicensePage
from ui.license_page.numpy_license_page import NumpyLicensePage


@final
class LicensePageControl(PageControl):
    def __init__(self, parent_viewport):
        super().__init__(
            logger=getLogger('root.app.license.view.license_page_control'), parent_viewport=parent_viewport
        )
        self.pages = [
            PygletLicensePage(parent_viewport=self.viewport),
            PyshadersLicensePage(parent_viewport=self.viewport),
            Pywin32LicensePage(parent_viewport=self.viewport),
            KeyringLicensePage(parent_viewport=self.viewport),
            NumpyLicensePage(parent_viewport=self.viewport),
            CxFreezeLicensePage(parent_viewport=self.viewport)
        ]
        self.on_mouse_scroll_handlers = []
        for p in self.pages:
            self.on_mouse_scroll_handlers.append(p.on_mouse_scroll)
            self.on_window_resize_handlers.extend(p.on_window_resize_handlers)
