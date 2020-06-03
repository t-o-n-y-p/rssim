from logging import getLogger
from typing import final

from database import CONFIG_DB_CURSOR, USER_DB_CURSOR
from ui import RED_SIGNAL_IMAGE, GREEN_SIGNAL_IMAGE, GREEN_SIGNAL, GROUPS, BATCHES, WHITE_SIGNAL_IMAGE, WHITE_SIGNAL

from ui.sprite_v2 import MapSpriteV2


@final
class SignalSpriteV2(MapSpriteV2):
    def __init__(self, map_id, track, base_route, parent_viewport):
        super().__init__(
            map_id, logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.sprite'),
            parent_viewport=parent_viewport
        )
        CONFIG_DB_CURSOR.execute(
            '''SELECT x, y, rotation FROM signal_config WHERE track = ? AND base_route = ? AND map_id = ?''',
            (track, base_route, self.map_id)
        )
        self.x, self.y, self.rotation = CONFIG_DB_CURSOR.fetchone()
        self.batch = BATCHES['main_batch']
        self.group = GROUPS['signal']
        USER_DB_CURSOR.execute(
            '''SELECT state FROM signals WHERE track = ? AND base_route = ? AND map_id = ?''',
            (track, base_route, self.map_id)
        )
        self.texture = RED_SIGNAL_IMAGE
        if (state := USER_DB_CURSOR.fetchone()[0]) == GREEN_SIGNAL:
            self.texture = GREEN_SIGNAL_IMAGE
        elif state == WHITE_SIGNAL:
            self.texture = WHITE_SIGNAL_IMAGE

    def on_change_state(self, state):
        if state == GREEN_SIGNAL:
            self.on_update_texture(GREEN_SIGNAL_IMAGE)
        elif state == WHITE_SIGNAL:
            self.on_update_texture(WHITE_SIGNAL_IMAGE)
        else:
            self.on_update_texture(RED_SIGNAL_IMAGE)
