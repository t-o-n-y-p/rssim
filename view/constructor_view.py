from logging import getLogger

from pyglet.text import Label

from view import *
from button.close_constructor_button import CloseConstructorButton
from button.build_track_button import BuildTrackButton


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
            locked_tracks_labels                list of "locked" labels for tracks
            title_tracks_labels                 list of "Track X" labels
            description_tracks_labels           list of track state labels
            build_track_button                  button which puts track under construction
            no_more_tracks_available_labels     list of "No more tracks available" labels
            coming_soon_environment_labels      list of "Coming soon" labels
            close_constructor_button            CloseConstructorButton object
            buttons                             list of all buttons
            on_buy_track                        on_click handler for buy track button
            money                               player bank account state

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
            Removes buy track button and its handlers.
            Notifies controller that player has bought the track.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.on_put_track_under_construction(min(list(self.track_state_matrix.keys())))

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
        self.locked_tracks_labels = {}
        self.title_tracks_labels = {}
        self.description_tracks_labels = {}
        self.build_track_button = BuildTrackButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                   groups=self.groups, on_click_action=on_buy_track)
        self.build_track_button.x_margin = self.track_cells_positions[0][0] + self.track_build_button_offset[0]
        self.build_track_button.y_margin = self.track_cells_positions[0][1] + self.track_build_button_offset[1]
        self.build_track_button.on_position_changed((self.build_track_button.x_margin,
                                                     self.build_track_button.y_margin))
        self.build_track_button.on_size_changed((self.cell_height, self.cell_height),
                                                self.locked_label_font_size)
        self.no_more_tracks_available_labels = []
        self.coming_soon_environment_labels = []
        self.close_constructor_button = CloseConstructorButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                               groups=self.groups, on_click_action=on_close_constructor)
        self.buttons.append(self.close_constructor_button)
        self.buttons.append(self.build_track_button)
        self.money = 0.0

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.is_activated = True
        self.railway_station_caption_sprite \
            = Label('R a i l w a y   s t a t i o n', font_name='Arial', font_size=self.caption_font_size,
                    x=self.railway_station_caption_position[0],
                    y=self.railway_station_caption_position[1],
                    anchor_x='center', anchor_y='center',
                    batch=self.batches['ui_batch'], group=self.groups['button_text'])
        self.environment_caption_sprite \
            = Label('E n v i r o n m e n t', font_name='Arial', font_size=self.caption_font_size,
                    x=self.environment_caption_position[0],
                    y=self.environment_caption_position[1],
                    anchor_x='center', anchor_y='center',
                    batch=self.batches['ui_batch'], group=self.groups['button_text'])
        # create "Coming soon" labels for environment since it is not yet implemented
        for i in range(4):
            self.coming_soon_environment_labels.append(
                Label('Coming soon', font_name='Arial', font_size=self.placeholder_font_size,
                      color=GREY,
                      x=self.environment_cell_positions[i][0] + self.placeholder_offset[0],
                      y=self.environment_cell_positions[i][1] + self.placeholder_offset[1],
                      anchor_x='center', anchor_y='center',
                      batch=self.batches['ui_batch'], group=self.groups['button_text'])
            )

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
        for label in self.coming_soon_environment_labels:
            label.delete()

        self.coming_soon_environment_labels.clear()
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
                    Label('No more tracks available', font_name='Arial',
                          font_size=self.placeholder_font_size,
                          color=GREY,
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
                        if self.money < self.track_state_matrix[dictionary_keys[i]][PRICE]:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label('', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                            if dictionary_keys[i] == min(list(self.track_state_matrix.keys())):
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
                        = Label(f'Track {dictionary_keys[i]}', font_name='Arial',
                                font_size=self.title_label_font_size,
                                x=self.track_cells_positions[i][0] + self.title_label_offset[0],
                                y=self.track_cells_positions[i][1] + self.title_label_offset[1],
                                anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                group=self.groups['button_text'])
                    if self.track_state_matrix[dictionary_keys[i]][UNLOCK_AVAILABLE]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Available for {} ¤'
                                    .format(self.track_state_matrix[dictionary_keys[i]][PRICE]),
                                    font_name='Arial', font_size=self.description_label_font_size,
                                    color=GREEN,
                                    x=self.track_cells_positions[i][0] + self.description_label_offset[0],
                                    y=self.track_cells_positions[i][1] + self.description_label_offset[1],
                                    anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                    group=self.groups['button_text'])
                    elif self.track_state_matrix[dictionary_keys[i]][UNDER_CONSTRUCTION]:
                        construction_time = self.track_state_matrix[dictionary_keys[i]][CONSTRUCTION_TIME]
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Under construction. {}h {}min left'
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
                                = Label('Requires level {}'
                                        .format(self.track_state_matrix[dictionary_keys[i]][LEVEL_REQUIRED]),
                                        font_name='Arial', font_size=self.description_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0]
                                          + self.description_label_offset[0],
                                        y=self.track_cells_positions[i][1]
                                          + self.description_label_offset[1],
                                        anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                        elif not self.track_state_matrix[dictionary_keys[i]][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                            self.description_tracks_labels[dictionary_keys[i]] \
                                = Label('Requires environment Tier X',
                                        font_name='Arial', font_size=self.description_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0]
                                          + self.description_label_offset[0],
                                        y=self.track_cells_positions[i][1]
                                          + self.description_label_offset[1],
                                        anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                        elif not self.track_state_matrix[dictionary_keys[i]][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
                            self.description_tracks_labels[dictionary_keys[i]] \
                                = Label('Build track {} to unlock'.format(dictionary_keys[i] - 1),
                                        font_name='Arial', font_size=self.description_label_font_size,
                                        color=GREY,
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
            for i in range(4):
                self.coming_soon_environment_labels[i].x \
                    = self.environment_cell_positions[i][0] + self.placeholder_offset[0]
                self.coming_soon_environment_labels[i].y \
                    = self.environment_cell_positions[i][1] + self.placeholder_offset[1]
                self.coming_soon_environment_labels[i].font_size = self.placeholder_font_size

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
        self.build_track_button.on_position_changed((self.build_track_button.x_margin,
                                                     self.build_track_button.y_margin))
        self.build_track_button.on_size_changed((self.cell_height, self.cell_height),
                                                self.locked_label_font_size)

        self.close_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                      int(24 / 80 * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_update_money(self, money, track_state_matrix):
        """
        Updates bank account state change when user spends or gains money.

        :param money:                   current bank account state
        :param track_state_matrix       table with all tracks state properties
        """
        self.money = money
        self.track_state_matrix = track_state_matrix
        if len(self.track_state_matrix) > 0:
            self.on_update_live_track_state(track_state_matrix, list(track_state_matrix.keys())[0])

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
            if self.money < track_state_matrix[track][PRICE]:
                self.locked_tracks_labels[track].text = ''
                if track == min(list(self.track_state_matrix.keys())):
                    self.build_track_button.on_deactivate()
            else:
                self.locked_tracks_labels[track].text = ' '
                self.build_track_button.on_activate()

        else:
            if not track_state_matrix[track][UNDER_CONSTRUCTION]:
                self.locked_tracks_labels[track].text = ''
            else:
                self.locked_tracks_labels[track].text = ' '

        if track_state_matrix[track][UNLOCK_AVAILABLE]:
            self.description_tracks_labels[track].text = 'Available for {} ¤'\
                                                         .format(track_state_matrix[track][PRICE])
            self.description_tracks_labels[track].color = GREEN
        elif track_state_matrix[track][UNDER_CONSTRUCTION]:
            construction_time = track_state_matrix[track][CONSTRUCTION_TIME]
            self.description_tracks_labels[track].text \
                = 'Under construction. {}h {}min left'\
                  .format(construction_time // FRAMES_IN_ONE_HOUR,
                          (construction_time // FRAMES_IN_ONE_MINUTE) % MINUTES_IN_ONE_HOUR)
            self.description_tracks_labels[track].color = ORANGE
        else:
            if not track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL]:
                self.description_tracks_labels[track].text = 'Requires level {}'\
                                                             .format(track_state_matrix[track][LEVEL_REQUIRED])
                self.description_tracks_labels[track].color = GREY
            elif not track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]:
                self.description_tracks_labels[track].text = 'Requires environment Tier X'
                self.description_tracks_labels[track].color = GREY
            elif not track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]:
                self.description_tracks_labels[track].text = 'Build track {} to unlock'.format(track - 1)
                self.description_tracks_labels[track].color = GREY

    def on_update_track_state(self, track_state_matrix, game_time):
        """
        Updates track state matrix every frame in case cell for this track is not yet created.

        :param track_state_matrix       table with all tracks state properties
        :param game_time:               current in-game time
        """
        self.track_state_matrix = track_state_matrix

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
