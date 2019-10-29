from logging import getLogger

from view import *
from ui.button.close_map_switcher_button import CloseMapSwitcherButton
from ui.label.map_switcher_title_label import MapSwitcherTitleLabel
from ui.shader_sprite.map_switcher_view_shader_sprite import MapSwitcherViewShaderSprite


class MapSwitcherView(GameBaseView):
    def __init__(self, controller):
        def on_close_map_switcher(button):
            self.controller.fade_out_animation.on_activate()

        super().__init__(controller, logger=getLogger(f'root.app.game.map_switcher.view'), child_window=True)
        self.shader_sprite = MapSwitcherViewShaderSprite(view=self)
        self.title_label = MapSwitcherTitleLabel(parent_viewport=self.viewport)
        self.close_map_switcher_button = CloseMapSwitcherButton(on_click_action=on_close_map_switcher,
                                                                parent_viewport=self.viewport)
        self.buttons = [self.close_map_switcher_button, ]

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.title_label.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_update_current_locale(self, new_locale):
        super().on_update_current_locale(new_locale)
        self.title_label.on_update_current_locale(self.current_locale)

    @final
    def on_change_screen_resolution(self, screen_resolution):
        super().on_change_screen_resolution(screen_resolution)
        self.shader_sprite.on_change_screen_resolution(self.screen_resolution)
        self.title_label.on_change_screen_resolution(self.screen_resolution)
        for b in self.buttons:
            b.on_change_screen_resolution(self.screen_resolution)

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.title_label.on_update_opacity(self.opacity)
