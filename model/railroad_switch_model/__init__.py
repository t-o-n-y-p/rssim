from logging import getLogger

from model import *
from database import USER_DB_CURSOR, CONFIG_DB_CURSOR


class RailroadSwitchModel(MapBaseModel):
    def __init__(self, controller, view, map_id, track_param_1, track_param_2, switch_type):
        super().__init__(controller, view, map_id, logger=getLogger(
                f'root.app.game.map.{map_id}.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.model'
            )
        )
        self.track_param_1 = track_param_1
        self.track_param_2 = track_param_2
        self.switch_type = switch_type
        USER_DB_CURSOR.execute('''SELECT busy, force_busy FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? AND map_id = ?''',
                               (self.track_param_1, self.track_param_2, self.switch_type, self.map_id))
        self.busy, self.force_busy = (bool(t) for t in USER_DB_CURSOR.fetchone())
        USER_DB_CURSOR.execute('''SELECT last_entered_by, current_position FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? AND map_id = ?''',
                               (self.track_param_1, self.track_param_2, self.switch_type, self.map_id))
        self.last_entered_by, self.current_position = USER_DB_CURSOR.fetchone()
        CONFIG_DB_CURSOR.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                    WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ? 
                                    AND map_id = ?''',
                                 (self.track_param_1, self.track_param_2, self.switch_type, self.map_id))
        self.state_change_listeners = CONFIG_DB_CURSOR.fetchall()
        USER_DB_CURSOR.execute('''SELECT locked FROM switches 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? AND map_id = ?''',
                               (self.track_param_1, self.track_param_2, self.switch_type, self.map_id))
        self.locked = bool(USER_DB_CURSOR.fetchone()[0])

    @final
    def on_save_state(self):
        USER_DB_CURSOR.execute('''UPDATE switches SET busy = ?, force_busy = ?, 
                                  last_entered_by = ?, current_position = ?, locked = ? 
                                  WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ? AND map_id = ?''',
                               (int(self.busy), int(self.force_busy), self.last_entered_by, self.current_position,
                                int(self.locked), self.track_param_1, self.track_param_2, self.switch_type,
                                self.map_id))

    @final
    def on_force_busy_on(self, positions, train_id):
        self.force_busy = True
        self.busy = True
        self.last_entered_by = train_id
        self.current_position = positions[0]
        self.view.on_change_current_position(self.current_position)
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=True)

    @final
    def on_force_busy_off(self):
        self.force_busy = False
        self.busy = False
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=False)
