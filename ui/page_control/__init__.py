from abc import ABC
from typing import final

from ui import get_inner_area_rect, window_size_has_changed, Viewport
from ui.button.previous_page_button import PreviousPageButton
from ui.button.next_page_button import NextPageButton
from ui.label.page_control_counter_label import PageControlCounterLabel
from database import USER_DB_CURSOR


def shader_sprite_exists(fn):
    def _handle_if_shader_sprite_exists(*args, **kwargs):
        if args[0].shader_sprite is not None:
            fn(*args, **kwargs)

    return _handle_if_shader_sprite_exists


class PageControl(ABC):
    def __init__(self, logger, parent_viewport):
        def on_navigate_to_previous_page(button):
            self.pages[self.current_page - 1].on_update_opacity(self.pages[self.current_page].opacity)
            self.pages[self.current_page].on_deactivate(instant=True)
            self.current_page -= 1
            self.pages[self.current_page].on_activate()
            self.current_page_label.on_update_args((self.current_page + 1, len(self.pages)))
            self.on_update_page_control_buttons()

        def on_navigate_to_next_page(button):
            self.pages[self.current_page + 1].on_update_opacity(self.pages[self.current_page].opacity)
            self.pages[self.current_page].on_deactivate(instant=True)
            self.current_page += 1
            self.pages[self.current_page].on_activate()
            self.current_page_label.on_update_args((self.current_page + 1, len(self.pages)))
            self.on_update_page_control_buttons()

        self.is_activated = False
        self.logger = logger
        self.parent_viewport = parent_viewport
        self.viewport = Viewport()
        self.screen_resolution = (0, 0)
        USER_DB_CURSOR.execute('SELECT current_locale FROM i18n')
        self.current_locale = USER_DB_CURSOR.fetchone()[0]
        self.pages = []
        self.current_page = 0
        self.current_page_label = PageControlCounterLabel(parent_viewport=self.viewport)
        self.previous_page_button = PreviousPageButton(
            on_click_action=on_navigate_to_previous_page, parent_viewport=self.viewport
        )
        self.next_page_button = NextPageButton(
            on_click_action=on_navigate_to_next_page, parent_viewport=self.viewport
        )
        self.buttons = [self.previous_page_button, self.next_page_button]
        self.shader_sprite = None
        self.opacity = 0
        self.on_window_resize_handlers = [self.on_window_resize, self.current_page_label.on_window_resize]

    @final
    def on_activate(self):
        self.is_activated = True
        self.current_page = 0
        if self.shader_sprite is not None:
            self.shader_sprite.create()

        self.current_page_label.on_update_args((self.current_page + 1, len(self.pages)))
        self.current_page_label.create()
        self.pages[self.current_page].on_activate()
        self.next_page_button.on_activate()

    @final
    def on_deactivate(self):
        self.is_activated = False
        self.pages[self.current_page].on_deactivate()
        for b in self.buttons:
            b.on_deactivate()

    @final
    @window_size_has_changed
    def on_window_resize(self, width, height):
        self.screen_resolution = width, height
        self.viewport.x1, self.viewport.y1 = get_inner_area_rect(self.screen_resolution)[0:2]
        self.viewport.x2 = self.viewport.x1 + get_inner_area_rect(self.screen_resolution)[2]
        self.viewport.y2 = self.viewport.y1 + get_inner_area_rect(self.screen_resolution)[3]

    @final
    def on_update_page_control_buttons(self):
        if self.current_page == 0:
            self.previous_page_button.on_deactivate(instant=True)
            self.previous_page_button.state = 'normal'
        else:
            self.previous_page_button.on_activate(instant=True)

        if self.current_page == len(self.pages) - 1:
            self.next_page_button.on_deactivate(instant=True)
            self.next_page_button.state = 'normal'
        else:
            self.next_page_button.on_activate(instant=True)

    @final
    def on_update_current_locale(self, new_locale):
        self.current_locale = new_locale
        self.current_page_label.on_update_current_locale(self.current_locale)
        for p in self.pages:
            p.on_update_current_locale(self.current_locale)

    @final
    def on_update_opacity(self, new_opacity):
        self.opacity = new_opacity
        if self.shader_sprite is not None:
            self.shader_sprite.on_update_opacity(self.opacity)

        self.current_page_label.on_update_opacity(self.opacity)
        self.pages[self.current_page].on_update_opacity(self.opacity)

    def on_apply_shaders_and_draw_vertices(self):
        pass
