from logging import getLogger
from typing import final

from ui.constructor_placeholder_container import ConstructorPlaceholderContainer
from ui.label.no_more_environment_available_label import NoMoreEnvironmentAvailableLabel


@final
class ConstructorEnvironmentPlaceholderContainer(ConstructorPlaceholderContainer):
    def __init__(self, bottom_parent_viewport, top_parent_viewport):
        super().__init__(
            bottom_parent_viewport, top_parent_viewport,
            logger=getLogger('root.constructor_environment_placeholder_container')
        )
        self.placeholder_label = NoMoreEnvironmentAvailableLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.placeholder_label.on_window_resize)
