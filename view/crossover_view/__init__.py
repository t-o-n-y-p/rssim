from logging import getLogger

from view import *
from textures import SWITCHES_STRAIGHT, SWITCHES_DIVERGING
from ui.sprite.crossover_sprite import CrossoverSprite


class CrossoverView(MapBaseView):
    def __init__(self, controller, map_id, track_param_1, track_param_2, crossover_type):
        super().__init__(controller, logger=getLogger(
                f'root.app.game.map.{map_id}.crossover.{track_param_1}.{track_param_2}.{crossover_type}.view'
            )
        )
        self.map_id = map_id
        CONFIG_DB_CURSOR.execute('''SELECT region_x, region_y, region_w, region_h FROM crossovers_config
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                    AND map_id = ?''',
                                 (track_param_1, track_param_2, crossover_type, self.map_id))
        self.crossover_region = CONFIG_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT current_position_1, current_position_2 FROM crossovers 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, crossover_type, self.map_id))
        self.current_position_1, self.current_position_2 = USER_DB_CURSOR.fetchone()
        self.images = {track_param_1:
                           {track_param_1: SWITCHES_STRAIGHT.get_region(*self.crossover_region),
                            track_param_2: SWITCHES_DIVERGING.get_region(*self.crossover_region)},
                       track_param_2:
                           {track_param_1: SWITCHES_DIVERGING.get_region(*self.crossover_region),
                            track_param_2: SWITCHES_STRAIGHT.get_region(*self.crossover_region)}
                       }
        USER_DB_CURSOR.execute('''SELECT locked FROM crossovers 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND crossover_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, crossover_type, self.map_id))
        self.locked = bool(USER_DB_CURSOR.fetchone()[0])
        self.sprite = CrossoverSprite(map_id, track_param_1, track_param_2, crossover_type,
                                      parent_viewport=self.viewport)
        self.sprite.on_update_texture(self.images[self.current_position_1][self.current_position_2])

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        if not self.sprite.is_located_outside_viewport() and not self.locked:
            self.sprite.create()

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.sprite.on_update_opacity(self.opacity)

    @final
    def on_change_base_offset(self, new_base_offset):
        super().on_change_base_offset(new_base_offset)
        self.sprite.on_change_base_offset(self.base_offset)
        if self.sprite.is_located_outside_viewport():
            self.sprite.delete()
        elif not self.locked:
            self.sprite.create()

    @final
    def on_change_scale(self, zoom_factor):
        super().on_change_scale(zoom_factor)
        self.sprite.on_change_scale(self.zoom_factor)

    @final
    def on_change_current_position(self, current_position_1, current_position_2):
        self.current_position_1 = current_position_1
        self.current_position_2 = current_position_2
        self.sprite.on_update_texture(self.images[self.current_position_1][self.current_position_2])
