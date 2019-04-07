from logging import getLogger

from view import *
from ui.constructor.track_cell import TrackCell
from ui.constructor.environment_cell import EnvironmentCell
from ui.button.close_constructor_button import CloseConstructorButton
from notifications.track_unlocked_notification import TrackUnlockedNotification
from notifications.environment_unlocked_notification import EnvironmentUnlockedNotification
from notifications.environment_construction_completed_notification import EnvironmentConstructionCompletedNotification
from notifications.track_construction_completed_notification import TrackConstructionCompletedNotification


class ConstructorView(View):
    """
    Implements Constructor view.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, user_db_cursor, config_db_cursor):
        """
        Button click handlers:
            on_close_constructor                on_click handler for close constructor button

        Constructor cell actions handlers:
            on_buy_construction_action          is activated when player buys construction
            on_set_money_target_action          is activated when money target is activated by player
            on_reset_money_target_action        is activated when money target is deactivated by player

        Properties:
            constructor_opacity                                 general opacity of constructor screen
            construction_state_matrix                           tracks and environment state storage
            money                                               current amount of money
            close_constructor_button                            CloseConstructorButton object
            buttons                                             list of all buttons
            constructor_cells                                   track and environment cells on constructor screen
            feature_unlocked_notification_enabled               indicates if notifications about track/tier unlock event
                                                                are enabled
            construction_completed_notification_enabled         indicates if notifications about track/tier construction
                                                                ending event are enabled
            money_target_activated                              indicates if money target for any construction
                                                                is activated
            money_target_cell_position                          column and row of constructor view cell
                                                                the target was last activated

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        """
        def on_close_constructor(button):
            """
            Notifies controller that player has closed constructor screen.

            :param button:                      button that was clicked
            """
            self.controller.on_deactivate_view()

        def on_buy_construction_action(construction_type, row, entity_number):
            """
            Puts given entity under construction and deactivates money target if this cell was selected.

            :param construction_type:       type of construction: track or environment
            :param row:                     number of cell on constructor screen
            :param entity_number:           number of track or environment tier
            """
            self.controller.on_put_under_construction(construction_type, entity_number)
            if self.money_target_activated and self.money_target_cell_position == [construction_type, row]:
                self.controller.on_deactivate_money_target()
                self.controller.parent_controller.parent_controller.on_update_money_target(0)

        def on_set_money_target_action(construction_type, row, entity_number):
            """
            Enables and activates money target for given cell on constructor screen.

            :param construction_type:       type of construction: track or environment
            :param row:                     number of cell on constructor screen
            :param entity_number:           number of track or environment tier
            """
            self.controller.on_activate_money_target(construction_type, row)
            self.controller.parent_controller.parent_controller.on_update_money_target(
                self.construction_state_matrix[construction_type][entity_number][PRICE]
            )

        def on_reset_money_target_action():
            """
            Disables and deactivates money target.
            """
            self.controller.on_deactivate_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(0)

        self.map_id = None
        self.on_update_map_id()
        super().__init__(user_db_cursor, config_db_cursor, logger=getLogger('root.app.game.map.constructor.view'))
        self.constructor_opacity = 0
        self.construction_state_matrix = None
        self.money = 0
        self.close_constructor_button = CloseConstructorButton(on_click_action=on_close_constructor)
        self.buttons = [self.close_constructor_button, ]
        track_cells = []
        environment_cells = []
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            track_cells.append(
                TrackCell(TRACKS, j, self.current_locale, on_buy_construction_action,
                          on_set_money_target_action, on_reset_money_target_action)
            )
            self.buttons.extend(track_cells[j].buttons)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            environment_cells.append(
                EnvironmentCell(ENVIRONMENT, j, self.current_locale, on_buy_construction_action,
                                on_set_money_target_action, on_reset_money_target_action)
            )
            self.buttons.extend(environment_cells[j].buttons)

        self.constructor_cells = [track_cells, environment_cells]
        self.user_db_cursor.execute('''SELECT feature_unlocked_notification_enabled, 
                                       construction_completed_notification_enabled FROM notification_settings''')
        self.feature_unlocked_notification_enabled, self.construction_completed_notification_enabled \
            = self.user_db_cursor.fetchone()
        self.feature_unlocked_notification_enabled = bool(self.feature_unlocked_notification_enabled)
        self.construction_completed_notification_enabled = bool(self.construction_completed_notification_enabled)
        self.user_db_cursor.execute('''SELECT money_target_activated FROM constructor WHERE map_id = ?''',
                                    (self.map_id, ))
        self.money_target_activated = bool(self.user_db_cursor.fetchone()[0])
        self.user_db_cursor.execute('''SELECT money_target_cell_position FROM constructor WHERE map_id = ?''',
                                    (self.map_id, ))
        self.money_target_cell_position = list(map(int, self.user_db_cursor.fetchone()[0].split(',')))

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_deactivate()

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_deactivate()

        for b in self.buttons:
            b.on_deactivate()

    def on_update(self):
        """
        Updates fade-in/fade-out animations and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        if self.is_activated:
            if self.constructor_opacity < 255:
                self.constructor_opacity += 15

            remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
            for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
                if not self.constructor_cells[TRACKS][j].is_activated:
                    self.constructor_cells[TRACKS][j].on_activate()
                    self.constructor_cells[TRACKS][j]\
                        .on_assign_new_data(remaining_tracks[j],
                                            self.construction_state_matrix[TRACKS][remaining_tracks[j]])
                    if self.money_target_activated and self.money_target_cell_position == [TRACKS, j]:
                        self.constructor_cells[TRACKS][j].on_activate_money_target()
                    else:
                        self.constructor_cells[TRACKS][j].on_deactivate_money_target()

                    return

            for j in range(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS):
                if not self.constructor_cells[TRACKS][j].is_activated:
                    self.constructor_cells[TRACKS][j].on_activate()
                    self.constructor_cells[TRACKS][j].on_assign_new_data(0, [])
                    return

            remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
            for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
                if not self.constructor_cells[ENVIRONMENT][j].is_activated:
                    self.constructor_cells[ENVIRONMENT][j].on_activate()
                    self.constructor_cells[ENVIRONMENT][j]\
                        .on_assign_new_data(remaining_tiers[j],
                                            self.construction_state_matrix[ENVIRONMENT][remaining_tiers[j]])
                    if self.money_target_activated and self.money_target_cell_position == [ENVIRONMENT, j]:
                        self.constructor_cells[ENVIRONMENT][j].on_activate_money_target()
                    else:
                        self.constructor_cells[ENVIRONMENT][j].on_deactivate_money_target()

                    return

            for j in range(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
                if not self.constructor_cells[ENVIRONMENT][j].is_activated:
                    self.constructor_cells[ENVIRONMENT][j].on_activate()
                    self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(0, [])
                    return

        if not self.is_activated:
            if self.constructor_opacity > 0:
                self.constructor_opacity -= 15

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.on_recalculate_ui_properties(screen_resolution)
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_change_screen_resolution(screen_resolution)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_change_screen_resolution(screen_resolution)

        self.close_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_money(self, money):
        """
        Updates bank account state to determine if player has enough money to buy something.

        :param money:                   new bank account state
        """
        self.money = money
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_update_money(money)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_update_money(money)

    def on_update_construction_state(self, construction_state_matrix, construction_type, entity_number, game_time=0):
        """
        Updates state for given construction.

        :param construction_state_matrix:       tracks and environment state storage
        :param construction_type:               type of construction: track or environment
        :param entity_number:                   number of track or environment tier
        :param game_time:                       current in-game time
        """
        self.construction_state_matrix = construction_state_matrix
        if construction_type == TRACKS:
            remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
            self.constructor_cells[construction_type][remaining_tracks.index(entity_number)]\
                .on_update_state(self.construction_state_matrix[TRACKS][entity_number])
        elif construction_type == ENVIRONMENT:
            remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
            self.constructor_cells[construction_type][remaining_tiers.index(entity_number)]\
                .on_update_state(self.construction_state_matrix[ENVIRONMENT][entity_number])

    @view_is_active
    def on_unlock_construction(self, construction_type, entity_number):
        """
        Removes unlocked construction from constructor screen and updates all cells.

        :param construction_type:               type of construction: track or environment
        :param entity_number:                   number of track or environment tier
        :return:
        """
        if self.money_target_activated and self.money_target_cell_position[0] == construction_type \
                and self.money_target_cell_position[1] > 0:
            self.money_target_cell_position[1] -= 1

        if construction_type == TRACKS:
            remaining_tracks = sorted(list(self.construction_state_matrix[TRACKS].keys()))
            remaining_tracks.remove(entity_number)
            for j in range(min(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS)):
                self.constructor_cells[TRACKS][j] \
                    .on_assign_new_data(remaining_tracks[j],
                                        self.construction_state_matrix[TRACKS][remaining_tracks[j]])
                if self.money_target_activated and self.money_target_cell_position == [TRACKS, j]:
                    self.constructor_cells[TRACKS][j].on_activate_money_target()
                else:
                    self.constructor_cells[TRACKS][j].on_deactivate_money_target()

            for j in range(len(remaining_tracks), CONSTRUCTOR_VIEW_TRACK_CELLS):
                self.constructor_cells[TRACKS][j].on_assign_new_data(0, [])

        elif construction_type == ENVIRONMENT:
            remaining_tiers = sorted(list(self.construction_state_matrix[ENVIRONMENT].keys()))
            remaining_tiers.remove(entity_number)
            for j in range(min(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS)):
                self.constructor_cells[ENVIRONMENT][j] \
                    .on_assign_new_data(remaining_tiers[j],
                                        self.construction_state_matrix[ENVIRONMENT][remaining_tiers[j]])
                if self.money_target_activated and self.money_target_cell_position == [ENVIRONMENT, j]:
                    self.constructor_cells[TRACKS][j].on_activate_money_target()
                else:
                    self.constructor_cells[TRACKS][j].on_deactivate_money_target()

            for j in range(len(remaining_tiers), CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
                self.constructor_cells[ENVIRONMENT][j].on_assign_new_data(0, [])

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        for j in range(CONSTRUCTOR_VIEW_TRACK_CELLS):
            self.constructor_cells[TRACKS][j].on_update_current_locale(self.current_locale)

        for j in range(CONSTRUCTOR_VIEW_ENVIRONMENT_CELLS):
            self.constructor_cells[ENVIRONMENT][j].on_update_current_locale(self.current_locale)

    def on_activate_money_target(self, construction_type, row):
        """
        Activates money target on given cell.

        :param construction_type:       type of construction: track or environment
        :param row:                     number of cell on constructor screen
        """
        self.money_target_activated = True
        self.money_target_cell_position = [construction_type, row]
        for i in range(len(self.constructor_cells)):
            for j in range(len(self.constructor_cells[i])):
                if i == construction_type and j == row:
                    self.constructor_cells[i][j].on_activate_money_target()
                else:
                    self.constructor_cells[i][j].on_deactivate_money_target()

    def on_deactivate_money_target(self):
        """
        Deactivates money target for all cells.
        """
        self.money_target_activated = False
        for i in range(len(self.constructor_cells)):
            for j in range(len(self.constructor_cells[i])):
                self.constructor_cells[i][j].on_deactivate_money_target()

    @notifications_available
    @feature_unlocked_notification_enabled
    def on_send_track_unlocked_notification(self, track):
        """
        Sends system notification when new track is unlocked.

        :param track:                           track number
        """
        track_unlocked_notification = TrackUnlockedNotification()
        track_unlocked_notification.send(self.current_locale, message_args=(track,))
        self.controller.parent_controller.parent_controller.parent_controller\
            .on_append_notification(track_unlocked_notification)

    @notifications_available
    @feature_unlocked_notification_enabled
    def on_send_environment_unlocked_notification(self, tier):
        """
        Sends system notification when new environment tier is unlocked.

        :param tier:                            environment tier number
        """
        environment_unlocked_notification = EnvironmentUnlockedNotification()
        environment_unlocked_notification.send(self.current_locale, message_args=(tier,))
        self.controller.parent_controller.parent_controller.parent_controller\
            .on_append_notification(environment_unlocked_notification)

    @notifications_available
    @construction_completed_notification_enabled
    def on_send_track_construction_completed_notification(self, track):
        """
        Sends system notification when track construction is completed.

        :param track:                           track number
        """
        track_construction_completed_notification = TrackConstructionCompletedNotification()
        track_construction_completed_notification.send(self.current_locale, message_args=(track,))
        self.controller.parent_controller.parent_controller.parent_controller\
            .on_append_notification(track_construction_completed_notification)

    @notifications_available
    @construction_completed_notification_enabled
    def on_send_environment_construction_completed_notification(self, tier):
        """
        Sends system notification when environment tier construction is completed.

        :param tier:                            environment tier number
        """
        environment_construction_completed_notification = EnvironmentConstructionCompletedNotification()
        environment_construction_completed_notification.send(self.current_locale, message_args=(tier,))
        self.controller.parent_controller.parent_controller.parent_controller\
            .on_append_notification(environment_construction_completed_notification)

    def on_change_feature_unlocked_notification_state(self, notification_state):
        """
        Updates feature unlocked notification state.

        :param notification_state:              new notification state defined by player
        """
        self.feature_unlocked_notification_enabled = notification_state

    def on_change_construction_completed_notification_state(self, notification_state):
        """
        Updates construction completed notification state.

        :param notification_state:              new notification state defined by player
        """
        self.construction_completed_notification_enabled = notification_state

    def on_update_map_id(self):
        self.map_id = 0
