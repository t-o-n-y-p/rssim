from logging import getLogger

from model import *


class SignalModel(Model):
    """
    Implements Signal model.
    Signal object is responsible for properties, UI and events related to the signal state.
    """
    def __init__(self, user_db_connection, user_db_cursor, config_db_cursor, track, base_route):
        """
        Properties:
            state                               indicates if signal is red or green
            locked                              indicates if signal is locked

        :param user_db_connection:              connection to the user DB (stores game state and user-defined settings)
        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param track:                           signal track number
        :param base_route:                      base route (train route part) which signal belongs to
        """
        super().__init__(user_db_connection, user_db_cursor, config_db_cursor,
                         logger=getLogger(f'root.app.game.map.signal.{track}.{base_route}.model'))
        self.logger.info('START INIT')
        self.user_db_cursor.execute('SELECT state, locked FROM signals WHERE track = ? AND base_route = ?',
                                    (track, base_route))
        self.state, self.locked = self.user_db_cursor.fetchone()
        self.locked = bool(self.locked)
        self.logger.debug(f'state: {self.state}')
        self.logger.debug(f'locked: {self.locked}')
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
        Updates state and locked values and activates the view.
        """
        self.logger.info('START ON_ACTIVATE_VIEW')
        self.view.state = self.state
        self.logger.debug(f'view.state = {self.view.state}')
        self.view.locked = self.locked
        self.logger.debug(f'view.locked = {self.view.locked}')
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
        self.logger.debug(f'state = {self.state}')
        self.logger.debug(f'locked = {self.locked}')
        self.user_db_cursor.execute('UPDATE signals SET state = ?, locked = ? WHERE track = ? AND base_route = ?',
                                    (self.state, int(self.locked), self.controller.track, self.controller.base_route))
        self.logger.debug('state saved successfully')
        self.logger.info('END ON_SAVE_STATE')

    def on_unlock(self):
        """
        Updates signal lock state. Notifies the view about lock state update.
        """
        self.logger.info('START ON_UNLOCK')
        self.locked = False
        self.logger.debug(f'locked = {self.locked}')
        self.view.on_unlock()
        self.logger.info('END ON_UNLOCK')

    def on_switch_to_green(self):
        """
        Updates signal state to green. Notifies the view about state change.
        """
        self.logger.info('START ON_SWITCH_TO_GREEN')
        self.state = 'green_signal'
        self.logger.debug(f'state = {self.state}')
        self.view.on_change_state(self.state)
        self.logger.info('END ON_SWITCH_TO_GREEN')

    def on_switch_to_red(self):
        """
        Updates signal state to red. Notifies the view about state change.
        """
        self.logger.info('START ON_SWITCH_TO_RED')
        self.state = 'red_signal'
        self.logger.debug(f'state = {self.state}')
        self.view.on_change_state(self.state)
        self.logger.info('END ON_SWITCH_TO_RED')
