from logging import getLogger

from ui.page_control import PageControl
from ui.license_page.pyglet_licence_page import PygletLicensePage
from ui.license_page.pyshaders_license_page import PyshadersLicensePage
from ui.license_page.pywin32_license_page import Pywin32LicensePage
from ui.license_page.cx_freeze_license_page import CxFreezeLicensePage


class LicensePageControl(PageControl):
    """
    Implements page control for license screen.
    """
    def __init__(self):
        """
        Properties:
            on_mouse_scroll_handlers            list of on_mouse_scroll handlers from license pages

        """
        super().__init__(logger=getLogger('root.app.main_menu.license.view.license_page_control'))
        self.pages = [PygletLicensePage(), PyshadersLicensePage(), Pywin32LicensePage(), CxFreezeLicensePage()]
        self.on_mouse_scroll_handlers = []
        for p in self.pages:
            self.on_mouse_scroll_handlers.append(p.handle_mouse_scroll)
