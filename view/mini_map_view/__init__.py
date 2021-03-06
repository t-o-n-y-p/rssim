from abc import ABC
from logging import getLogger
from math import ceil
from typing import final

from database import USER_DB_CURSOR
from ui import get_mini_map_width, MAP_CAMERA, MAP_WIDTH, get_mini_map_height, MAP_HEIGHT, get_top_bar_height, \
    get_bottom_bar_height, get_mini_map_position

from ui.sprite.mini_map_sprite import MiniMapSprite
from ui.sprite.mini_environment_sprite import MiniEnvironmentSprite
from ui.shader_sprite.mini_map_view_shader_sprite import MiniMapViewShaderSprite
from view import MapBaseView, view_is_not_active


class MiniMapView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.mini_map.view'))
        USER_DB_CURSOR.execute('''SELECT unlocked_tracks FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.unlocked_tracks = USER_DB_CURSOR.fetchone()[0]
        self.mini_map_sprite = MiniMapSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.mini_environment_sprite = MiniEnvironmentSprite(map_id=self.map_id, parent_viewport=self.viewport)
        self.shader_sprite = MiniMapViewShaderSprite(view=self)
        self.on_window_resize_handlers.extend(
            [
                self.shader_sprite.on_window_resize, self.mini_map_sprite.on_window_resize,
                self.mini_environment_sprite.on_window_resize
            ]
        )
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        self.shader_sprite.create()
        self.mini_map_sprite.create()
        self.mini_environment_sprite.create()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.shader_sprite.on_update_opacity(self.opacity)
        self.mini_map_sprite.on_update_opacity(self.opacity)
        self.mini_environment_sprite.on_update_opacity(self.opacity)

    @final
    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        self.mini_map_sprite.on_unlock_track(self.unlocked_tracks)

    @final
    def on_unlock_environment(self, tier):
        self.mini_environment_sprite.on_unlock_environment(tier)

    @final
    def get_mini_map_frame_position(self):
        return (
            ceil(MAP_CAMERA.position[0] / MAP_WIDTH * get_mini_map_width(self.screen_resolution) / MAP_CAMERA.zoom)
            + get_mini_map_position(self.screen_resolution)[0],
            ceil(
                (get_bottom_bar_height(self.screen_resolution) + MAP_CAMERA.position[1]) / MAP_HEIGHT
                * get_mini_map_height(self.screen_resolution) / MAP_CAMERA.zoom
            ) + get_mini_map_position(self.screen_resolution)[1]
        )

    @final
    def get_mini_map_frame_height(self):
        return int(
            (
                self.viewport.y2 - self.viewport.y1 - get_bottom_bar_height(self.screen_resolution)
                - get_top_bar_height(self.screen_resolution)
            ) / (MAP_HEIGHT * MAP_CAMERA.zoom) * get_mini_map_height(self.screen_resolution)
        )

    @final
    def get_mini_map_frame_width(self):
        return int(
            (self.viewport.x2 - self.viewport.x1) / (MAP_WIDTH * MAP_CAMERA.zoom)
            * get_mini_map_width(self.screen_resolution)
        )
