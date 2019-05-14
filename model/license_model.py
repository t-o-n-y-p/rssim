from logging import getLogger

from model import *


class LicenseModel(Model):
    """
    Implements License model.
    License object is responsible for properties, UI and events related to the license screen.
    """
    def __init__(self):
        super().__init__(logger=getLogger('root.app.license.model'))

    def on_activate_view(self):
        """
        Activates view and refreshes all data.
        """
        self.view.on_activate()
