from abc import ABC
from typing import final

from ui import window_size_has_changed, UIObject, localizable, default_object, optional_object, get_inner_area_viewport
from ui.button_v2.next_page_button_v2 import NextPageButtonV2
from ui.button_v2.previous_page_button_v2 import PreviousPageButtonV2
from ui.label_v2.page_control_counter_label_v2 import PageControlCounterLabelV2


class PageControlV2(UIObject, ABC):
    @localizable
    @default_object(PageControlCounterLabelV2)
    @default_object(NextPageButtonV2)
    @optional_object(PreviousPageButtonV2)
    def __init__(self, logger, parent_viewport):
        super().__init__(logger, parent_viewport)
        self.pages = []
        self.current_page = 0

    @final
    def on_activate(self):
        super().on_activate()
        self.current_page = 0
        self.page_control_counter_label_v2.begin_update()                                                       # noqa
        self.page_control_counter_label_v2.on_current_page_update(self.current_page + 1)                        # noqa
        self.page_control_counter_label_v2.on_total_pages_update(len(self.pages))                               # noqa
        self.page_control_counter_label_v2.end_update()                                                         # noqa

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        super().on_window_resize(width, height)
        self.viewport = get_inner_area_viewport(self.screen_resolution)

    @final
    def on_click_action_next_page_button_v2(self):
        self.pages[self.current_page].fade_out_animation.on_activate()
        self.pages[self.current_page + 1].fade_in_animation.on_activate()
        self.current_page += 1
        self.page_control_counter_label_v2.on_current_page_update(self.current_page + 1)                        # noqa
        if self.current_page == len(self.pages) - 1:
            self.next_page_button_v2.fade_out_animation.on_activate()                                           # noqa
        elif self.current_page == 1:
            self.previous_page_button_v2.fade_in_animation.on_activate()                                        # noqa

    @final
    def on_click_action_previous_page_button_v2(self):
        self.pages[self.current_page].fade_out_animation.on_activate()
        self.pages[self.current_page - 1].fade_in_animation.on_activate()
        self.current_page -= 1
        self.page_control_counter_label_v2.on_current_page_update(self.current_page + 1)                        # noqa
        if self.current_page == 0:
            self.previous_page_button_v2.fade_out_animation.on_activate()                                       # noqa
        elif self.current_page == len(self.pages) - 2:
            self.next_page_button_v2.fade_in_animation.on_activate()                                            # noqa
