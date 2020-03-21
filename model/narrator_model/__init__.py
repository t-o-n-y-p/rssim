from logging import getLogger
from operator import itemgetter

from model import *
from database import NARRATOR_QUEUE


class NarratorModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.model'))

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''DELETE FROM narrator WHERE map_id = ?''', (self.map_id, ))
        for announcement in NARRATOR_QUEUE[self.map_id]:
            USER_DB_CURSOR.execute('''INSERT INTO narrator VALUES (?, ?, ?, ?, ?, ?)''', (self.map_id, *announcement))

    @final
    def on_update_time(self, dt):
        NARRATOR_QUEUE[self.map_id] = sorted(NARRATOR_QUEUE[self.map_id], key=itemgetter(ANNOUNCEMENT_TIME))
        # self.logger.debug(f'{self.game_time + int(self.game_time_fraction + dt * self.dt_multiplier)=}')
        # self.logger.debug(f'{NARRATOR_QUEUE[self.map_id]=}')
        while len(NARRATOR_QUEUE[self.map_id]) > 0 \
                and self.game_time + int(self.game_time_fraction + dt * self.dt_multiplier) \
                >= NARRATOR_QUEUE[self.map_id][0][ANNOUNCEMENT_TIME] \
                and NARRATOR_QUEUE[self.map_id][0][ANNOUNCEMENT_LOCKED]:
            NARRATOR_QUEUE[self.map_id].pop(0)

        super().on_update_time(dt)

    @final
    def on_dt_multiplier_update(self, dt_multiplier):
        print(f'{self.dt_multiplier=}, {dt_multiplier=}')
        print([announcement for announcement in NARRATOR_QUEUE[self.map_id]
               if announcement[ANNOUNCEMENT_TYPE] in get_announcement_types_diff(self.dt_multiplier, dt_multiplier)])
        for announcement in [announcement for announcement in NARRATOR_QUEUE[self.map_id]
                             if announcement[ANNOUNCEMENT_TYPE]
                             in get_announcement_types_diff(self.dt_multiplier, dt_multiplier)]:
            announcement[ANNOUNCEMENT_LOCKED] = int(self.dt_multiplier < dt_multiplier)

        print([announcement for announcement in NARRATOR_QUEUE[self.map_id]
               if announcement[ANNOUNCEMENT_TYPE] in get_announcement_types_diff(self.dt_multiplier, dt_multiplier)])

        super().on_dt_multiplier_update(dt_multiplier)

    @final
    def on_announcement_add(self, announcement_time, announcement_type, train_id, track_number):
        NARRATOR_QUEUE[self.map_id].append(
            [
                announcement_time, int(
                    not(announcement_type in get_announcement_types_enabled(self.dt_multiplier)
                        and self.view.is_activated)
                ),
                announcement_type, train_id, track_number
            ]
        )
