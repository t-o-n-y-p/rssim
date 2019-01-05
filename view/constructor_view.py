from pyglet.text import Label
from pyglet.image import load
from pyglet.sprite import Sprite

from .view_base import View
from .button import CloseConstructorButton, BuyTrackButton


def _view_is_active(fn):
    def _handle_if_view_is_activated(*args, **kwargs):
        if args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_activated


def _view_is_not_active(fn):
    def _handle_if_view_is_not_activated(*args, **kwargs):
        if not args[0].is_activated:
            fn(*args, **kwargs)

    return _handle_if_view_is_not_activated


def _track_is_in_top4(fn):
    def _handle_if_track_is_in_top4(*args, **kwargs):
        if args[2] in args[0].locked_tracks_labels:
            fn(*args, **kwargs)

    return _handle_if_track_is_in_top4


class ConstructorView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        def on_close_constructor(button):
            self.controller.on_deactivate_view()

        def on_buy_track(button):
            button.on_deactivate()
            key_for_remove = None
            for key, value in self.buy_buttons.items():
                if value == button:
                    key_for_remove = key
                    self.controller.on_put_track_under_construction(key)

            self.controller.on_detach_handlers(
                on_mouse_motion_handlers=[self.buy_buttons[key_for_remove].handle_mouse_motion, ],
                on_mouse_press_handlers=[self.buy_buttons[key_for_remove].handle_mouse_press, ],
                on_mouse_release_handlers=[self.buy_buttons[key_for_remove].handle_mouse_release, ],
                on_mouse_leave_handlers=[self.buy_buttons[key_for_remove].handle_mouse_leave, ]
            )
            self.buttons.remove(self.buy_buttons.pop(key_for_remove))

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.screen_resolution = (1280, 720)
        self.background_image = load('img/constructor/constructor_1280_720.png')
        self.background_sprite = None
        self.locked_tracks_labels = {}
        self.title_tracks_labels = {}
        self.description_tracks_labels = {}
        self.buy_buttons = {}
        self.no_more_tracks_available_labels = []
        self.coming_soon_environment_labels = []
        self.close_constructor_button = CloseConstructorButton(surface=self.surface, batch=self.batch,
                                                               groups=self.groups, on_click_action=on_close_constructor)
        self.buttons.append(self.close_constructor_button)
        self.on_buy_track = on_buy_track
        self.money = 0.0
        self.track_state_locked = 0
        self.track_state_under_construction = 1
        self.track_state_construction_time = 2
        self.track_state_unlock_condition_from_level = 3
        self.track_state_unlock_condition_from_previous_track = 4
        self.track_state_unlock_condition_from_environment = 5
        self.track_state_unlock_available = 6
        self.track_state_price = 7
        self.track_state_level = 8

    @_view_is_not_active
    def on_activate(self):
        self.is_activated = True
        if self.background_sprite is None:
            self.background_sprite = Sprite(self.background_image, x=0, y=78, batch=self.batch,
                                            group=self.groups['main_frame'])
            self.background_sprite.opacity = 0

        self.coming_soon_environment_labels \
            = [Label('Coming soon', font_name='Arial', font_size=22, color=(112, 112, 112, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 - 168 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']),
               Label('Coming soon', font_name='Arial', font_size=22, color=(112, 112, 112, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 - 67 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']),
               Label('Coming soon', font_name='Arial', font_size=22, color=(112, 112, 112, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 + 34 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']),
               Label('Coming soon', font_name='Arial', font_size=22, color=(112, 112, 112, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 + 135 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text'])
               ]

        for b in self.buttons:
            if b.to_activate_on_controller_init:
                b.on_activate()

    @_view_is_active
    def on_deactivate(self):
        self.is_activated = False
        for l in self.coming_soon_environment_labels:
            l.delete()
            l = None

        for d in self.locked_tracks_labels:
            self.locked_tracks_labels[d].delete()

        self.locked_tracks_labels.clear()

        for d in self.title_tracks_labels:
            self.title_tracks_labels[d].delete()

        self.title_tracks_labels.clear()

        for d in self.description_tracks_labels:
            self.description_tracks_labels[d].delete()

        self.description_tracks_labels.clear()

        for l in self.no_more_tracks_available_labels:
            l.delete()
            l = None

        for b in self.buttons:
            b.on_deactivate()

        self.locked_tracks_labels = {}
        self.title_tracks_labels = {}
        self.description_tracks_labels = {}
        for key in self.buy_buttons:
            self.controller.on_detach_handlers(
                on_mouse_motion_handlers=[self.buy_buttons[key].handle_mouse_motion, ],
                on_mouse_press_handlers=[self.buy_buttons[key].handle_mouse_press, ],
                on_mouse_release_handlers=[self.buy_buttons[key].handle_mouse_release, ],
                on_mouse_leave_handlers=[self.buy_buttons[key].handle_mouse_leave, ]
            )
            self.buttons.remove(self.buy_buttons[key])

        self.buy_buttons = {}
        self.no_more_tracks_available_labels = []
        self.coming_soon_environment_labels = []

    def on_update(self):
        if self.is_activated and self.background_sprite.opacity < 255:
            self.background_sprite.opacity += 15

        if not self.is_activated and self.background_sprite is not None:
            if self.background_sprite.opacity > 0:
                self.background_sprite.opacity -= 15
                if self.background_sprite.opacity <= 0:
                    self.background_sprite.delete()
                    self.background_sprite = None

    def on_change_screen_resolution(self, screen_resolution):
        self.screen_resolution = screen_resolution
        self.background_image = load('img/constructor/constructor_{}_{}.png'
                                     .format(self.screen_resolution[0], self.screen_resolution[1]))
        if self.is_activated:
            self.background_sprite.image = self.background_image
            for i in range(4):
                self.coming_soon_environment_labels[i].x = self.screen_resolution[0] // 2 + 21 + 288
                self.coming_soon_environment_labels[i].y = self.screen_resolution[1] // 2 - 168 + 40 + i * 101

        self.close_constructor_button.x_margin = self.screen_resolution[0]
        self.close_constructor_button.y_margin = self.screen_resolution[1]
        for b in self.buttons:
            b.on_position_changed((screen_resolution[0] - b.x_margin, screen_resolution[1] - b.y_margin))

    def on_update_money(self, money):
        self.money = money

    @_view_is_active
    @_track_is_in_top4
    def on_update_live_track_state(self, track_state_matrix, track):
        if track_state_matrix[track][self.track_state_unlock_available]:
            if self.money < track_state_matrix[track][self.track_state_price]:
                self.locked_tracks_labels[track].text = ''
            else:
                self.locked_tracks_labels[track].text = ' '
                if track not in self.buy_buttons:
                    self.buy_buttons[track] = BuyTrackButton(surface=self.surface, batch=self.batch,
                                                             groups=self.groups, on_click_action=self.on_buy_track)
                    self.buy_buttons[track].x_margin = self.screen_resolution[0] // 2 + 11 + 80
                    self.buy_buttons[track].y_margin \
                        = self.screen_resolution[1] // 2 - 135 + list(track_state_matrix.keys()).index(track) * 101
                    self.buy_buttons[track].on_position_changed(
                        (self.screen_resolution[0] - self.buy_buttons[track].x_margin,
                         self.screen_resolution[1] - self.buy_buttons[track].y_margin)
                    )
                    self.buttons.append(self.buy_buttons[track])
                    self.buy_buttons[track].on_activate()
                    self.controller.on_append_handlers(
                        on_mouse_motion_handlers=[self.buy_buttons[track].handle_mouse_motion, ],
                        on_mouse_press_handlers=[self.buy_buttons[track].handle_mouse_press, ],
                        on_mouse_release_handlers=[self.buy_buttons[track].handle_mouse_release, ],
                        on_mouse_leave_handlers=[self.buy_buttons[track].handle_mouse_leave, ]
                    )

        else:
            if not track_state_matrix[track][self.track_state_under_construction]:
                self.locked_tracks_labels[track].text = ''
            else:
                self.locked_tracks_labels[track].text = ' '

        if track_state_matrix[track][self.track_state_unlock_available]:
            self.description_tracks_labels[track].text = 'Available for {} ¤'\
                                                         .format(track_state_matrix[track][self.track_state_price])
            self.description_tracks_labels[track].color = (0, 192, 0, 255)
        elif track_state_matrix[track][self.track_state_under_construction]:
            construction_time = track_state_matrix[track][self.track_state_construction_time]
            self.description_tracks_labels[track].text = 'Under construction. {}h {}min left'\
                                                         .format(construction_time // 14400,
                                                                 (construction_time // 240) % 60)
            self.description_tracks_labels[track].color = (255, 127, 0, 255)
        else:
            if not track_state_matrix[track][self.track_state_unlock_condition_from_level]:
                self.description_tracks_labels[track].text = 'Requires level {}'\
                                                             .format(track_state_matrix[track][self.track_state_level])
                self.description_tracks_labels[track].color = (112, 112, 112, 255)
            elif not track_state_matrix[track][self.track_state_unlock_condition_from_environment]:
                self.description_tracks_labels[track].text = 'Requires environment Tier X'
                self.description_tracks_labels[track].color = (112, 112, 112, 255)
            elif not track_state_matrix[track][self.track_state_unlock_condition_from_previous_track]:
                self.description_tracks_labels[track].text = 'Build track {} to unlock'.format(track - 1)
                self.description_tracks_labels[track].color = (112, 112, 112, 255)

    @_view_is_active
    def on_update_track_state(self, track_state_matrix, game_time):
        dictionary_keys = list(track_state_matrix.keys())
        available_options = min(len(dictionary_keys), 4)
        if available_options < 4:
            for i in range(len(self.no_more_tracks_available_labels)):
                self.no_more_tracks_available_labels[i].x = self.screen_resolution[0] // 2 - 21 - 288
                self.no_more_tracks_available_labels[i].y = self.screen_resolution[1] // 2 - 168 + 40 + i * 101

            if len(self.no_more_tracks_available_labels) < 4 - available_options:
                self.no_more_tracks_available_labels.append(
                    Label('No more track available', font_name='Arial', font_size=22, color=(112, 112, 112, 255),
                          x=self.screen_resolution[0] // 2 - 11 - 288,
                          y=self.screen_resolution[1] // 2 - 168 + 40 + len(self.no_more_tracks_available_labels) * 101,
                          anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text'])
                )

        for i in range(available_options):
            if dictionary_keys[i] not in self.locked_tracks_labels:
                if track_state_matrix[dictionary_keys[i]][self.track_state_unlock_available]:
                    if self.money < track_state_matrix[dictionary_keys[i]][self.track_state_price]:
                        self.locked_tracks_labels[dictionary_keys[i]] \
                            = Label('', font_name='Webdings', font_size=40, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 40,
                                    y=self.screen_resolution[1] // 2 + 135 + 40 - i * 101,
                                    anchor_x='center', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                    else:
                        self.locked_tracks_labels[dictionary_keys[i]] \
                            = Label(' ', font_name='Webdings', font_size=40, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 40,
                                    y=self.screen_resolution[1] // 2 + 135 + 40 - i * 101,
                                    anchor_x='center', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                        self.buy_buttons[dictionary_keys[i]] = BuyTrackButton(surface=self.surface, batch=self.batch,
                                                                              groups=self.groups,
                                                                              on_click_action=self.on_buy_track)
                        self.buy_buttons[dictionary_keys[i]].x_margin = self.screen_resolution[0] // 2 + 11 + 80
                        self.buy_buttons[dictionary_keys[i]].y_margin \
                            = self.screen_resolution[1] // 2 - 135 + i * 101
                        self.buy_buttons[dictionary_keys[i]].on_position_changed(
                            (self.screen_resolution[0] - self.buy_buttons[dictionary_keys[i]].x_margin,
                             self.screen_resolution[1] - self.buy_buttons[dictionary_keys[i]].y_margin)
                        )
                        self.buttons.append(self.buy_buttons[dictionary_keys[i]])
                        self.buy_buttons[dictionary_keys[i]].on_activate()
                        self.controller.on_append_handlers(
                            on_mouse_motion_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_motion, ],
                            on_mouse_press_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_press, ],
                            on_mouse_release_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_release, ],
                            on_mouse_leave_handlers=[self.buy_buttons[dictionary_keys[i]].handle_mouse_leave, ]
                        )

                else:
                    if not track_state_matrix[dictionary_keys[i]][self.track_state_under_construction]:
                        self.locked_tracks_labels[dictionary_keys[i]] \
                            = Label('', font_name='Webdings', font_size=40, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 40,
                                    y=self.screen_resolution[1] // 2 + 135 + 40 - i * 101,
                                    anchor_x='center', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                    else:
                        self.locked_tracks_labels[dictionary_keys[i]] \
                            = Label(' ', font_name='Webdings', font_size=40, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 40,
                                    y=self.screen_resolution[1] // 2 + 135 + 40 - i * 101,
                                    anchor_x='center', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])

                self.title_tracks_labels[dictionary_keys[i]] \
                    = Label(f'Track {dictionary_keys[i]}', font_name='Arial', font_size=24, color=(255, 255, 255, 255),
                            x=self.screen_resolution[0] // 2 - 11 - 576 + 10,
                            y=self.screen_resolution[1] // 2 + 135 + 56 - i * 101,
                            anchor_x='left', anchor_y='center', batch=self.batch,
                            group=self.groups['button_text'])

                if track_state_matrix[dictionary_keys[i]][self.track_state_unlock_available]:
                    self.description_tracks_labels[dictionary_keys[i]] \
                        = Label('Available for {} ¤'
                                .format(track_state_matrix[dictionary_keys[i]][self.track_state_price]),
                                font_name='Arial', font_size=16, color=(0, 192, 0, 255),
                                x=self.screen_resolution[0] // 2 - 11 - 576 + 10,
                                y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                anchor_x='left', anchor_y='center', batch=self.batch,
                                group=self.groups['button_text'])
                elif track_state_matrix[dictionary_keys[i]][self.track_state_under_construction]:
                    construction_time = track_state_matrix[dictionary_keys[i]][self.track_state_construction_time]
                    self.description_tracks_labels[dictionary_keys[i]] \
                        = Label('Under construction. {}h {}min left'
                                .format(construction_time // 14400, (construction_time // 240) % 60),
                                font_name='Arial', font_size=16, color=(255, 127, 0, 255),
                                x=self.screen_resolution[0] // 2 - 11 - 576 + 10,
                                y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                anchor_x='left', anchor_y='center', batch=self.batch,
                                group=self.groups['button_text'])
                else:
                    if not track_state_matrix[dictionary_keys[i]][self.track_state_unlock_condition_from_level]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Requires level {}'
                                    .format(track_state_matrix[dictionary_keys[i]][self.track_state_level]),
                                    font_name='Arial', font_size=16, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 576 + 10,
                                    y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                    anchor_x='left', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                    elif not track_state_matrix[dictionary_keys[i]][self.track_state_unlock_condition_from_environment]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Requires environment Tier X',
                                    font_name='Arial', font_size=16, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 576 + 10,
                                    y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                    anchor_x='left', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                    elif not track_state_matrix[dictionary_keys[i]][
                        self.track_state_unlock_condition_from_previous_track
                    ]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Build track {} to unlock'.format(dictionary_keys[i] - 1),
                                    font_name='Arial', font_size=16, color=(112, 112, 112, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 576 + 10,
                                    y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                    anchor_x='left', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])

                break

    @_view_is_active
    def on_unlock_track_live(self, track):
        self.locked_tracks_labels[track].delete()
        self.locked_tracks_labels.pop(track)
        for t in self.locked_tracks_labels:
            self.locked_tracks_labels[t].y += 101

        self.title_tracks_labels[track].delete()
        self.title_tracks_labels.pop(track)
        for t in self.title_tracks_labels:
            self.title_tracks_labels[t].y += 101

        self.description_tracks_labels[track].delete()
        self.description_tracks_labels.pop(track)
        for t in self.description_tracks_labels:
            self.description_tracks_labels[t].y += 101
