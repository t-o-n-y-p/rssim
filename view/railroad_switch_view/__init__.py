from logging import getLogger

from view import *
from textures import SWITCHES_STRAIGHT, SWITCHES_DIVERGING
from ui.sprite.railroad_switch_sprite import RailroadSwitchSprite


class RailroadSwitchView(MapBaseView):
    def __init__(self, controller, map_id, track_param_1, track_param_2, switch_type):
        super().__init__(controller, map_id, logger=getLogger(
                f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.view'
            )
        )
        CONFIG_DB_CURSOR.execute('''SELECT region_x, region_y, region_w, region_h FROM switches_config
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                    AND map_id = ?''',
                                 (track_param_1, track_param_2, switch_type, self.map_id))
        self.switch_region = CONFIG_DB_CURSOR.fetchone()
        USER_DB_CURSOR.execute('''SELECT current_position FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, switch_type, self.map_id))
        self.current_position = USER_DB_CURSOR.fetchone()[0]
        self.images = {track_param_1: SWITCHES_STRAIGHT.get_region(*self.switch_region),
                       track_param_2: SWITCHES_DIVERGING.get_region(*self.switch_region)}
        USER_DB_CURSOR.execute('''SELECT locked FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? 
                                  AND map_id = ?''',
                               (track_param_1, track_param_2, switch_type, self.map_id))
        self.locked = bool(USER_DB_CURSOR.fetchone()[0])
        self.sprite = RailroadSwitchSprite(map_id, track_param_1, track_param_2, switch_type,
                                           parent_viewport=self.viewport)
        self.sprite.on_update_texture(self.images[self.current_position])

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
    def on_update(self):
        if self.sprite.is_located_outside_viewport():
            self.sprite.delete()
        elif not self.locked:
            self.sprite.create()

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        self.sprite.on_update_opacity(self.opacity)

    @final
    def on_change_current_position(self, current_position):
        self.current_position = current_position
        self.sprite.on_update_texture(self.images[self.current_position])
