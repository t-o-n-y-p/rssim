from pyglet.text import Label
from pyglet.image import load
from pyglet.sprite import Sprite

from .view_base import View
from .button import CloseConstructorButton


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


class ConstructorView(View):
    def __init__(self, user_db_cursor, config_db_cursor, surface, batch, groups):
        def on_close_constructor(button):
            self.controller.on_deactivate_view()

        super().__init__(user_db_cursor, config_db_cursor, surface, batch, groups)
        self.screen_resolution = (1280, 720)
        self.background_image = load('img/constructor/constructor_1280_720.png')
        self.background_sprite = None
        self.locked_tracks_labels = {}
        self.title_tracks_labels = {}
        self.description_tracks_labels = {}
        self.buttons_tracks_labels = {}
        self.no_more_tracks_available_labels = []
        self.coming_soon_environment_labels = []
        self.close_constructor_button = CloseConstructorButton(surface=self.surface, batch=self.batch,
                                                               groups=self.groups, on_click_action=on_close_constructor)
        self.buttons.append(self.close_constructor_button)
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
            = [Label('Coming soon', font_name='Arial', font_size=22, color=(96, 96, 96, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 - 168 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']),
               Label('Coming soon', font_name='Arial', font_size=22, color=(96, 96, 96, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 - 67 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']),
               Label('Coming soon', font_name='Arial', font_size=22, color=(96, 96, 96, 255),
                     x=self.screen_resolution[0] // 2 + 11 + 288, y=self.screen_resolution[1] // 2 + 34 + 40,
                     anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text']),
               Label('Coming soon', font_name='Arial', font_size=22, color=(96, 96, 96, 255),
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
                    Label('No more track available', font_name='Arial', font_size=22, color=(96, 96, 96, 255),
                          x=self.screen_resolution[0] // 2 - 11 - 288,
                          y=self.screen_resolution[1] // 2 - 168 + 40 + len(self.no_more_tracks_available_labels) * 101,
                          anchor_x='center', anchor_y='center', batch=self.batch, group=self.groups['button_text'])
                )

        for i in range(available_options):
            if dictionary_keys[i] not in self.locked_tracks_labels:
                if track_state_matrix[dictionary_keys[i]][self.track_state_unlock_available] \
                        or track_state_matrix[dictionary_keys[i]][self.track_state_under_construction]:
                    self.locked_tracks_labels[dictionary_keys[i]] \
                        = Label('', font_name='Webdings', font_size=40, color=(255, 255, 255, 255),
                                x=self.screen_resolution[0] // 2 - 11 - 576 + 40,
                                y=self.screen_resolution[1] // 2 - 168 + 40 + i * 101,
                                anchor_x='center', anchor_y='center', batch=self.batch,
                                group=self.groups['button_text'])
                else:
                    self.locked_tracks_labels[dictionary_keys[i]] \
                        = Label('', font_name='Webdings', font_size=40, color=(96, 96, 96, 255),
                                x=self.screen_resolution[0] // 2 - 11 - 576 + 40,
                                y=self.screen_resolution[1] // 2 - 168 + 40 + i * 101,
                                anchor_x='center', anchor_y='center', batch=self.batch,
                                group=self.groups['button_text'])

                self.title_tracks_labels[dictionary_keys[i]] \
                    = Label(f'Track {dictionary_keys[i]}', font_name='Arial', font_size=24, color=(255, 255, 255, 255),
                            x=self.screen_resolution[0] // 2 - 11 - 576 + 90,
                            y=self.screen_resolution[1] // 2 + 135 + 56 - i * 101,
                            anchor_x='left', anchor_y='center', batch=self.batch,
                            group=self.groups['button_text'])

                if track_state_matrix[dictionary_keys[i]][self.track_state_unlock_available]:
                    n = 1
                elif track_state_matrix[dictionary_keys[i]][self.track_state_under_construction]:
                    n = 1
                else:
                    if not track_state_matrix[dictionary_keys[i]][self.track_state_unlock_condition_from_level]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Requires level {}'
                                    .format(track_state_matrix[dictionary_keys[i]][self.track_state_level]),
                                    font_name='Arial', font_size=16, color=(96, 96, 96, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 576 + 90,
                                    y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                    anchor_x='left', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                    elif not track_state_matrix[dictionary_keys[i]][self.track_state_unlock_condition_from_environment]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Requires environment Tier X',
                                    font_name='Arial', font_size=16, color=(96, 96, 96, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 576 + 90,
                                    y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                    anchor_x='left', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
                    elif not track_state_matrix[dictionary_keys[i]][
                        self.track_state_unlock_condition_from_previous_track
                    ]:
                        self.description_tracks_labels[dictionary_keys[i]] \
                            = Label('Build track {} to unlock'.format(dictionary_keys[i] - 1),
                                    font_name='Arial', font_size=16, color=(96, 96, 96, 255),
                                    x=self.screen_resolution[0] // 2 - 11 - 576 + 90,
                                    y=self.screen_resolution[1] // 2 + 135 + 21 - i * 101,
                                    anchor_x='left', anchor_y='center', batch=self.batch,
                                    group=self.groups['button_text'])
