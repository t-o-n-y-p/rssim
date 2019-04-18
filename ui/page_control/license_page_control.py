from logging import getLogger

from ui.page_control import PageControl
from ui.license_page.pyglet_licence_page import PygletLicensePage
from ui.license_page.pyshaders_license_page import PyshadersLicensePage
from ui.license_page.pywin32_license_page import Pywin32LicensePage
from ui.license_page.cx_freeze_license_page import CxFreezeLicensePage


class LicensePageControl(PageControl):
    def __init__(self, current_locale):
        super().__init__(current_locale, logger=getLogger('root.app.main_menu.license.view.license_page_control'))
        self.pages = [PygletLicensePage(current_locale), PyshadersLicensePage(current_locale),
                      Pywin32LicensePage(current_locale), CxFreezeLicensePage(current_locale)]
        self.on_mouse_scroll_handlers = []
        for p in self.pages:
            self.on_mouse_scroll_handlers.append(p.handle_mouse_scroll)
