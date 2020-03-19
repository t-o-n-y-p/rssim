from logging import getLogger
from operator import itemgetter

from model import *
from database import NARRATOR_QUEUE


class NarratorModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.model'))
        self.narrator_queue = NARRATOR_QUEUE[self.map_id]

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''DELETE FROM narrator WHERE map_id = ?''', (self.map_id, ))
        for announcement in self.narrator_queue:
            USER_DB_CURSOR.execute('''INSERT INTO narrator VALUES (?, ?, ?, ?, ?, ?)''', (self.map_id, *announcement))

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        self.narrator_queue = sorted(self.narrator_queue, key=itemgetter(ANNOUNCEMENT_TIME))
        while len(self.narrator_queue) > 0 and self.game_time >= self.narrator_queue[0][ANNOUNCEMENT_TIME] \
                and (self.narrator_queue[0][ANNOUNCEMENT_LOCKED] or not self.view.is_activated):
            self.narrator_queue.pop(0)

    @final
    def on_dt_multiplier_update(self, dt_multiplier):
        for announcement in [announcement for announcement in self.narrator_queue
                             if announcement[ANNOUNCEMENT_TYPE]
                             in get_announcement_types_diff(self.dt_multiplier, dt_multiplier)]:
            announcement[ANNOUNCEMENT_LOCKED] = int(self.dt_multiplier > dt_multiplier)

        super().on_dt_multiplier_update(dt_multiplier)

    @final
    def on_announcement_add(self, announcement_time, announcement_type, train_id, track_number):
        NARRATOR_QUEUE[self.map_id].append(
            (
                announcement_time, not(announcement_type in get_announcement_types_enabled(self.dt_multiplier)),
                announcement_type, train_id, track_number
            )
        )
