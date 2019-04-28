from logging import getLogger

from model import *


class SignalModel(Model):
    """
    Implements Signal model.
    Signal object is responsible for properties, UI and events related to the signal state.
    """
    def __init__(self, map_id, track, base_route):
        """
        Properties:
            map_id                              ID of the map which this signal belongs to
            state                               indicates if signal is red or green
            locked                              indicates if signal is locked

        :param map_id:                          ID of the map which this signal belongs to
        :param track:                           signal track number
        :param base_route:                      base route (train route part) which signal belongs to
        """
        super().__init__(logger=getLogger(f'root.app.game.map.{map_id}.signal.{track}.{base_route}.model'))
        self.map_id = map_id
        self.user_db_cursor.execute('''SELECT state, locked FROM signals 
                                       WHERE track = ? AND base_route = ? AND map_id = ?''',
                                    (track, base_route, self.map_id))
        self.state, self.locked = self.user_db_cursor.fetchone()
        self.locked = bool(self.locked)

    @model_is_not_active
    def on_activate(self):
        """
        Activates the model and the view.
        """
        self.is_activated = True

    def on_activate_view(self):
        """
        Updates state and locked values and activates the view.
        """
        self.view.state = self.state
        self.view.locked = self.locked
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
        self.user_db_cursor.execute('''UPDATE signals SET state = ?, locked = ? 
                                       WHERE track = ? AND base_route = ? AND map_id = ?''',
                                    (self.state, int(self.locked), self.controller.track, self.controller.base_route,
                                     self.map_id))

    def on_unlock(self):
        """
        Updates signal lock state. Notifies the view about lock state update.
        """
        self.locked = False
        self.view.on_unlock()

    def on_switch_to_green(self):
        """
        Updates signal state to green. Notifies the view about state change.
        """
        self.state = 'green_signal'
        self.view.on_change_state(self.state)

    def on_switch_to_red(self):
        """
        Updates signal state to red. Notifies the view about state change.
        """
        self.state = 'red_signal'
        self.view.on_change_state(self.state)
