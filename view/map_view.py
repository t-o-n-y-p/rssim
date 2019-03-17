from logging import getLogger
from time import perf_counter

from pyglet.sprite import Sprite
from pyglet import resource

from view import *
from button import create_two_state_button
from button.zoom_in_button import ZoomInButton
from button.zoom_out_button import ZoomOutButton
from button.open_schedule_button import OpenScheduleButton
from button.open_constructor_button import OpenConstructorButton


class MapView(View):
    """
    Implements Map view.
    Map object is responsible for properties, UI and events related to the map.
    """
    def __init__(self, user_db_cursor, config_db_cursor, surface, batches, groups):
        """
        Button click handlers:
            on_click_zoom_in_button             on_click handler for zoom in button
            on_click_zoom_out_button            on_click handler for zoom out button
            on_leave_action                     on_leave handler for buttons located inside the map area
            on_hover_action                     on_hover handler for buttons located inside the map area
            on_open_schedule                    on_click handler for open schedule button
            on_open_constructor                 on_click handler for open constructor button

        Properties:
            unlocked_tracks                     number of unlocked tracks in the game
            main_map                            main map texture
            environment                         environment texture
            map_offset                          additional offset from map base offset for smaller maps
            mini_map_offset                     additional offset from mini_map position
            main_map_sprite                     sprite for main map from main map texture
            environment_sprite                  sprite for main environment from environment texture
            mini_map_sprite                     sprite for mini-map from main map texture
            mini_environment_sprite             sprite for mini-map environment from environment texture
            is_mini_map_activated               indicates if mini map is displayed or not
            mini_map_timer                      indicates how much time passed since user released mouse button
            map_opacity                         general map opacity
            mini_map_opacity                    mini-map opacity
            base_offset_lower_left_limit        maximum value for vertical and horizontal base offset
            base_offset_upper_right_limit       minimum value for vertical and horizontal base offset
            mini_map_position                   position of mini-map lower left corner
            mini_map_width                      width of the mini-map
            mini_map_height                     height of the mini-map
            zoom_in_button                      ZoomInButton object
            zoom_out_button                     ZoomOutButton object
            open_schedule_button                OpenScheduleButton object
            open_constructor_button             OpenConstructorButton object
            buttons                             list of all buttons
            map_move_mode_available             indicates if user can drag the map to move it
            map_move_mode                       indicates if user is about to move the map
            on_mouse_press_handlers             list of on_mouse_press event handlers
            on_mouse_release_handlers           list of on_mouse_release event handlers
            on_mouse_drag_handlers              list of on_mouse_drag event handlers

        :param user_db_cursor:                  user DB cursor (is used to execute user DB queries)
        :param config_db_cursor:                configuration DB cursor (is used to execute configuration DB queries)
        :param surface:                         surface to draw all UI objects on
        :param batches:                         batches to group all labels and sprites
        :param groups:                          defines drawing layers (some labels and sprites behind others)
        """
        def on_click_zoom_in_button(button):
            """
            Deactivates zoom in button. Activates zoom out button.
            Notifies controller that player has zoomed in the map.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_zoom_in()

        def on_click_zoom_out_button(button):
            """
            Deactivates zoom out button. Activates zoom in button.
            Notifies controller that player has zoomed out the map.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            button.paired_button.on_activate()
            self.controller.on_zoom_out()

        def on_leave_action():
            """
            Map move mode becomes available if mouse cursor is not over any button located inside the map area.
            """
            self.map_move_mode_available = True

        def on_hover_action():
            """
            Map move mode becomes unavailable if mouse cursor is over any button located inside the map area.
            """
            self.map_move_mode_available = False

        def on_open_schedule(button):
            """
            Deactivates open schedule button.
            Notifies controller that player has opened schedule screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.on_open_schedule()

        def on_open_constructor(button):
            """
            Deactivates open constructor button.
            Notifies controller that player has opened constructor screen.

            :param button:                      button that was clicked
            """
            button.on_deactivate()
            self.controller.on_open_constructor()

        super().__init__(user_db_cursor, config_db_cursor, surface, batches, groups,
                         logger=getLogger('root.app.game.map.view'))
        self.user_db_cursor.execute('SELECT unlocked_tracks FROM game_progress')
        self.unlocked_tracks = self.user_db_cursor.fetchone()[0]
        self.main_map = resource.image(f'full_map_{self.unlocked_tracks}.dds')
        self.environment = resource.image('full_map_e_0.dds')
        self.map_offset = (0, 0)
        self.mini_map_offset = (0, 0)
        self.on_change_map_offset()
        self.main_map_sprite = None
        self.environment_sprite = None
        self.mini_map_sprite = None
        self.mini_environment_sprite = None
        self.is_mini_map_activated = False
        self.mini_map_timer = 0.0
        self.map_opacity = 0
        self.mini_map_opacity = 0
        self.mini_map_width = 0
        self.mini_map_height = 0
        self.mini_map_position = (0, 0)
        self.base_offset_lower_left_limit = (0, 0)
        self.base_offset_upper_right_limit = (self.screen_resolution[0] - MAP_WIDTH,
                                              self.screen_resolution[1] - MAP_HEIGHT)
        self.zoom_in_button, self.zoom_out_button \
            = create_two_state_button(ZoomInButton(surface=self.surface,
                                                   batch=self.batches['ui_batch'], groups=self.groups,
                                                   on_click_action=on_click_zoom_in_button,
                                                   on_hover_action=on_hover_action,
                                                   on_leave_action=on_leave_action),
                                      ZoomOutButton(surface=self.surface,
                                                    batch=self.batches['ui_batch'], groups=self.groups,
                                                    on_click_action=on_click_zoom_out_button,
                                                    on_hover_action=on_hover_action,
                                                    on_leave_action=on_leave_action))
        self.open_schedule_button = OpenScheduleButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                       groups=self.groups, on_click_action=on_open_schedule)
        self.open_constructor_button = OpenConstructorButton(surface=self.surface, batch=self.batches['ui_batch'],
                                                             groups=self.groups, on_click_action=on_open_constructor)
        self.buttons.append(self.zoom_in_button)
        self.buttons.append(self.zoom_out_button)
        self.buttons.append(self.open_schedule_button)
        self.buttons.append(self.open_constructor_button)
        self.map_move_mode_available = True
        self.map_move_mode = False
        self.on_mouse_press_handlers.append(self.handle_mouse_press)
        self.on_mouse_release_handlers.append(self.handle_mouse_release)
        self.on_mouse_drag_handlers.append(self.handle_mouse_drag)

    def on_update(self):
        """
        Updates fade-in/fade-out animations.
        """
        if self.is_activated and self.map_opacity < 255:
            self.map_opacity += 15
            self.main_map_sprite.opacity += 15
            self.environment_sprite.opacity += 15

        if not self.is_activated and self.map_opacity > 0:
            self.map_opacity -= 15
            self.main_map_sprite.opacity -= 15
            if self.main_map_sprite.opacity <= 0:
                self.main_map_sprite.delete()
                self.main_map_sprite = None

            self.environment_sprite.opacity -= 15
            if self.environment_sprite.opacity <= 0:
                self.environment_sprite.delete()
                self.environment_sprite = None

        if self.is_mini_map_activated and self.mini_map_opacity < 255:
            self.mini_map_opacity += 15
            self.mini_map_sprite.opacity += 15
            self.mini_environment_sprite.opacity += 15

        if not self.is_mini_map_activated and self.mini_map_opacity > 0:
            self.mini_map_opacity -= 15
            self.mini_map_sprite.opacity -= 15
            if self.mini_map_sprite.opacity <= 0:
                self.mini_map_sprite.delete()
                self.mini_map_sprite = None

            self.mini_environment_sprite.opacity -= 15
            if self.mini_environment_sprite.opacity <= 0:
                self.mini_environment_sprite.delete()
                self.mini_environment_sprite = None

        cpu_time = perf_counter()
        if self.is_mini_map_activated and not self.map_move_mode \
                and cpu_time - self.mini_map_timer > MINI_MAP_FADE_OUT_TIMER:
            self.is_mini_map_activated = False

    @mini_map_is_not_active
    def on_activate_mini_map(self):
        """
        Activates mini-map when user starts moving the main map.
        """
        self.is_mini_map_activated = True
        if self.mini_environment_sprite is None:
            self.mini_environment_sprite = Sprite(self.environment, x=self.mini_map_position[0],
                                                  y=self.mini_map_position[1], batch=self.batches['mini_map_batch'],
                                                  group=self.groups['mini_environment'])
            self.mini_environment_sprite.opacity = 0

        self.mini_environment_sprite.scale = self.mini_map_width / MAP_WIDTH
        if self.mini_map_sprite is None:
            self.mini_map_sprite = Sprite(self.main_map, x=self.mini_map_position[0],
                                          y=self.mini_map_position[1]
                                          + int(self.mini_map_offset[1] * self.mini_map_width / MAP_WIDTH),
                                          batch=self.batches['mini_map_batch'], group=self.groups['mini_map'])
            self.mini_map_sprite.opacity = 0

        self.mini_map_sprite.scale = self.mini_map_width / MAP_WIDTH

    @view_is_not_active
    def on_activate(self):
        """
        Activates the view and creates all sprites and labels.
        """
        self.is_activated = True
        self.on_change_map_offset()
        if self.main_map_sprite is None:
            self.main_map_sprite = Sprite(self.main_map, x=self.base_offset[0] + self.map_offset[0],
                                          y=self.base_offset[1] + self.map_offset[1],
                                          batch=self.batches['main_batch'], group=self.groups['main_map'])
            self.main_map_sprite.opacity = 0

        self.main_map_sprite.scale = self.zoom_factor
        if self.environment_sprite is None:
            self.environment_sprite = Sprite(self.environment, x=self.base_offset[0], y=self.base_offset[1],
                                             batch=self.batches['main_batch'], group=self.groups['environment'])
            self.environment_sprite.opacity = 0

        self.environment_sprite.scale = self.zoom_factor
        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

        if self.zoom_out_activated:
            self.zoom_in_button.on_activate()
        else:
            self.zoom_out_button.on_activate()

    @view_is_active
    def on_deactivate(self):
        """
        Deactivates the view and the mini-map, destroys all labels and buttons.
        """
        self.is_activated = False
        self.is_mini_map_activated = False
        for b in self.buttons:
            b.on_deactivate()

    def on_change_base_offset(self, new_base_offset):
        """
        Updates base offset and moves all labels and sprites to its new positions.

        :param new_base_offset:         new base offset
        """
        self.base_offset = new_base_offset
        if self.is_activated:
            self.main_map_sprite.position = (self.base_offset[0] + self.map_offset[0],
                                             self.base_offset[1] + self.map_offset[1])
            self.environment_sprite.position = self.base_offset

    def on_unlock_track(self, track):
        """
        Updates number of unlocked tracks.

        :param track:                   track number
        :return:
        """
        self.unlocked_tracks = track
        self.main_map = resource.image(f'full_map_{track}.dds')
        self.on_change_map_offset()
        if self.is_activated:
            self.main_map_sprite.image = self.main_map
            self.main_map_sprite.position = (self.base_offset[0] + self.map_offset[0],
                                             self.base_offset[1] + self.map_offset[1])

        if self.is_mini_map_activated:
            self.mini_map_sprite.image = self.main_map
            self.mini_map_sprite.update(y=self.mini_map_position[1]
                                        + int(self.mini_map_offset[1] * self.mini_map_width / MAP_WIDTH),
                                        scale=self.mini_map_width / MAP_WIDTH)

    def on_change_zoom_factor(self, zoom_factor, zoom_out_activated):
        """
        Zooms in/out all sprites.
        Note that adjusting base offset is made by on_change_base_offset handler,
        this function only changes scale.

        :param zoom_factor                      sprite scale coefficient
        :param zoom_out_activated               indicates if zoom out mode is activated
        """
        self.zoom_factor = zoom_factor
        self.zoom_out_activated = zoom_out_activated
        self.on_change_map_offset()
        if self.is_activated:
            self.main_map_sprite.scale = zoom_factor
            self.environment_sprite.scale = zoom_factor

        if self.zoom_out_activated:
            self.base_offset_upper_right_limit = (self.screen_resolution[0] - MAP_WIDTH // 2,
                                                  self.screen_resolution[1] - MAP_HEIGHT // 2)
            self.base_offset = (self.base_offset[0] // 2 + self.screen_resolution[0] // 4,
                                self.base_offset[1] // 2 + self.screen_resolution[1] // 4)
        else:
            self.base_offset_upper_right_limit = (self.screen_resolution[0] - MAP_WIDTH,
                                                  self.screen_resolution[1] - MAP_HEIGHT)
            self.base_offset = (self.base_offset[0] * 2 - self.screen_resolution[0] // 2,
                                self.base_offset[1] * 2 - self.screen_resolution[1] // 2)

        self.check_base_offset_limits()

    def on_change_screen_resolution(self, screen_resolution):
        """
        Updates screen resolution and moves all labels and sprites to its new positions.

        :param screen_resolution:       new screen resolution
        """
        if self.zoom_out_activated:
            self.base_offset_upper_right_limit = (screen_resolution[0] - MAP_WIDTH // 2,
                                                  screen_resolution[1] - MAP_HEIGHT // 2)
        else:
            self.base_offset_upper_right_limit = (screen_resolution[0] - MAP_WIDTH,
                                                  screen_resolution[1] - MAP_HEIGHT)

        self.base_offset = (self.base_offset[0] + (screen_resolution[0] - self.screen_resolution[0]) // 2,
                            self.base_offset[1] + (screen_resolution[1] - self.screen_resolution[1]) // 2)
        self.check_base_offset_limits()
        self.on_recalculate_ui_properties(screen_resolution)
        self.mini_map_width = self.screen_resolution[0] // 4
        self.mini_map_height = round(self.mini_map_width / 2)
        self.mini_map_position = (self.screen_resolution[0] - self.mini_map_width - 8,
                                  self.screen_resolution[1] - self.top_bar_height - 6 - self.mini_map_height)
        if self.is_mini_map_activated:
            self.mini_environment_sprite.update(x=self.mini_map_position[0], y=self.mini_map_position[1],
                                                scale=self.mini_map_width / MAP_WIDTH)
            self.mini_map_sprite.update(x=self.mini_map_position[0],
                                        y=self.mini_map_position[1]
                                        + int(self.mini_map_offset[1] * self.mini_map_width / MAP_WIDTH),
                                        scale=self.mini_map_width / MAP_WIDTH)

        self.zoom_in_button.x_margin = 0
        self.zoom_in_button.y_margin = self.screen_resolution[1] - self.top_bar_height - self.top_bar_height * 2 + 4
        self.zoom_in_button.on_size_changed((self.top_bar_height * 2 - 2, self.top_bar_height * 2 - 2),
                                            int(self.zoom_in_button.base_font_size_property * self.bottom_bar_height))
        self.zoom_out_button.x_margin = 0
        self.zoom_out_button.y_margin = self.screen_resolution[1] - self.top_bar_height - self.top_bar_height * 2 + 4
        self.zoom_out_button.on_size_changed((self.top_bar_height * 2 - 2, self.top_bar_height * 2 - 2),
                                             int(self.zoom_out_button.base_font_size_property * self.bottom_bar_height))
        self.open_schedule_button.x_margin = self.screen_resolution[0] - 11 * self.bottom_bar_height // 2 + 2
        self.open_schedule_button.y_margin = 0
        self.open_schedule_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                  int(self.open_schedule_button.base_font_size_property
                                                      * self.bottom_bar_height))
        self.open_constructor_button.on_size_changed((self.bottom_bar_height, self.bottom_bar_height),
                                                     int(self.open_constructor_button.base_font_size_property
                                                         * self.bottom_bar_height))
        for b in self.buttons:
            b.on_position_changed((b.x_margin, b.y_margin))

    def on_deactivate_zoom_buttons(self):
        """
        Deactivates zoom buttons when user opens schedule or constructor screen.
        """
        self.zoom_in_button.on_deactivate()
        self.zoom_out_button.on_deactivate()

    def on_activate_zoom_buttons(self):
        """
        Activates appropriate zoom button when user closes schedule or constructor screen.
        """
        if self.zoom_out_activated:
            self.zoom_in_button.on_activate()
        else:
            self.zoom_out_button.on_activate()

    @view_is_active
    @cursor_is_on_the_map
    @left_mouse_button
    @map_move_mode_available
    def handle_mouse_press(self, x, y, button, modifiers):
        """
        When left button is pressed and mouse cursor is over the map, activates map move mode and mini-map.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param button:          determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.map_move_mode = True
        self.on_activate_mini_map()

    @map_move_mode_enabled
    def handle_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """
        Moves the map if map move mode is active and player moves his mouse.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param dx:              relative X position from the previous mouse position
        :param dy:              relative Y position from the previous mouse position
        :param buttons:         determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.base_offset = (self.base_offset[0] + dx, self.base_offset[1] + dy)
        self.check_base_offset_limits()
        self.controller.on_change_base_offset(self.base_offset)

    @left_mouse_button
    def handle_mouse_release(self, x, y, button, modifiers):
        """
        When left button is released, deactivates map move mode and starts mini-map timer.

        :param x:               mouse cursor X position inside the app window
        :param y:               mouse cursor Y position inside the app window
        :param button:          determines which mouse button was pressed
        :param modifiers:       determines if some modifier key is held down (at the moment we don't use it)
        """
        self.map_move_mode = False
        self.mini_map_timer = perf_counter()

    def check_base_offset_limits(self):
        """
        Checks if new base offset value exceeds the limits and updates it if needed.
        """
        if self.base_offset[0] > self.base_offset_lower_left_limit[0]:
            self.base_offset = (self.base_offset_lower_left_limit[0], self.base_offset[1])

        if self.base_offset[0] < self.base_offset_upper_right_limit[0]:
            self.base_offset = (self.base_offset_upper_right_limit[0], self.base_offset[1])

        if self.base_offset[1] > self.base_offset_lower_left_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_lower_left_limit[1])

        if self.base_offset[1] < self.base_offset_upper_right_limit[1]:
            self.base_offset = (self.base_offset[0], self.base_offset_upper_right_limit[1])

    def on_change_map_offset(self):
        """
        Adjusts map offset based on texture height and map height.
        """
        if self.zoom_out_activated:
            self.map_offset = (0, (MAP_HEIGHT - self.main_map.height) // 4)
        else:
            self.map_offset = (0, (MAP_HEIGHT - self.main_map.height) // 2)

        self.mini_map_offset = (0, (MAP_HEIGHT - self.main_map.height) // 2)
