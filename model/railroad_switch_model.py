from logging import getLogger

from model import *


class RailroadSwitchModel(Model):
    """
    Implements Railroad switch model.
    Railroad switch object is responsible for properties, UI and events related to the railroad switch.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor, track_param_1, track_param_2, switch_type):
        """
        Properties:
            busy                                indicates if any switch direction is busy
            force_busy                          indicates if any switch direction is force_busy
            last_entered_by                     train ID which made the switch direction force_busy last time
            state_change_listeners              train route sections which share this switch
            current_position                    current switch position
            locked                              indicates if switch is available for player

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param track_param_1:                   number of the straight track
        :param track_param_2:                   number of the diverging track
        :param switch_type:                     railroad switch location: left/right side of the map
        """
        super().__init__(
            user_db_connection, user_db_cursor, config_db_cursor,
            logger=getLogger(
                f'root.app.game.map.railroad_switch.{track_param_1}.{track_param_2}.{switch_type}.model'
            )
        )
        self.user_db_cursor.execute('''SELECT busy, force_busy FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (track_param_1, track_param_2, switch_type))
        self.busy, self.force_busy = list(map(bool, self.user_db_cursor.fetchone()))
        self.user_db_cursor.execute('''SELECT last_entered_by, current_position FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (track_param_1, track_param_2, switch_type))
        self.last_entered_by, self.current_position = self.user_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?''',
                                      (track_param_1, track_param_2, switch_type))
        self.state_change_listeners = self.config_db_cursor.fetchall()
        self.user_db_cursor.execute('''SELECT locked FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (track_param_1, track_param_2, switch_type))
        self.locked = bool(self.user_db_cursor.fetchone()[0])

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True
        self.on_activate_view()

    def on_activate_view(self):
        """
        Activates the Railroad switch view.
        """
        self.view.on_activate()

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.is_activated = False

    def on_save_state(self):
        """
        Saves railroad switch state to user progress database.
        """
        track_param_1 = self.controller.track_param_1
        track_param_2 = self.controller.track_param_2
        switch_type = self.controller.switch_type
        self.user_db_cursor.execute('''UPDATE switches SET busy = ?, force_busy = ?, 
                                       last_entered_by = ?, current_position = ?, locked = ? 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (int(self.busy), int(self.force_busy), self.last_entered_by, self.current_position,
                                     int(self.locked), track_param_1, track_param_2, switch_type))

    def on_force_busy_on(self, positions, train_id):
        """
        Locks switch in required position since the train is approaching.

        :param positions:               direction the train is about to proceed to
        :param train_id:                ID of the train which is about to pass through the switch
        """
        self.force_busy = True
        self.busy = True
        self.last_entered_by = train_id
        self.current_position = positions[0]
        self.view.on_change_current_position(self.current_position)
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=True)

    def on_force_busy_off(self):
        """
        Unlocks switch position after the train has passed it.
        """
        self.force_busy = False
        self.busy = False
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=False)

    def on_unlock(self):
        """
        Updates switch lock state. Notifies the view about lock state update.
        """
        self.locked = False
        self.view.on_unlock()
