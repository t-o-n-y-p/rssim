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
        self.logger.info('START INIT')
        self.user_db_cursor.execute('''SELECT busy, force_busy, last_entered_by, current_position FROM switches 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (track_param_1, track_param_2, switch_type))
        self.busy, self.force_busy, self.last_entered_by, self.current_position = self.user_db_cursor.fetchone()
        self.busy = bool(self.force_busy)
        self.force_busy = bool(self.force_busy)
        self.logger.debug(f'busy: {self.busy}')
        self.logger.debug(f'force_busy: {self.force_busy}')
        self.logger.debug(f'last_entered_by: {self.last_entered_by}')
        self.logger.debug(f'current_position: {self.current_position}')
        self.config_db_cursor.execute('''SELECT track, train_route, section_number FROM train_route_sections
                                         WHERE track_param_1 = ? AND track_param_2 = ? AND section_type = ?''',
                                      (track_param_1, track_param_2, switch_type))
        self.state_change_listeners = self.config_db_cursor.fetchall()
        self.logger.debug(f'state_change_listeners: {self.state_change_listeners}')
        self.logger.info('END INIT')

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.on_activate_view()
        self.logger.info('END ON_ACTIVATE')

    def on_activate_view(self):
        """
        Activates the Railroad switch view.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.on_activate()
        self.logger.info('END ON_ACTIVATE_VIEW')

    @model_is_active
    def on_deactivate(self):
        """
        Deactivates the model.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.logger.info('END ON_DEACTIVATE')

    def on_save_state(self):
        """
        Saves railroad switch state to user progress database.
        """
        self.logger.info('START ON_SAVE_STATE')
        track_param_1 = self.controller.track_param_1
        self.logger.debug(f'track_param_1: {track_param_1}')
        track_param_2 = self.controller.track_param_2
        self.logger.debug(f'track_param_2: {track_param_2}')
        switch_type = self.controller.switch_type
        self.logger.debug(f'switch_type: {switch_type}')
        self.logger.debug(f'busy: {self.busy}')
        self.logger.debug(f'force_busy: {self.force_busy}')
        self.logger.debug(f'last_entered_by: {self.last_entered_by}')
        self.logger.debug(f'current_position: {self.current_position}')
        self.user_db_cursor.execute('''UPDATE switches SET busy = ?, force_busy = ?, 
                                       last_entered_by = ?, current_position = ? 
                                       WHERE track_param_1 = ? AND track_param_2 = ? AND switch_type = ?''',
                                    (int(self.busy), int(self.force_busy), self.last_entered_by, self.current_position,
                                     track_param_1, track_param_2, switch_type))
        self.logger.debug('state saved successfully')
        self.logger.info('END ON_SAVE_STATE')

    def on_force_busy_on(self, positions, train_id):
        """
        Locks switch in required position since the train is approaching.

        :param positions:               direction the train is about to proceed to
        :param train_id:                ID of the train which is about to pass through the switch
        """
        self.logger.info('START ON_FORCE_BUSY_ON')
        self.force_busy = True
        self.logger.debug(f'force_busy: {self.force_busy}')
        self.busy = True
        self.logger.debug(f'busy: {self.busy}')
        self.last_entered_by = train_id
        self.current_position = positions[0]
        self.logger.debug(f'current_position: {self.current_position}')
        self.logger.debug(f'state_change_listeners: {self.state_change_listeners}')
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=True)

        self.logger.info('END ON_FORCE_BUSY_ON')

    def on_force_busy_off(self):
        """
        Unlocks switch position after the train has passed it.
        """
        self.logger.info('START ON_FORCE_BUSY_OFF')
        self.force_busy = False
        self.logger.debug(f'force_busy: {self.force_busy}')
        self.busy = False
        self.logger.debug(f'busy: {self.busy}')
        self.logger.debug(f'state_change_listeners: {self.state_change_listeners}')
        for listener in self.state_change_listeners:
            self.controller.parent_controller.on_update_train_route_section_status(listener, status=False)

        self.logger.info('END ON_FORCE_BUSY_OFF')
