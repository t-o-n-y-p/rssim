from logging import getLogger

from pyglet.text import Label

from view import *
from ui.track_cell import TrackCell
from ui.environment_cell import EnvironmentCell
from button.close_constructor_button import CloseConstructorButton
from notifications.track_unlocked_notification import TrackUnlockedNotification
from notifications.environment_unlocked_notification import EnvironmentUnlockedNotification
from notifications.environment_construction_completed_notification import EnvironmentConstructionCompletedNotification
from notifications.track_construction_completed_notification import TrackConstructionCompletedNotification
from i18n import I18N_RESOURCES, i18n_number_category


class ConstructorView(View):
    """
    Implements Constructor view.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        def on_close_constructor(button):
            """
            Notifies controller that player has closed constructor screen.

            :param button:                      button that was clicked
            """
            self.controller.on_deactivate_view()

        def on_buy_construction_action(construction_type, entity_number):
            self.controller.on_deactivate_track_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(0)
            self.controller.on_put_under_construction(construction_type, entity_number)

        def on_set_money_target_action(construction_type, row, entity_number):
            self.controller.on_activate_track_money_target()
            for i in range(len(self.constructor_cells[construction_type])):
                if i != row:
                    self.constructor_cells[construction_type][i].on_deactivate_money_target()

            for i in range(len(self.constructor_cells[(construction_type + 1) % 2])):
                self.constructor_cells[(construction_type + 1) % 2][i].on_deactivate_money_target()

            self.money_target_activated = True
            self.money_target_position = (construction_type, row)
            self.controller.parent_controller.parent_controller.on_update_money_target(
                self.construction_state_matrix[construction_type][entity_number][PRICE]
            )

        def on_reset_money_target_action():
            self.controller.on_deactivate_track_money_target()
            self.money_target_activated = False
            self.controller.parent_controller.parent_controller.on_update_money_target(0)

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.map.constructor.view'))
        self.constructor_opacity = 0
        self.railway_station_caption_sprite = None
        self.railway_station_caption_position = [0, 0]
        self.environment_caption_sprite = None
        self.environment_caption_position = [0, 0]
        self.construction_state_matrix = None
        self.money = 0
        self.close_constructor_button = CloseConstructorButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                               groups=self.groups, on_click_action=on_close_constructor)
        self.buttons = [self.close_constructor_button, ]
        self.constructor_cells = [[], []]
        for j in range(4):
            self.constructor_cells[0][j] = TrackCell(0, j, self.config_db_cursor, self.surface, self.batches,
                                                     self.groups, self.current_locale, on_buy_construction_action,
                                                     on_set_money_target_action, on_reset_money_target_action)
            self.buttons.extend(self.constructor_cells[0][j].buttons)

        for j in range(4):
            self.constructor_cells[1][j] = EnvironmentCell(0, j, self.config_db_cursor, self.surface, self.batches,
                                                           self.groups, self.current_locale, on_buy_construction_action,
                                                           on_set_money_target_action, on_reset_money_target_action)
            self.buttons.extend(self.constructor_cells[1][j].buttons)

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.railway_station_caption_sprite \
            = Label(I18N_RESOURCES['railway_station_caption_string'][self.current_locale],
                    font_name='Arial', font_size=self.caption_font_size,
                    x=self.railway_station_caption_position[0],
                    y=self.railway_station_caption_position[1],
                    anchor_x='center', anchor_y='center',
                    batch=self.batches['ui_batch'], group=self.groups['button_text'])
        self.environment_caption_sprite \
            = Label(I18N_RESOURCES['environment_caption_string'][self.current_locale],
                    font_name='Arial', font_size=self.caption_font_size,
                    x=self.environment_caption_position[0],
                    y=self.environment_caption_position[1],
                    anchor_x='center', anchor_y='center',
                    batch=self.batches['ui_batch'], group=self.groups['button_text'])

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all labels and buttons.
        """
        self.is_activated = False
        self.railway_station_caption_sprite.delete()
        self.railway_station_caption_sprite = None
        self.environment_caption_sprite.delete()
        self.environment_caption_sprite = None
        for j in range(4):
            self.constructor_cells[0][j].on_deactivate()

        for j in range(4):
            self.constructor_cells[1][j].on_deactivate()

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

            remaining_tracks = sorted(list(self.construction_state_matrix[0].keys()))
            for j in range(min(len(remaining_tracks), 4)):
                if not self.constructor_cells[0][j].is_activated:
                    self.constructor_cells[0][j].on_activate()
                    self.constructor_cells[0][j]\
                        .on_assign_new_data(remaining_tracks[j], self.construction_state_matrix[0][remaining_tracks[j]])
                    return

            for j in range(len(remaining_tracks), 4):
                if not self.constructor_cells[0][j].is_activated:
                    self.constructor_cells[0][j].on_activate()
                    self.constructor_cells[0][j].on_assign_new_data(0, [])
                    return

            remaining_tiers = sorted(list(self.construction_state_matrix[1].keys()))
            for j in range(min(len(remaining_tiers), 4)):
                if not self.constructor_cells[1][j].is_activated:
                    self.constructor_cells[1][j].on_activate()
                    self.constructor_cells[1][j]\
                        .on_assign_new_data(remaining_tiers[j], self.construction_state_matrix[1][remaining_tiers[j]])
                    return

            for j in range(len(remaining_tiers), 4):
                if not self.constructor_cells[1][j].is_activated:
                    self.constructor_cells[1][j].on_activate()
                    self.constructor_cells[1][j].on_assign_new_data(0, [])
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
        self.on_read_ui_info()
        if self.is_activated:
            self.railway_station_caption_sprite.x = self.railway_station_caption_position[0]
            self.railway_station_caption_sprite.y = self.railway_station_caption_position[1]
            self.railway_station_caption_sprite.font_size = self.caption_font_size
            self.environment_caption_sprite.x = self.environment_caption_position[0]
            self.environment_caption_sprite.y = self.environment_caption_position[1]
            self.environment_caption_sprite.font_size = self.caption_font_size

        for j in range(4):
            self.constructor_cells[0][j].on_change_screen_resolution(screen_resolution)

        for j in range(4):
            self.constructor_cells[1][j].on_change_screen_resolution(screen_resolution)

        self.close_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                      int(self.close_constructor_button.base_font_size_property
                                                          * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_money(self, money):
        self.money = money
        for j in range(4):
            self.constructor_cells[0][j].on_update_money(money)

        for j in range(4):
            self.constructor_cells[1][j].on_update_money(money)

    def on_update_construction_state(self, construction_state_matrix, game_time):
        self.construction_state_matrix = construction_state_matrix

    @view_is_active
    def on_unlock_track_live(self, track):
        """
        Deletes unlocked track and moves all cells one position to the top of the screen.

        :param track:                   track number
        """
        cell_step = self.cell_height + self.interval_between_cells
        self.locked_tracks_labels[track].delete()
        self.locked_tracks_labels.pop(track)
        for t in self.locked_tracks_labels:
            self.locked_tracks_labels[t].y += cell_step

        self.title_tracks_labels[track].delete()
        self.title_tracks_labels.pop(track)
        for t in self.title_tracks_labels:
            self.title_tracks_labels[t].y += cell_step

        self.description_tracks_labels[track].delete()
        self.description_tracks_labels.pop(track)
        for t in self.description_tracks_labels:
            self.description_tracks_labels[t].y += cell_step

        for p in range(len(self.no_more_tracks_available_labels)):
            self.no_more_tracks_available_labels[p].y += cell_step

    @view_is_active
    def on_unlock_environment_live(self, tier):
        """
        Deletes unlocked tier and moves all cells one position to the top of the screen.

        :param tier:                    environment tier number
        """
        cell_step = self.cell_height + self.interval_between_cells
        self.locked_tiers_labels[tier].delete()
        self.locked_tiers_labels.pop(tier)
        for t in self.locked_tiers_labels:
            self.locked_tiers_labels[t].y += cell_step

        self.title_tiers_labels[tier].delete()
        self.title_tiers_labels.pop(tier)
        for t in self.title_tiers_labels:
            self.title_tiers_labels[t].y += cell_step

        self.description_tiers_labels[tier].delete()
        self.description_tiers_labels.pop(tier)
        for t in self.description_tiers_labels:
            self.description_tiers_labels[t].y += cell_step

        for p in range(len(self.no_more_tiers_available_labels)):
            self.no_more_tiers_available_labels[p].y += cell_step

    def on_read_ui_info(self):
        """
        Reads aff offsets and font size from the database.
        """
        self.config_db_cursor.execute('''SELECT constructor_railway_station_caption_x, constructor_caption_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.railway_station_caption_position = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT constructor_environment_caption_x, constructor_caption_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.environment_caption_position = self.config_db_cursor.fetchone()
        self.config_db_cursor.execute('''SELECT constructor_cell_height, constructor_interval_between_cells
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.cell_height, self.interval_between_cells = self.config_db_cursor.fetchone()
        cell_step = self.cell_height + self.interval_between_cells
        self.config_db_cursor.execute('''SELECT constructor_cell_top_left_x, constructor_cell_top_left_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        fetched_coords = self.config_db_cursor.fetchone()
        self.track_cells_positions = ((fetched_coords[0], fetched_coords[1]),
                                      (fetched_coords[0], fetched_coords[1] - cell_step),
                                      (fetched_coords[0], fetched_coords[1] - cell_step * 2),
                                      (fetched_coords[0], fetched_coords[1] - cell_step * 3))
        self.config_db_cursor.execute('''SELECT constructor_cell_top_right_x, constructor_cell_top_right_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        fetched_coords = self.config_db_cursor.fetchone()
        self.environment_cell_positions = ((fetched_coords[0], fetched_coords[1]),
                                           (fetched_coords[0], fetched_coords[1] - cell_step),
                                           (fetched_coords[0], fetched_coords[1] - cell_step * 2),
                                           (fetched_coords[0], fetched_coords[1] - cell_step * 3))
        self.config_db_cursor.execute('''SELECT constructor_locked_label_offset_x, constructor_locked_label_offset_y,
                                         constructor_build_button_offset_x, constructor_build_button_offset_y,
                                         constructor_title_text_offset_x, constructor_title_text_offset_y,
                                         constructor_description_text_offset_x, constructor_description_text_offset_y,
                                         constructor_placeholder_offset_x, constructor_placeholder_offset_y,
                                         constructor_locked_label_font_size, constructor_title_text_font_size,
                                         constructor_description_text_font_size, constructor_placeholder_font_size,
                                         constructor_caption_font_size 
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.locked_label_offset[0], self.locked_label_offset[1], \
            self.track_build_button_offset[0], self.track_build_button_offset[1], \
            self.title_label_offset[0], self.title_label_offset[1], \
            self.description_label_offset[0], self.description_label_offset[1], \
            self.placeholder_offset[0], self.placeholder_offset[1], \
            self.locked_label_font_size, self.title_label_font_size, \
            self.description_label_font_size, self.placeholder_font_size, \
            self.caption_font_size = self.config_db_cursor.fetchone()

    def on_update_current_locale(self, new_locale):
        """
        Updates current locale selected by user and all text labels.

        :param new_locale:                      selected locale
        """
        self.current_locale = new_locale
        if self.is_activated:
            self.railway_station_caption_sprite.text \
                = I18N_RESOURCES['railway_station_caption_string'][self.current_locale]
            self.environment_caption_sprite.text = I18N_RESOURCES['environment_caption_string'][self.current_locale]

            for i in self.no_more_tracks_available_labels:
                i.text = I18N_RESOURCES['no_more_tracks_available_placeholder_string'][self.current_locale]

            for i in self.title_tracks_labels:
                self.title_tracks_labels[i].text \
                    = I18N_RESOURCES['title_track_string'][self.current_locale].format(i)

            for i in self.description_tracks_labels:
                if self.track_state_matrix[i][UNLOCK_AVAILABLE]:
                    self.description_tracks_labels[i].text \
                        = I18N_RESOURCES['unlock_available_track_description_string'][self.current_locale]\
                        .format(self.track_state_matrix[i][PRICE]).replace(',', ' ')
                elif self.track_state_matrix[i][UNDER_CONSTRUCTION]:
                    construction_time = self.track_state_matrix[i][CONSTRUCTION_TIME]
                    self.description_tracks_labels[i].text \
                        = I18N_RESOURCES['under_construction_track_description_string'][self.current_locale]\
                        .format(construction_time // FRAMES_IN_ONE_HOUR,
                                (construction_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
                else:
                    if not self.track_state_matrix[i][UNLOCK_CONDITION_FROM_LEVEL]:
                        self.description_tracks_labels[i].text \
                            = I18N_RESOURCES[
                            'unlock_condition_from_level_track_description_string'
                        ][self.current_locale].format(self.track_state_matrix[i][LEVEL_REQUIRED])
                    elif not self.track_state_matrix[i][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                        self.description_tracks_labels[i].text \
                            = I18N_RESOURCES[
                            'unlock_condition_from_environment_track_description_string'
                        ][self.current_locale].format(0)
                    elif not self.track_state_matrix[i][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
                        self.description_tracks_labels[i].text \
                            = I18N_RESOURCES[
                            'unlock_condition_from_previous_track_track_description_string'
                        ][self.current_locale].format(i - 1)

    def on_activate_track_money_target(self):
        """
        Updates track_money_target_activated flag value.
        Money target buttons are displayed based on this flag.
        """
        self.track_money_target_activated = True

    def on_deactivate_track_money_target(self):
        """
        Updates track_money_target_activated flag value.
        Money target buttons are displayed based on this flag.
        """
        self.track_money_target_activated = False

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
