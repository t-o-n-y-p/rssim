from logging import getLogger

from pyglet.text import Label

from view import *
from button import create_two_state_button
from button.close_constructor_button import CloseConstructorButton
from button.build_track_button import BuildTrackButton
from button.set_track_money_target_button import SetTrackMoneyTargetButton
from button.reset_track_money_target_button import ResetTrackMoneyTargetButton
from notifications.track_unlocked_notification import TrackUnlockedNotification
from notifications.environment_unlocked_notification import EnvironmentUnlockedNotification
from notifications.environment_construction_completed_notification import EnvironmentConstructionCompletedNotification
from notifications.track_construction_completed_notification import TrackConstructionCompletedNotification
from i18n import I18N_RESOURCES


class ConstructorView(View):
    """
    Implements Constructor view.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_close_constructor                on_click handler for close constructor button
            on_buy_track                        on_click handler for buy track button
            on_set_track_money_target           on_click handler for set track money target button
            on_reset_track_money_target         on_click handler for reset track money target button

        Properties:
            track_cells_positions               list of positions for track cells
            environment_cell_positions          list of positions for environment cells
            locked_label_offset                 "locked" label offset from the cell position
            buy_button_offset                   buy track button offset from the cell position
            title_label_offset                  "Track X" label offset from the cell position
            description_label_offset            track state label offset from the cell position
            placeholder_offset                  cell placeholder offset from the cell position
            locked_label_font_size              font size for label indicating that rack is locked
            title_label_font_size               font size for "Track X" label
            description_label_font_size         font size for track state label
            placeholder_font_size               font size for cell placeholder
            cell_height                         height of all cells
            interval_between_cells              vertical space between cells
            railway_station_caption_position    position of "Railway station" label
            environment_caption_position        position of "Environment" label
            caption_font_size                   "Railway station" and "Environment" font size
            constructor_opacity                 general opacity of the constructor screen
            railway_station_caption_sprite      label for "Railway station" string
            environment_caption_sprite          label for "Environment" string
            track_state_matrix                  table with all tracks state properties:
                                                property #0 indicates if track is locked
                                                property #1 indicates if track is under construction
                                                property #2 indicates construction time left
                                                property #3 indicates if unlock condition from level is met
                                                property #4 indicates if unlock condition from previous track is met
                                                property #5 indicates if unlock condition from environment is met
                                                property #6 indicates if all unlock conditions are met
                                                property #7 indicates track price
                                                property #8 indicates required level for this track
                                                property #9 indicates required environment tier for this track
            environment_state_matrix            table with all environment state properties:
                                                property #0 indicates if environment is locked
                                                property #1 indicates if environment is under construction
                                                property #2 indicates construction time left
                                                property #3 indicates if unlock condition from level is met
                                                property #4 indicates if unlock condition from previous env. is met
                                                property #5 is reserved
                                                property #6 indicates if all unlock conditions are met
                                                property #7 indicates environment price
                                                property #8 indicates required level for this environment
            locked_tracks_labels                list of "locked" labels for tracks
            locked_tiers_labels                 list of "locked" labels for environment tiers
            title_tracks_labels                 list of "Track X" labels
            title_tiers_labels                  list of "Tier X" labels
            description_tracks_labels           list of track state labels
            description_tiers_labels            list of environment tiers state labels
            build_track_button                  button which puts track under construction
            set_track_money_target_button       SetTrackMoneyTargetButton object
            reset_track_money_target_button     ResetTrackMoneyTargetButton object
            no_more_tracks_available_labels     list of "No more tracks available" labels
            no_more_tiers_available_labels      list of "No more tiers available" labels
            close_constructor_button            CloseConstructorButton object
            buttons                             list of all buttons
            on_buy_track                        on_click handler for buy track button
            money                               player bank account state
            track_money_target_activated        indicates if user tracks money target for upcoming station track
            feature_unlocked_notification_enabled
                                indicates if feature unlocked notifications are enabled by user in game settings
            construction_completed_notification_enabled
                                indicates if construction completed notifications are enabled by user in game settings

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        def on_close_constructor(button):
            """
            Notifies controller that player has closed constructor screen.

            :param button:                      button that was clicked
            """
            self.controller.on_deactivate_view()

        def on_buy_track(button):
            """
            Removes buy track button and its handlers. Resets money target and removes money target buttons.
            Notifies controller that player has bought the track.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.set_track_money_target_button.on_deactivate()
            self.reset_track_money_target_button.on_deactivate()
            self.controller.on_deactivate_track_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(0)
            self.controller.on_put_track_under_construction(min(list(self.track_state_matrix.keys())))

        def on_set_track_money_target(button):
            """
            Sets money target value so user can see how much money left for purchase.
            Switches money target button state.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_activate_track_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(
                self.track_state_matrix[min(list(self.track_state_matrix.keys()))][PRICE]
            )

        def on_reset_track_money_target(button):
            """
            Resets money target value. Switches money target button state.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_deactivate_track_money_target()
            self.controller.parent_controller.parent_controller.on_update_money_target(0)

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.map.constructor.view'))
        self.track_cells_positions = ()
        self.environment_cell_positions = ()
        self.locked_label_offset = [0, 0]
        self.track_build_button_offset = [0, 0]
        self.title_label_offset = [0, 0]
        self.description_label_offset = [0, 0]
        self.placeholder_offset = [0, 0]
        self.locked_label_font_size = 0
        self.title_label_font_size = 0
        self.description_label_font_size = 0
        self.placeholder_font_size = 0
        self.cell_height = 0
        self.interval_between_cells = 0
        self.railway_station_caption_position = [0, 0]
        self.environment_caption_position = [0, 0]
        self.caption_font_size = 0
        self.on_read_ui_info()
        self.constructor_opacity = 0
        self.railway_station_caption_sprite = None
        self.environment_caption_sprite = None
        self.track_state_matrix = None
        self.environment_state_matrix = None
        self.locked_tracks_labels = {}
        self.locked_tiers_labels = {}
        self.title_tracks_labels = {}
        self.title_tiers_labels = {}
        self.description_tracks_labels = {}
        self.description_tiers_labels = {}
        self.build_track_button = BuildTrackButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                   groups=self.groups, on_click_action=on_buy_track)
        self.set_track_money_target_button, self.reset_track_money_target_button \
            = create_two_state_button(SetTrackMoneyTargetButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                                groups=self.groups,
                                                                on_click_action=on_set_track_money_target),
                                      ResetTrackMoneyTargetButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                                  groups=self.groups,
                                                                  on_click_action=on_reset_track_money_target))
        self.no_more_tracks_available_labels = []
        self.no_more_tiers_available_labels = []
        self.close_constructor_button = CloseConstructorButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                               groups=self.groups, on_click_action=on_close_constructor)
        self.buttons.append(self.close_constructor_button)
        self.buttons.append(self.build_track_button)
        self.buttons.append(self.set_track_money_target_button)
        self.buttons.append(self.reset_track_money_target_button)
        self.money = 0.0
        self.user_db_cursor.execute('SELECT track_money_target_activated FROM graphics')
        self.track_money_target_activated = bool(self.user_db_cursor.fetchone()[0])
        self.user_db_cursor.execute('''SELECT feature_unlocked_notification_enabled, 
                                       construction_completed_notification_enabled FROM notification_settings''')
        self.feature_unlocked_notification_enabled, self.construction_completed_notification_enabled \
            = self.user_db_cursor.fetchone()
        self.feature_unlocked_notification_enabled = bool(self.feature_unlocked_notification_enabled)
        self.construction_completed_notification_enabled = bool(self.construction_completed_notification_enabled)

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
        for d in self.locked_tracks_labels:
            self.locked_tracks_labels[d].delete()

        self.locked_tracks_labels.clear()
        for d in self.title_tracks_labels:
            self.title_tracks_labels[d].delete()

        self.title_tracks_labels.clear()
        for d in self.description_tracks_labels:
            self.description_tracks_labels[d].delete()

        self.description_tracks_labels.clear()
        for label in self.no_more_tracks_available_labels:
            label.delete()

        self.no_more_tracks_available_labels.clear()
        for label in self.no_more_tiers_available_labels:
            label.delete()

        self.no_more_tiers_available_labels.clear()
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

            # add "No more tracks available" label if number of available tracks is less than 4
            dictionary_keys = list(self.track_state_matrix.keys())
            available_options = min(len(dictionary_keys), 4)
            if available_options < 4 and len(self.no_more_tracks_available_labels) < 4 - available_options:
                position_index = available_options + len(self.no_more_tracks_available_labels)
                self.no_more_tracks_available_labels.append(
                    Label(I18N_RESOURCES['no_more_tracks_available_placeholder_string'][self.current_locale],
                          font_name='Arial', font_size=self.placeholder_font_size, color=GREY,
                          x=self.track_cells_positions[position_index][0] + self.placeholder_offset[0],
                          y=self.track_cells_positions[position_index][1] + self.placeholder_offset[1],
                          anchor_x='center', anchor_y='center',
                          batch=self.batches['ui_batch'], group=self.groups['button_text'])
                )

            for i in range(available_options):
                # create new cell if there are more tracks available;
                # only 1 cell is created every frame for performance reasons
                if dictionary_keys[i] not in self.locked_tracks_labels:
                    # if track is unlocked and not enough money, create disabled construction label;
                    # if player has enough money, create button to buy the track
                    if self.track_state_matrix[dictionary_keys[i]][UNLOCK_AVAILABLE]:
                        if self.track_money_target_activated:
                            self.reset_track_money_target_button.on_activate()
                        else:
                            self.set_track_money_target_button.on_activate()

                        if self.money < self.track_state_matrix[dictionary_keys[i]][PRICE]:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label('', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                            self.build_track_button.on_deactivate()

                        else:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label(' ', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                            self.build_track_button.on_activate()

                    # if track is not available, create locked label if track is not under construction
                    else:
                        if not self.track_state_matrix[dictionary_keys[i]][UNDER_CONSTRUCTION]:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label('', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                        else:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label(' ', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])

                    # create track cell title and description
                    self.title_tracks_labels[dictionary_keys[i]] \
                        = Label(I18N_RESOURCES['title_track_string'][self.current_locale].format(dictionary_keys[i]),
                                font_name='Arial', font_size=self.title_label_font_size,
                                x=self.track_cells_positions[i][0] + self.title_label_offset[0],
                                y=self.track_cells_positions[i][1] + self.title_label_offset[1],
                                anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                group=self.groups['button_text'])
                    if self.track_state_matrix[dictionary_keys[i]][UNLOCK_AVAILABLE]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label(I18N_RESOURCES['unlock_available_track_description_string'][self.current_locale]
                                    .format(self.track_state_matrix[dictionary_keys[i]][PRICE]).replace(',', ' '),
                                    font_name='Arial', font_size=self.description_label_font_size,
                                    color=GREEN,
                                    x=self.track_cells_positions[i][0] + self.description_label_offset[0],
                                    y=self.track_cells_positions[i][1] + self.description_label_offset[1],
                                    anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                    group=self.groups['button_text'])
                    elif self.track_state_matrix[dictionary_keys[i]][UNDER_CONSTRUCTION]:
                        construction_time = self.track_state_matrix[dictionary_keys[i]][CONSTRUCTION_TIME]
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label(I18N_RESOURCES['under_construction_track_description_string'][self.current_locale]
                                    .format(construction_time // FRAMES_IN_ONE_HOUR,
                                            (construction_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR),
                                    font_name='Arial', font_size=self.description_label_font_size,
                                    color=ORANGE,
                                    x=self.track_cells_positions[i][0] + self.description_label_offset[0],
                                    y=self.track_cells_positions[i][1] + self.description_label_offset[1],
                                    anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                    group=self.groups['button_text'])
                    else:
                        if not self.track_state_matrix[dictionary_keys[i]][UNLOCK_CONDITION_FROM_LEVEL]:
                            self.description_tracks_labels[dictionary_keys[i]] \
                                = Label(I18N_RESOURCES[
                                            'unlock_condition_from_level_track_description_string'
                                        ][self.current_locale]
                                        .format(self.track_state_matrix[dictionary_keys[i]][LEVEL_REQUIRED]),
                                        font_name='Arial', font_size=self.description_label_font_size, color=GREY,
                                        x=self.track_cells_positions[i][0]
                                          + self.description_label_offset[0],
                                        y=self.track_cells_positions[i][1]
                                          + self.description_label_offset[1],
                                        anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                        elif not self.track_state_matrix[dictionary_keys[i]][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                            self.description_tracks_labels[dictionary_keys[i]] \
                                = Label(I18N_RESOURCES[
                                            'unlock_condition_from_environment_track_description_string'
                                        ][self.current_locale]
                                        .format(self.track_state_matrix[dictionary_keys[i]][ENVIRONMENT_REQUIRED]),
                                        font_name='Arial', font_size=self.description_label_font_size, color=GREY,
                                        x=self.track_cells_positions[i][0]
                                          + self.description_label_offset[0],
                                        y=self.track_cells_positions[i][1]
                                          + self.description_label_offset[1],
                                        anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                        elif not self.track_state_matrix[dictionary_keys[i]][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
                            self.description_tracks_labels[dictionary_keys[i]] \
                                = Label(I18N_RESOURCES[
                                            'unlock_condition_from_previous_track_track_description_string'
                                        ][self.current_locale].format(dictionary_keys[i] - 1),
                                        font_name='Arial', font_size=self.description_label_font_size, color=GREY,
                                        x=self.track_cells_positions[i][0]
                                          + self.description_label_offset[0],
                                        y=self.track_cells_positions[i][1]
                                          + self.description_label_offset[1],
                                        anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])

                    break

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

            dictionary_keys = list(self.locked_tracks_labels.keys())
            for i in range(len(dictionary_keys)):
                self.locked_tracks_labels[dictionary_keys[i]].x \
                    = self.track_cells_positions[i][0] + self.locked_label_offset[0]
                self.locked_tracks_labels[dictionary_keys[i]].y \
                    = self.track_cells_positions[i][1] + self.locked_label_offset[1]
                self.locked_tracks_labels[dictionary_keys[i]].font_size = self.locked_label_font_size
                self.title_tracks_labels[dictionary_keys[i]].x \
                    = self.track_cells_positions[i][0] + self.title_label_offset[0]
                self.title_tracks_labels[dictionary_keys[i]].y \
                    = self.track_cells_positions[i][1] + self.title_label_offset[1]
                self.title_tracks_labels[dictionary_keys[i]].font_size = self.title_label_font_size
                self.description_tracks_labels[dictionary_keys[i]].x \
                    = self.track_cells_positions[i][0] + self.description_label_offset[0]
                self.description_tracks_labels[dictionary_keys[i]].y \
                    = self.track_cells_positions[i][1] + self.description_label_offset[1]
                self.description_tracks_labels[dictionary_keys[i]].font_size \
                    = self.description_label_font_size

        self.build_track_button.x_margin = self.track_cells_positions[0][0] + self.track_build_button_offset[0]
        self.build_track_button.y_margin = self.track_cells_positions[0][1] + self.track_build_button_offset[1]
        self.build_track_button.on_size_changed((self.cell_height, self.cell_height),
                                                self.locked_label_font_size)
        self.set_track_money_target_button.x_margin = self.track_cells_positions[0][0] \
                                                    + self.track_build_button_offset[0] - self.cell_height + 2
        self.set_track_money_target_button.y_margin = self.track_cells_positions[0][1] \
                                                    + self.track_build_button_offset[1]
        self.set_track_money_target_button.on_size_changed((self.cell_height, self.cell_height),
                                                           self.locked_label_font_size)
        self.reset_track_money_target_button.x_margin = self.track_cells_positions[0][0] \
                                                      + self.track_build_button_offset[0] - self.cell_height + 2
        self.reset_track_money_target_button.y_margin = self.track_cells_positions[0][1] \
                                                      + self.track_build_button_offset[1]
        self.reset_track_money_target_button.on_size_changed((self.cell_height, self.cell_height),
                                                             int(24 * self.locked_label_font_size / 40))
        self.close_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                      int(self.close_constructor_button.base_font_size_property
                                                          * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_money(self, money, track_state_matrix, environment_state_matrix):
        """
        Updates bank account state change when user spends or gains money.

        :param money:                           current bank account state
        :param track_state_matrix               table with all tracks state properties
        :param environment_state_matrix         table with all environment state properties
        """
        self.money = money
        self.track_state_matrix = track_state_matrix
        self.environment_state_matrix = environment_state_matrix
        if len(self.track_state_matrix) > 0:
            self.on_update_live_track_state(track_state_matrix, min(list(track_state_matrix.keys())))

        if len(self.environment_state_matrix) > 0:
            self.on_update_live_environment_state(environment_state_matrix, min(list(environment_state_matrix.keys())))

    @view_is_active
    @track_cell_is_created
    def on_update_live_track_state(self, track_state_matrix, track):
        """
        Updates track state when constructor screen is opened and track cell has been created.

        :param track_state_matrix       table with all tracks state properties
        :param track:                   track number
        """
        self.track_state_matrix = track_state_matrix
        if track_state_matrix[track][UNLOCK_AVAILABLE]:
            if self.track_money_target_activated:
                self.reset_track_money_target_button.on_activate()
            else:
                self.set_track_money_target_button.on_activate()

            if self.money < track_state_matrix[track][PRICE]:
                self.locked_tracks_labels[track].text = ''
                self.build_track_button.on_deactivate()
            else:
                self.locked_tracks_labels[track].text = ' '
                self.build_track_button.on_activate()

        else:
            self.set_track_money_target_button.on_deactivate()
            self.reset_track_money_target_button.on_deactivate()
            if not track_state_matrix[track][UNDER_CONSTRUCTION]:
                self.locked_tracks_labels[track].text = ''
            else:
                self.locked_tracks_labels[track].text = ' '

        if track_state_matrix[track][UNLOCK_AVAILABLE]:
            self.description_tracks_labels[track].text \
                = I18N_RESOURCES['unlock_available_track_description_string'][self.current_locale]\
                .format(track_state_matrix[track][PRICE]).replace(',', ' ')
            self.description_tracks_labels[track].color = GREEN
        elif track_state_matrix[track][UNDER_CONSTRUCTION]:
            construction_time = track_state_matrix[track][CONSTRUCTION_TIME]
            self.description_tracks_labels[track].text \
                = I18N_RESOURCES['under_construction_track_description_string'][self.current_locale]\
                .format(construction_time // FRAMES_IN_ONE_HOUR,
                        (construction_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
            self.description_tracks_labels[track].color = ORANGE
        else:
            if not track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL]:
                self.description_tracks_labels[track].text \
                    = I18N_RESOURCES['unlock_condition_from_level_track_description_string'][self.current_locale]\
                    .format(track_state_matrix[track][LEVEL_REQUIRED])
                self.description_tracks_labels[track].color = GREY
            elif not track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                self.description_tracks_labels[track].text \
                    = I18N_RESOURCES['unlock_condition_from_environment_track_description_string'][self.current_locale]\
                    .format(0)
                self.description_tracks_labels[track].color = GREY
            elif not track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
                self.description_tracks_labels[track].text \
                    = I18N_RESOURCES[
                    'unlock_condition_from_previous_track_track_description_string'
                ][self.current_locale].format(track - 1)
                self.description_tracks_labels[track].color = GREY

    def on_update_track_state(self, track_state_matrix, game_time):
        """
        Updates track state matrix every frame in case cell for this track is not yet created.

        :param track_state_matrix       table with all tracks state properties
        :param game_time:               current in-game time
        """
        self.track_state_matrix = track_state_matrix

    def on_update_environment_state(self, environment_state_matrix, game_time):
        """
        Updates environment state matrix every frame in case cell for this track is not yet created.

        :param environment_state_matrix         table with all environment state properties
        :param game_time:                       current in-game time
        """
        self.environment_state_matrix = environment_state_matrix

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
