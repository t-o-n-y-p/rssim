from typing import final

from ui import default_object
from ui.constructor_placeholder_container_v2 import ConstructorPlaceholderContainerV2
from ui.label_v2.no_more_tracks_available_label_v2 import NoMoreTracksAvailableLabelV2


@final
class TrackPlaceholderContainerV2(ConstructorPlaceholderContainerV2):
    @default_object(NoMoreTracksAvailableLabelV2)
    def __init__(self, logger, parent_viewport, bottom_parent_viewport, top_parent_viewport):
        super().__init__(logger, parent_viewport, bottom_parent_viewport, top_parent_viewport)

    def on_update_top_parent_viewport(self, top_parent_viewport):
        super().on_update_top_parent_viewport(top_parent_viewport)
        self.no_more_tracks_available_label_v2.on_position_update()                                             # noqa
