from logging import getLogger

from pyglet.text import Label

from view import *
from button.close_constructor_button import CloseConstructorButton
from button.buy_track_button import BuyTrackButton


class ConstructorView(View):
    """
    Implements Constructor view.
    Constructor object is responsible for building new tracks and station environment.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_close_constructor                    on_click handler for close constructor button
            on_buy_track                            on_click handler for buy track button

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
            buy_buttons                         list of buy track buttons
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
            self.logger.info('START ON_CLOSE_CONSTRUCTOR')
            self.controller.on_deactivate_view()
            self.logger.info('END ON_CLOSE_CONSTRUCTOR')

        def on_buy_track(button):
            """
            Removes buy track button and its handlers.
            Notifies controller that player has bought the track.

            :param button:                      button that was clicked
            """
            self.logger.info('START ON_BUY_TRACK')
            button.on_deactivate()
            key_to_remove = None
            for key, value in self.buy_buttons.items():
                if value == button:
                    key_to_remove = key
                    self.logger.debug(f'key_to_remove: {key_to_remove}')
                    self.controller.on_put_track_under_construction(key)

            self.controller.on_detach_handlers(
                on_mouse_motion_handlers=[self.buy_buttons[key_to_remove].handle_mouse_motion, ],
                on_mouse_press_handlers=[self.buy_buttons[key_to_remove].handle_mouse_press, ],
                on_mouse_release_handlers=[self.buy_buttons[key_to_remove].handle_mouse_release, ],
                on_mouse_leave_handlers=[self.buy_buttons[key_to_remove].handle_mouse_leave, ]
            )
            self.logger.debug(f'buy_buttons: {self.buy_buttons.keys()}')
            self.logger.debug(f'number of buttons: {len(self.buttons)}')
            self.buttons.remove(self.buy_buttons.pop(key_to_remove))
            self.logger.debug(f'buy_buttons: {self.buy_buttons.keys()}')
            self.logger.debug(f'number of buttons: {len(self.buttons)}')
            self.logger.info('END ON_BUY_TRACK')

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.map.constructor.view'))
        self.logger.info('START INIT')
        self.track_cells_positions = ()
        self.environment_cell_positions = ()
        self.locked_label_offset = [0, 0]
        self.buy_button_offset = [0, 0]
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
        self.buy_buttons = {}
        self.no_more_tracks_available_labels = []
        self.coming_soon_environment_labels = []
        self.close_constructor_button = CloseConstructorButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                               groups=self.groups, on_click_action=on_close_constructor)
        self.logger.debug('buttons created successfully')
        self.buttons.append(self.close_constructor_button)
        self.logger.debug(f'buttons list length: {len(self.buttons)}')
        self.on_buy_track = on_buy_track
        self.money = 0.0
        self.logger.info('END INIT')

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates sprites and labels.
        """
        self.logger.info('START ON_ACTIVATE')
        self.is_activated = True
        self.logger.debug(f'is activated: {self.is_activated}')
        self.railway_station_caption_sprite \
            = Label('R a i l w a y   s t a t i o n', font_name='Arial', font_size=self.caption_font_size,
                    x=self.railway_station_caption_position[0],
                    y=self.railway_station_caption_position[1],
                    anchor_x='center', anchor_y='center',
                    batch=self.batches['ui_batch'], group=self.groups['button_text'])
        self.logger.debug(f'railway_station_caption_sprite position: {self.railway_station_caption_position}')
        self.logger.debug(f'railway_station_caption_sprite font size: {self.caption_font_size}')
        self.environment_caption_sprite \
            = Label('E n v i r o n m e n t', font_name='Arial', font_size=self.caption_font_size,
                    x=self.environment_caption_position[0],
                    y=self.environment_caption_position[1],
                    anchor_x='center', anchor_y='center',
                    batch=self.batches['ui_batch'], group=self.groups['button_text'])
        self.logger.debug(f'environment_caption_sprite position: {self.environment_caption_position}')
        self.logger.debug(f'environment_caption_sprite font size: {self.caption_font_size}')
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
            self.logger.debug('coming_soon_environment_labels {} position: {}'
                              .format(i, (self.environment_cell_positions[i][0] + self.placeholder_offset[0],
                                          self.environment_cell_positions[i][1] + self.placeholder_offset[1])))
            self.logger.debug(f'coming_soon_environment_labels {i} font size: {self.placeholder_font_size}')

        for b in self.buttons:
            self.logger.debug(f'button: {b.__class__.__name__}')
            self.logger.debug(f'to_activate_on_controller_init: {b.to_activate_on_controller_init}')
            if b.to_activate_on_controller_init:
                b.on_activate()

        self.logger.info('END ON_ACTIVATE')

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and destroys all sprites and labels.
        """
        self.logger.info('START ON_DEACTIVATE')
        self.is_activated = False
        self.logger.debug(f'is activated: {self.is_activated}')
        self.railway_station_caption_sprite.delete()
        self.railway_station_caption_sprite = None
        self.logger.debug(f'railway_station_caption_sprite: {self.railway_station_caption_sprite}')
        self.environment_caption_sprite.delete()
        self.environment_caption_sprite = None
        self.logger.debug(f'environment_caption_sprite: {self.environment_caption_sprite}')
        for label in self.coming_soon_environment_labels:
            label.delete()

        self.coming_soon_environment_labels.clear()
        self.logger.debug(f'coming_soon_environment_labels: {self.coming_soon_environment_labels}')
        for d in self.locked_tracks_labels:
            self.locked_tracks_labels[d].delete()

        self.locked_tracks_labels.clear()
        self.logger.debug(f'locked_tracks_labels: {self.locked_tracks_labels}')
        for d in self.title_tracks_labels:
            self.title_tracks_labels[d].delete()

        self.title_tracks_labels.clear()
        self.logger.debug(f'title_tracks_labels: {self.title_tracks_labels}')
        for d in self.description_tracks_labels:
            self.description_tracks_labels[d].delete()

        self.description_tracks_labels.clear()
        self.logger.debug(f'description_tracks_labels: {self.description_tracks_labels}')
        for label in self.no_more_tracks_available_labels:
            label.delete()

        self.no_more_tracks_available_labels.clear()
        self.logger.debug(f'no_more_tracks_available_labels: {self.no_more_tracks_available_labels}')
        for b in self.buttons:
            b.on_deactivate()

        self.logger.debug(f'number of buttons: {len(self.buttons)}')
        for key in self.buy_buttons:
            self.controller.on_detach_handlers(
                on_mouse_motion_handlers=[self.buy_buttons[key].handle_mouse_motion, ],
                on_mouse_press_handlers=[self.buy_buttons[key].handle_mouse_press, ],
                on_mouse_release_handlers=[self.buy_buttons[key].handle_mouse_release, ],
                on_mouse_leave_handlers=[self.buy_buttons[key].handle_mouse_leave, ]
            )
            self.buttons.remove(self.buy_buttons[key])

        self.logger.debug(f'number of buttons: {len(self.buttons)}')
        self.buy_buttons.clear()
        self.logger.debug(f'buy_buttons: {self.buy_buttons}')
        self.logger.info('END ON_DEACTIVATE')

    def on_update(self):
        """
        Updates fade-in/fade-out animations and create sprites if some are missing.
        Not all sprites are created at once, they are created one by one to avoid massive FPS drop.
        """
        self.logger.info('START ON_UPDATE')
        if self.is_activated:
            self.logger.debug(f'constructor_opacity: {self.constructor_opacity}')
            if self.constructor_opacity < 255:
                self.constructor_opacity += 15

            # add "No more tracks available" label if number of available tracks is less than 4
            dictionary_keys = list(self.track_state_matrix.keys())
            self.logger.debug(f'dictionary_keys: {dictionary_keys}')
            available_options = min(len(dictionary_keys), 4)
            self.logger.debug(f'available_options: {available_options}')
            if available_options < 4 and len(self.no_more_tracks_available_labels) < 4 - available_options:
                position_index = available_options + len(self.no_more_tracks_available_labels)
                self.logger.debug(f'available_options: {available_options}')
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
                self.logger.debug(f'locked_tracks_labels: {self.locked_tracks_labels.keys()}')
                self.logger.debug(f'next track: {dictionary_keys[i]}')
                if dictionary_keys[i] not in self.locked_tracks_labels:
                    self.logger.debug('unlock_available: {}'
                                      .format(self.track_state_matrix[dictionary_keys[i]][UNLOCK_AVAILABLE]))
                    # if track is unlocked and not enough money, create disabled construction label;
                    # if player has enough money, create button to buy the track
                    if self.track_state_matrix[dictionary_keys[i]][UNLOCK_AVAILABLE]:
                        self.logger.debug(f'money: {self.money}')
                        self.logger.debug(f'price: {self.track_state_matrix[dictionary_keys[i]][PRICE]}')
                        if self.money < self.track_state_matrix[dictionary_keys[i]][PRICE]:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label('', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                            self.logger.debug('locked label text: {}'
                                              .format(self.locked_tracks_labels[dictionary_keys[i]].text))
                            self.logger.debug('locked label position: {}'
                                              .format((self.locked_tracks_labels[dictionary_keys[i]].x,
                                                       self.locked_tracks_labels[dictionary_keys[i]].y)))
                            self.logger.debug('locked label font size: {}'
                                              .format(self.locked_tracks_labels[dictionary_keys[i]].font_size))
                        else:
                            self.locked_tracks_labels[dictionary_keys[i]] \
                                = Label(' ', font_name='Webdings', font_size=self.locked_label_font_size,
                                        color=GREY,
                                        x=self.track_cells_positions[i][0] + self.locked_label_offset[0],
                                        y=self.track_cells_positions[i][1] + self.locked_label_offset[1],
                                        anchor_x='center', anchor_y='center', batch=self.batches['ui_batch'],
                                        group=self.groups['button_text'])
                            self.logger.debug('locked label text: {}'
                                              .format(self.locked_tracks_labels[dictionary_keys[i]].text))
                            self.logger.debug('locked label position: {}'
                                              .format((self.locked_tracks_labels[dictionary_keys[i]].x,
                                                       self.locked_tracks_labels[dictionary_keys[i]].y)))
                            self.logger.debug('locked label font size: {}'
                                              .format(self.locked_tracks_labels[dictionary_keys[i]].font_size))
                            self.buy_buttons[dictionary_keys[i]] \
                                = BuyTrackButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                 groups=self.groups, on_click_action=self.on_buy_track)
                            self.buy_buttons[dictionary_keys[i]].x_margin \
                                = self.track_cells_positions[i][0] + self.buy_button_offset[0]
                            self.buy_buttons[dictionary_keys[i]].y_margin \
                                = self.track_cells_positions[i][1] + self.buy_button_offset[1]
                            self.buy_buttons[dictionary_keys[i]].on_position_changed(
                                (self.buy_buttons[dictionary_keys[i]].x_margin,
                                 self.buy_buttons[dictionary_keys[i]].y_margin)
                            )
                            self.buy_buttons[dictionary_keys[i]] \
                                .on_size_changed((self.cell_height, self.cell_height),
                                                 self.locked_label_font_size)
                            self.logger.debug(f'buttons list length: {len(self.buttons)}')
                            self.buttons.append(self.buy_buttons[dictionary_keys[i]])
                            self.logger.debug(f'buttons list length: {len(self.buttons)}')
                            self.buy_buttons[dictionary_keys[i]].on_activate()
                            self.controller.on_append_handlers(
                                on_mouse_motion_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_motion, ],
                                on_mouse_press_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_press, ],
                                on_mouse_release_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_release, ],
                                on_mouse_leave_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_leave, ]
                            )

                    # if track is not available, create locked label if track is not under construction
                    else:
                        self.logger.debug('under_construction: {}'
                                          .format(self.track_state_matrix[dictionary_keys[i]][UNDER_CONSTRUCTION]))
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

                        self.logger.debug('locked label text: {}'
                                          .format(self.locked_tracks_labels[dictionary_keys[i]].text))
                        self.logger.debug('locked label position: {}'
                                          .format((self.locked_tracks_labels[dictionary_keys[i]].x,
                                                   self.locked_tracks_labels[dictionary_keys[i]].y)))
                        self.logger.debug('locked label font size: {}'
                                          .format(self.locked_tracks_labels[dictionary_keys[i]].font_size))

                    # create track cell title and description
                    self.title_tracks_labels[dictionary_keys[i]] \
                        = Label(f'Track {dictionary_keys[i]}', font_name='Arial',
                                font_size=self.title_label_font_size,
                                x=self.track_cells_positions[i][0] + self.title_label_offset[0],
                                y=self.track_cells_positions[i][1] + self.title_label_offset[1],
                                anchor_x='left', anchor_y='center', batch=self.batches['ui_batch'],
                                group=self.groups['button_text'])
                    self.logger.debug('title label text: {}'
                                      .format(self.title_tracks_labels[dictionary_keys[i]].text))
                    self.logger.debug('title label position: {}'
                                      .format((self.title_tracks_labels[dictionary_keys[i]].x,
                                               self.title_tracks_labels[dictionary_keys[i]].y)))
                    self.logger.debug('title label font size: {}'
                                      .format(self.title_tracks_labels[dictionary_keys[i]].font_size))

                    self.logger.debug('unlock_available: {}'
                                      .format(self.track_state_matrix[dictionary_keys[i]][UNLOCK_AVAILABLE]))
                    self.logger.debug('under_construction: {}'
                                      .format(self.track_state_matrix[dictionary_keys[i]][UNDER_CONSTRUCTION]))
                    self.logger.debug('unlock_condition_from_level: {}'
                                      .format(self.track_state_matrix[dictionary_keys[i]][UNLOCK_CONDITION_FROM_LEVEL]))
                    self.logger.debug('unlock_condition_from_environment: {}'
                                      .format(self.track_state_matrix[dictionary_keys[i]][
                                                                            UNLOCK_CONDITION_FROM_ENVIRONMENT]))
                    self.logger.debug('unlock_condition_from_previous_track: {}'
                                      .format(self.track_state_matrix[dictionary_keys[i]][
                                                                            UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]))
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
                        self.logger.debug(f'construction time: {construction_time}')
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

                    self.logger.debug('description label text: {}'
                                      .format(self.description_tracks_labels[dictionary_keys[i]].text))
                    self.logger.debug('description label position: {}'
                                      .format((self.description_tracks_labels[dictionary_keys[i]].x,
                                               self.description_tracks_labels[dictionary_keys[i]].y)))
                    self.logger.debug('description label font size: {}'
                                      .format(self.description_tracks_labels[dictionary_keys[i]].font_size))
                    self.logger.debug('description label font color: {}'
                                      .format(self.description_tracks_labels[dictionary_keys[i]].color))
                    break

        if not self.is_activated:
            self.logger.debug(f'constructor_opacity: {self.constructor_opacity}')
            if self.constructor_opacity > 0:
                self.constructor_opacity -= 15

        self.logger.info('END ON_UPDATE')

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        self.logger.info('START ON_CHANGE_SCREEN_RESOLUTION')
        self.on_recalculate_ui_properties(screen_resolution)
        self.on_read_ui_info()
        self.logger.debug(f'is activated: {self.is_activated}')
        if self.is_activated:
            self.railway_station_caption_sprite.x = self.railway_station_caption_position[0]
            self.railway_station_caption_sprite.y = self.railway_station_caption_position[1]
            self.railway_station_caption_sprite.font_size = self.caption_font_size
            self.logger.debug('railway_station_caption_sprite position: {}'
                              .format((self.railway_station_caption_sprite.x,
                                       self.railway_station_caption_sprite.y)))
            self.logger.debug('railway_station_caption_sprite font size: {}'
                              .format(self.railway_station_caption_sprite.font_size))
            self.environment_caption_sprite.x = self.environment_caption_position[0]
            self.environment_caption_sprite.y = self.environment_caption_position[1]
            self.environment_caption_sprite.font_size = self.caption_font_size
            self.logger.debug('environment_caption_sprite position: {}'
                              .format((self.environment_caption_sprite.x,
                                       self.environment_caption_sprite.y)))
            self.logger.debug('environment_caption_sprite font size: {}'
                              .format(self.environment_caption_sprite.font_size))
            for i in range(4):
                self.coming_soon_environment_labels[i].x \
                    = self.environment_cell_positions[i][0] + self.placeholder_offset[0]
                self.coming_soon_environment_labels[i].y \
                    = self.environment_cell_positions[i][1] + self.placeholder_offset[1]
                self.coming_soon_environment_labels[i].font_size = self.placeholder_font_size
                self.logger.debug('coming_soon_environment_labels position: {}'
                                  .format((self.coming_soon_environment_labels[i].x,
                                           self.coming_soon_environment_labels[i].y)))
                self.logger.debug('coming_soon_environment_labels font size: {}'
                                  .format(self.coming_soon_environment_labels[i].font_size))

            dictionary_keys = list(self.locked_tracks_labels.keys())
            self.logger.debug(f'dictionary_keys: {dictionary_keys}')
            for i in range(len(dictionary_keys)):
                self.locked_tracks_labels[dictionary_keys[i]].x \
                    = self.track_cells_positions[i][0] + self.locked_label_offset[0]
                self.locked_tracks_labels[dictionary_keys[i]].y \
                    = self.track_cells_positions[i][1] + self.locked_label_offset[1]
                self.locked_tracks_labels[dictionary_keys[i]].font_size = self.locked_label_font_size
                self.logger.debug('locked_tracks_labels position: {}'
                                  .format((self.locked_tracks_labels[dictionary_keys[i]].x,
                                           self.locked_tracks_labels[dictionary_keys[i]].y)))
                self.logger.debug('locked_tracks_labels font size: {}'
                                  .format(self.locked_tracks_labels[dictionary_keys[i]].font_size))
                self.title_tracks_labels[dictionary_keys[i]].x \
                    = self.track_cells_positions[i][0] + self.title_label_offset[0]
                self.title_tracks_labels[dictionary_keys[i]].y \
                    = self.track_cells_positions[i][1] + self.title_label_offset[1]
                self.title_tracks_labels[dictionary_keys[i]].font_size = self.title_label_font_size
                self.logger.debug('title_tracks_labels position: {}'
                                  .format((self.title_tracks_labels[dictionary_keys[i]].x,
                                           self.title_tracks_labels[dictionary_keys[i]].y)))
                self.logger.debug('title_tracks_labels font size: {}'
                                  .format(self.title_tracks_labels[dictionary_keys[i]].font_size))
                self.description_tracks_labels[dictionary_keys[i]].x \
                    = self.track_cells_positions[i][0] + self.description_label_offset[0]
                self.description_tracks_labels[dictionary_keys[i]].y \
                    = self.track_cells_positions[i][1] + self.description_label_offset[1]
                self.description_tracks_labels[dictionary_keys[i]].font_size \
                    = self.description_label_font_size
                self.logger.debug('description_tracks_labels position: {}'
                                  .format((self.description_tracks_labels[dictionary_keys[i]].x,
                                           self.description_tracks_labels[dictionary_keys[i]].y)))
                self.logger.debug('description_tracks_labels font size: {}'
                                  .format(self.description_tracks_labels[dictionary_keys[i]].font_size))

            dictionary_keys = list(self.buy_buttons.keys())
            self.logger.debug(f'dictionary_keys: {dictionary_keys}')
            for i in range(len(dictionary_keys)):
                self.buy_buttons[dictionary_keys[i]].x_margin \
                    = self.track_cells_positions[i][0] + self.buy_button_offset[0]
                self.buy_buttons[dictionary_keys[i]].y_margin \
                    = self.track_cells_positions[i][1] + self.buy_button_offset[1]
                self.buy_buttons[dictionary_keys[i]].on_position_changed(
                    (self.buy_buttons[dictionary_keys[i]].x_margin, self.buy_buttons[dictionary_keys[i]].y_margin)
                )
                self.buy_buttons[dictionary_keys[i]] \
                    .on_size_changed((self.cell_height, self.cell_height),
                                     self.locked_label_font_size)

        self.close_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                      int(24 / 80 * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

        self.logger.info('END ON_CHANGE_SCREEN_RESOLUTION')

    def on_update_money(self, money, track_state_matrix):
        """
        Updates bank account state change when user spends or gains money.

        :param money:                   current bank account state
        :param track_state_matrix       table with all tracks state properties
        """
        self.logger.info('START ON_UPDATE_MONEY')
        self.money = money
        self.logger.debug(f'money: {self.money}')
        self.track_state_matrix = track_state_matrix
        self.logger.debug(f'track_state_matrix: {self.track_state_matrix}')
        if len(self.track_state_matrix) > 0:
            self.on_update_live_track_state(track_state_matrix, list(track_state_matrix.keys())[0])

        self.logger.info('END ON_UPDATE_MONEY')

    @view_is_active
    @track_cell_is_created
    def on_update_live_track_state(self, track_state_matrix, track):
        """
        Updates track state when constructor screen is opened and track cell has been created.

        :param track_state_matrix       table with all tracks state properties
        :param track:                   track number
        """
        self.logger.info('START ON_UPDATE_LIVE_TRACK_STATE')
        self.track_state_matrix = track_state_matrix
        self.logger.debug(f'track_state_matrix: {self.track_state_matrix}')
        self.logger.debug(f'unlock_available: {track_state_matrix[track][UNLOCK_AVAILABLE]}')
        if track_state_matrix[track][UNLOCK_AVAILABLE]:
            self.logger.debug(f'money: {self.money}')
            self.logger.debug(f'price: {track_state_matrix[track][PRICE]}')
            if self.money < track_state_matrix[track][PRICE]:
                self.locked_tracks_labels[track].text = ''
                self.logger.debug(f'locked_tracks_labels text: {self.locked_tracks_labels[track].text}')
            else:
                self.locked_tracks_labels[track].text = ' '
                self.logger.debug(f'locked_tracks_labels text: {self.locked_tracks_labels[track].text}')
                self.logger.debug(f'track: {track}')
                self.logger.debug(f'buy buttons track numbers: {self.buy_buttons.keys()}')
                if track not in self.buy_buttons:
                    self.buy_buttons[track] = BuyTrackButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                             groups=self.groups, on_click_action=self.on_buy_track)
                    self.buy_buttons[track].x_margin \
                        = self.track_cells_positions[list(track_state_matrix.keys()).index(track)][0] \
                        + self.buy_button_offset[0]
                    self.buy_buttons[track].y_margin \
                        = self.track_cells_positions[list(track_state_matrix.keys()).index(track)][1] \
                        + self.buy_button_offset[1]
                    self.buy_buttons[track].on_position_changed(
                        (self.buy_buttons[track].x_margin, self.buy_buttons[track].y_margin)
                    )
                    self.buy_buttons[track] \
                        .on_size_changed((self.cell_height, self.cell_height),
                                         self.locked_label_font_size)
                    self.logger.debug(f'buttons list length: {len(self.buttons)}')
                    self.buttons.append(self.buy_buttons[track])
                    self.logger.debug(f'buttons list length: {len(self.buttons)}')
                    self.buy_buttons[track].on_activate()
                    self.controller.on_append_handlers(
                        on_mouse_motion_handlers=[self.buy_buttons[track].handle_mouse_motion, ],
                        on_mouse_press_handlers=[self.buy_buttons[track].handle_mouse_press, ],
                        on_mouse_release_handlers=[self.buy_buttons[track].handle_mouse_release, ],
                        on_mouse_leave_handlers=[self.buy_buttons[track].handle_mouse_leave, ]
                    )

        else:
            self.logger.debug(f'under_construction: {track_state_matrix[track][UNDER_CONSTRUCTION]}')
            if not track_state_matrix[track][UNDER_CONSTRUCTION]:
                self.locked_tracks_labels[track].text = ''
            else:
                self.locked_tracks_labels[track].text = ' '

            self.logger.debug(f'locked_tracks_labels text: {self.locked_tracks_labels[track].text}')

        self.logger.debug('unlock_available: {}'
                          .format(track_state_matrix[track][UNLOCK_AVAILABLE]))
        self.logger.debug('under_construction: {}'
                          .format(track_state_matrix[track][UNDER_CONSTRUCTION]))
        self.logger.debug('unlock_condition_from_level: {}'
                          .format(track_state_matrix[track][UNLOCK_CONDITION_FROM_LEVEL]))
        self.logger.debug('unlock_condition_from_environment: {}'
                          .format(track_state_matrix[track][UNLOCK_CONDITION_FROM_ENVIRONMENT]))
        self.logger.debug('unlock_condition_from_previous_track: {}'
                          .format(track_state_matrix[track][UNLOCK_CONDITION_FROM_PREVIOUS_TRACK]))
        if track_state_matrix[track][UNLOCK_AVAILABLE]:
            self.description_tracks_labels[track].text = 'Available for {} ¤'\
                                                         .format(track_state_matrix[track][PRICE])
            self.description_tracks_labels[track].color = GREEN
        elif track_state_matrix[track][UNDER_CONSTRUCTION]:
            construction_time = track_state_matrix[track][CONSTRUCTION_TIME]
            self.logger.debug(f'construction time: {construction_time}')
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

        self.logger.debug('description label text: {}'
                          .format(self.description_tracks_labels[track].text))
        self.logger.debug('description label font color: {}'
                          .format(self.description_tracks_labels[track].color))
        self.logger.info('END ON_UPDATE_LIVE_TRACK_STATE')

    def on_update_track_state(self, track_state_matrix, game_time):
        """
        Updates track state matrix every frame in case cell for this track is not yet created.

        :param track_state_matrix       table with all tracks state properties
        :param game_time:               current in-game time
        """
        self.logger.info('START ON_UPDATE_TRACK_STATE')
        self.track_state_matrix = track_state_matrix
        self.logger.debug(f'track_state_matrix: {self.track_state_matrix}')
        self.logger.info('END ON_UPDATE_TRACK_STATE')

    @view_is_active
    def on_unlock_track_live(self, track):
        """
        Deletes unlocked track and moves all cells one position to the top of the screen.

        :param track:                   track number
        """
        self.logger.info('START ON_UNLOCK_TRACK_LIVE')
        cell_step = self.cell_height + self.interval_between_cells
        self.logger.debug(f'cell_step: {cell_step}')
        self.logger.debug(f'locked_tracks_labels: {self.locked_tracks_labels.keys()}')
        self.locked_tracks_labels[track].delete()
        self.locked_tracks_labels.pop(track)
        self.logger.debug(f'locked_tracks_labels: {self.locked_tracks_labels.keys()}')
        for t in self.locked_tracks_labels:
            self.logger.debug(f'locked track label Y position: {self.locked_tracks_labels[t].y}')
            self.locked_tracks_labels[t].y += cell_step
            self.logger.debug(f'locked track label Y position: {self.locked_tracks_labels[t].y}')

        self.logger.debug(f'title_tracks_labels: {self.title_tracks_labels.keys()}')
        self.title_tracks_labels[track].delete()
        self.title_tracks_labels.pop(track)
        self.logger.debug(f'title_tracks_labels: {self.title_tracks_labels.keys()}')
        for t in self.title_tracks_labels:
            self.logger.debug(f'title track label Y position: {self.title_tracks_labels[t].y}')
            self.title_tracks_labels[t].y += cell_step
            self.logger.debug(f'title track label Y position: {self.title_tracks_labels[t].y}')

        self.logger.debug(f'description_tracks_labels: {self.description_tracks_labels.keys()}')
        self.description_tracks_labels[track].delete()
        self.description_tracks_labels.pop(track)
        self.logger.debug(f'description_tracks_labels: {self.description_tracks_labels.keys()}')
        for t in self.description_tracks_labels:
            self.logger.debug(f'description track label Y position: {self.description_tracks_labels[t].y}')
            self.description_tracks_labels[t].y += cell_step
            self.logger.debug(f'description track label Y position: {self.description_tracks_labels[t].y}')

        for b in self.buy_buttons:
            self.buy_buttons[b].y_margin += cell_step
            self.buy_buttons[b].on_position_changed(
                (self.buy_buttons[b].x_margin, self.buy_buttons[b].y_margin)
            )

        for p in range(len(self.no_more_tracks_available_labels)):
            self.logger.debug('no_more_tracks_available label Y position: {}'
                              .format(self.no_more_tracks_available_labels[p].y))
            self.no_more_tracks_available_labels[p].y += cell_step
            self.logger.debug('no_more_tracks_available label Y position: {}'
                              .format(self.no_more_tracks_available_labels[p].y))

        self.logger.info('END ON_UNLOCK_TRACK_LIVE')

    def on_read_ui_info(self):
        """
        Reads aff offsets and font size from the database.
        """
        self.logger.info('START ON_READ_UI_INFO')
        self.config_db_cursor.execute('''SELECT constructor_railway_station_caption_x, constructor_caption_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.railway_station_caption_position = self.config_db_cursor.fetchone()
        self.logger.debug(f'railway_station_caption_position: {self.railway_station_caption_position}')
        self.config_db_cursor.execute('''SELECT constructor_environment_caption_x, constructor_caption_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.environment_caption_position = self.config_db_cursor.fetchone()
        self.logger.debug(f'environment_caption_position: {self.environment_caption_position}')
        self.config_db_cursor.execute('''SELECT constructor_cell_height, constructor_interval_between_cells
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        self.cell_height, self.interval_between_cells = self.config_db_cursor.fetchone()
        self.logger.debug(f'cell_height: {self.cell_height}')
        self.logger.debug(f'interval_between_cells: {self.interval_between_cells}')
        cell_step = self.cell_height + self.interval_between_cells
        self.config_db_cursor.execute('''SELECT constructor_cell_top_left_x, constructor_cell_top_left_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        fetched_coords = self.config_db_cursor.fetchone()
        self.track_cells_positions = ((fetched_coords[0], fetched_coords[1]),
                                      (fetched_coords[0], fetched_coords[1] - cell_step),
                                      (fetched_coords[0], fetched_coords[1] - cell_step * 2),
                                      (fetched_coords[0], fetched_coords[1] - cell_step * 3))
        self.logger.debug(f'track_cells_positions: {self.track_cells_positions}')
        self.config_db_cursor.execute('''SELECT constructor_cell_top_right_x, constructor_cell_top_right_y
                                         FROM screen_resolution_config WHERE app_width = ? AND app_height = ?''',
                                      (self.screen_resolution[0], self.screen_resolution[1]))
        fetched_coords = self.config_db_cursor.fetchone()
        self.environment_cell_positions = ((fetched_coords[0], fetched_coords[1]),
                                           (fetched_coords[0], fetched_coords[1] - cell_step),
                                           (fetched_coords[0], fetched_coords[1] - cell_step * 2),
                                           (fetched_coords[0], fetched_coords[1] - cell_step * 3))
        self.logger.debug(f'environment_cell_positions: {self.environment_cell_positions}')
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
            self.buy_button_offset[0], self.buy_button_offset[1], \
            self.title_label_offset[0], self.title_label_offset[1], \
            self.description_label_offset[0], self.description_label_offset[1], \
            self.placeholder_offset[0], self.placeholder_offset[1], \
            self.locked_label_font_size, self.title_label_font_size, \
            self.description_label_font_size, self.placeholder_font_size, \
            self.caption_font_size = self.config_db_cursor.fetchone()
        self.logger.debug(f'locked_label_offset: {self.locked_label_offset}')
        self.logger.debug(f'buy_button_offset: {self.buy_button_offset}')
        self.logger.debug(f'title_label_offset: {self.title_label_offset}')
        self.logger.debug(f'description_label_offset: {self.description_label_offset}')
        self.logger.debug(f'placeholder_offset: {self.placeholder_offset}')
        self.logger.debug(f'locked_label_font_size: {self.locked_label_font_size}')
        self.logger.debug(f'title_label_font_size: {self.title_label_font_size}')
        self.logger.debug(f'description_label_font_size: {self.description_label_font_size}')
        self.logger.debug(f'placeholder_font_size: {self.placeholder_font_size}')
        self.logger.debug(f'caption_font_size: {self.caption_font_size}')
        self.logger.info('END ON_READ_UI_INFO')
