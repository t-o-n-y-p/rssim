from logging import getLogger

from ui import *
from ui.constructor_placeholder_container import ConstructorPlaceholderContainer
from ui.label.no_more_tracks_available_label import NoMoreTracksAvailableLabel


@final
class ConstructorTrackPlaceholderContainer(ConstructorPlaceholderContainer):
    def __init__(self, bottom_parent_viewport, top_parent_viewport):
        super().__init__(bottom_parent_viewport, top_parent_viewport,
                         logger=getLogger('root.constructor_track_placeholder_container'))
        self.placeholder_label = NoMoreTracksAvailableLabel(parent_viewport=self.viewport)
        self.on_window_resize_handlers.append(self.placeholder_label.on_window_resize)
