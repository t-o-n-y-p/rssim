from random import choice, seed
from logging import getLogger

from model import *
from textures import MAXIMUM_CAR_COLLECTIONS
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR, on_commit


class MapModel(MapBaseModel, ABC):
    def __init__(self, controller, view, map_id):
        super().__init__(controller, view, map_id, logger=getLogger(f'root.app.game.map.{map_id}.model'))
        USER_DB_CURSOR.execute('''SELECT locked, unlocked_tracks, unlocked_environment 
                                  FROM map_progress WHERE map_id = ?''', (self.map_id, ))
        self.locked, self.unlocked_tracks, self.unlocked_environment = USER_DB_CURSOR.fetchone()
        self.locked = bool(self.locked)
        USER_DB_CURSOR.execute('''SELECT unlocked_car_collections FROM map_progress WHERE map_id = ?''',
                               (self.map_id, ))
        self.unlocked_car_collections = [int(c) for c in USER_DB_CURSOR.fetchone()[0].split(',')]
        USER_DB_CURSOR.execute('''SELECT last_known_base_offset FROM map_position_settings WHERE map_id = ?''',
                               (self.map_id, ))
        self.last_known_base_offset = [int(p) for p in USER_DB_CURSOR.fetchone()[0].split(',')]
        USER_DB_CURSOR.execute('''SELECT last_known_zoom FROM map_position_settings WHERE map_id = ?''',
                               (self.map_id, ))
        self.last_known_zoom = USER_DB_CURSOR.fetchone()[0]
        CONFIG_DB_CURSOR.execute('''SELECT unlocked_tracks_by_default FROM map_progress_config WHERE map_id = ?''',
                                 (self.map_id, ))
        self.unlocked_tracks_by_default = CONFIG_DB_CURSOR.fetchone()[0]

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE map_progress SET locked = ?, unlocked_tracks = ?, unlocked_environment = ?, 
                                  unlocked_car_collections = ? WHERE map_id = ?''',
                               (int(self.locked), self.unlocked_tracks, self.unlocked_environment,
                                ','.join(str(c) for c in self.unlocked_car_collections), self.map_id))

    @final
    def on_unlock_track(self, track):
        self.unlocked_tracks = track
        if self.unlocked_tracks in CAR_COLLECTION_UNLOCK_TRACK_LIST[self.map_id]:
            self.on_add_new_car_collection()

        self.view.on_unlock_track(track)
        self.view.on_unlock_construction()

    @final
    def on_unlock_environment(self, tier):
        self.unlocked_environment = tier
        self.view.on_unlock_environment(tier)
        self.view.on_unlock_construction()

    @final
    def on_save_and_commit_last_known_base_offset(self):
        self.last_known_base_offset = self.view.base_offset
        USER_DB_CURSOR.execute('''UPDATE map_position_settings SET last_known_base_offset = ? WHERE map_id = ?''',
                               (','.join(str(p) for p in self.last_known_base_offset), self.map_id))
        on_commit()

    @final
    def on_save_and_commit_last_known_zoom(self):
        self.last_known_zoom = self.view.zoom
        USER_DB_CURSOR.execute('''UPDATE map_position_settings SET last_known_zoom = ? WHERE map_id = ?''',
                               (self.last_known_zoom, self.map_id))
        on_commit()

    @final
    def on_clear_trains_info(self):
        USER_DB_CURSOR.execute('''DELETE FROM trains WHERE map_id = ?''', (self.map_id, ))

    def on_create_train(self, train_id, cars, track, train_route, state, direction, new_direction,
                        current_direction, priority, boarding_time, exp, money, switch_direction_required):
        pass

    @final
    def on_add_new_car_collection(self):
        all_collections_set = set(range(MAXIMUM_CAR_COLLECTIONS[self.map_id]))
        available_car_collections = list(all_collections_set.difference(set(self.unlocked_car_collections)))
        if len(available_car_collections) > 0:
            seed()
            selected_collection = choice(available_car_collections)
            self.unlocked_car_collections.append(selected_collection)

    @final
    def get_signals_to_unlock_with_track(self, track):
        CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config 
                                    WHERE track_unlocked_with = ? AND environment_unlocked_with <= ? AND map_id = ?''',
                                 (track, self.unlocked_environment, self.map_id))
        return CONFIG_DB_CURSOR.fetchall()

    @final
    def get_switches_to_unlock_with_track(self, track):
        CONFIG_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches_config 
                                    WHERE track_unlocked_with = ? AND environment_unlocked_with <= ? AND map_id = ?''',
                                 (track, self.unlocked_environment, self.map_id))
        return CONFIG_DB_CURSOR.fetchall()

    @final
    def get_crossovers_to_unlock_with_track(self, track):
        CONFIG_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, crossover_type FROM crossovers_config 
                                    WHERE track_unlocked_with = ? AND environment_unlocked_with <= ? AND map_id = ?''',
                                 (track, self.unlocked_environment, self.map_id))
        return CONFIG_DB_CURSOR.fetchall()

    @final
    def get_shops_to_unlock_with_track(self, track):
        CONFIG_DB_CURSOR.execute('''SELECT shop_id FROM shops_config WHERE map_id = ? AND track_required = ?''',
                                 (self.map_id, track))
        return CONFIG_DB_CURSOR.fetchall()

    @final
    def get_signals_to_unlock_with_environment(self, tier):
        CONFIG_DB_CURSOR.execute('''SELECT track, base_route FROM signal_config 
                                    WHERE track_unlocked_with <= ? AND environment_unlocked_with = ? AND map_id = ?''',
                                 (self.unlocked_tracks, tier, self.map_id))
        return CONFIG_DB_CURSOR.fetchall()

    @final
    def get_switches_to_unlock_with_environment(self, tier):
        CONFIG_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, switch_type FROM switches_config 
                                    WHERE track_unlocked_with <= ? AND environment_unlocked_with = ? AND map_id = ?''',
                                 (self.unlocked_tracks, tier, self.map_id))
        return CONFIG_DB_CURSOR.fetchall()

    @final
    def get_crossovers_to_unlock_with_environment(self, tier):
        CONFIG_DB_CURSOR.execute('''SELECT track_param_1, track_param_2, crossover_type FROM crossovers_config 
                                    WHERE track_unlocked_with <= ? AND environment_unlocked_with = ? AND map_id = ?''',
                                 (self.unlocked_tracks, tier, self.map_id))
        return CONFIG_DB_CURSOR.fetchall()
