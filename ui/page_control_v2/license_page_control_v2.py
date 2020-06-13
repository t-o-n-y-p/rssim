from typing import final

from ui import default_object, optional_object
from ui.license_page_v2.cx_freeze_license_page_v2 import CxFreezeLicensePageV2
from ui.license_page_v2.keyring_license_page_v2 import KeyringLicensePageV2
from ui.license_page_v2.numpy_license_page_v2 import NumpyLicensePageV2
from ui.license_page_v2.pyglet_licence_page_v2 import PygletLicensePageV2
from ui.license_page_v2.pyshaders_license_page_v2 import PyshadersLicensePageV2
from ui.license_page_v2.pywin32_license_page_v2 import Pywin32LicensePageV2
from ui.page_control_v2 import PageControlV2


@final
class LicensePageControlV2(PageControlV2):
    @default_object(PygletLicensePageV2)
    @optional_object(PyshadersLicensePageV2)
    @optional_object(Pywin32LicensePageV2)
    @optional_object(KeyringLicensePageV2)
    @optional_object(NumpyLicensePageV2)
    @optional_object(CxFreezeLicensePageV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
