from logging import getLogger

from i18n import I18N_RESOURCES, ENGLISH, numbers_to_speech_en, RUSSIAN, numbers_to_speech_ru, DATIVE, NOMINATIVE, \
    GENITIVE, PREPOSITIONAL
from music_track.narrator_intro import NarratorIntro
from view import *


class NarratorView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.view'))
        self.is_speaking = False
        self.is_playing_announcement = False
        self.playback_start_time = 0
        USER_DB_CURSOR.execute('''SELECT master_volume FROM sound''')
        self.master_volume = USER_DB_CURSOR.fetchone()[0]
        self.track_number_converters = {
            ENGLISH: numbers_to_speech_en.to_cardinal,
            RUSSIAN: numbers_to_speech_ru.to_ordinal
        }
        self.on_append_window_handlers()

    @final
    @view_is_not_active
    def on_activate(self):
        super().on_activate()
        for announcement in [a for a in NARRATOR_QUEUE[self.map_id]
                             if a[ANNOUNCEMENT_TYPE] in get_announcement_types_enabled(self.dt_multiplier)]:
            announcement[ANNOUNCEMENT_LOCKED] = FALSE

    @final
    @view_is_active
    def on_deactivate(self):
        super().on_deactivate()
        for announcement in NARRATOR_QUEUE[self.map_id]:
            announcement[ANNOUNCEMENT_LOCKED] = TRUE

    @final
    def on_update(self):
        if SPEAKER.Status.RunningState == 1 and self.is_speaking:
            self.is_speaking = False
            self.is_playing_announcement = False

    @final
    def on_update_opacity(self, new_opacity):
        super().on_update_opacity(new_opacity)
        MIDI_PLAYER.on_narrator_intro_opacity_update(self.opacity)
        SPEAKER.Volume = round(self.opacity / 255 * self.master_volume)
        if self.opacity <= 0:
            SPEAKER.Speak('<silence msec="1"/>', 11)
            self.is_speaking = False
            self.is_playing_announcement = False

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        if len(NARRATOR_QUEUE[self.map_id]) > 0:
            # self.logger.debug(f'{self.game_time=}')
            # self.logger.debug(f'{NARRATOR_QUEUE[self.map_id]=}')
            if self.game_time >= NARRATOR_QUEUE[self.map_id][0][ANNOUNCEMENT_TIME] and not self.is_playing_announcement:
                self.is_playing_announcement = True
                self.playback_start_time = self.game_time
                if self.is_activated:
                    MIDI_PLAYER.add_narrator_intro(NarratorIntro())

            if self.game_time >= self.playback_start_time + self.dt_multiplier * 1.5 and self.is_playing_announcement \
                    and not self.is_speaking:
                self.on_announcement_play(NARRATOR_QUEUE[self.map_id][0])
                NARRATOR_QUEUE[self.map_id].pop(0)

    @final
    @view_is_active
    def on_announcement_play(self, announcement):
        self.is_speaking = True
        announcement_resource_location \
            = I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string'][self.current_locale]
        if announcement[ANNOUNCEMENT_TYPE] == PASS_THROUGH_ANNOUNCEMENT:
            SPEAKER.Speak(
                announcement_resource_location.format(
                    self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_TRACK_NUMBER], DATIVE)
                ), 9
            )
        elif announcement[ANNOUNCEMENT_TYPE] in (ARRIVAL_ANNOUNCEMENT, ARRIVAL_FINISHED_ANNOUNCEMENT):
            SPEAKER.Speak(
                announcement_resource_location.format(
                    announcement[ANNOUNCEMENT_TRAIN_ID],
                    self.track_number_converters[self.current_locale](
                        announcement[ANNOUNCEMENT_TRACK_NUMBER], NOMINATIVE
                    )
                ), 9
            )
        elif announcement[ANNOUNCEMENT_TYPE] == DEPARTURE_ANNOUNCEMENT:
            track_number_category = 'other'
            if self.current_locale == RUSSIAN and announcement[ANNOUNCEMENT_TRACK_NUMBER] == 2:
                track_number_category = 'two'

            SPEAKER.Speak(
                announcement_resource_location[track_number_category].format(
                    announcement[ANNOUNCEMENT_TRAIN_ID],
                    self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_TRACK_NUMBER], GENITIVE)
                ), 9
            )
        elif announcement[ANNOUNCEMENT_TYPE] == FIVE_MINUTES_LEFT_ANNOUNCEMENT:
            SPEAKER.Speak(
                announcement_resource_location.format(
                    announcement[ANNOUNCEMENT_TRAIN_ID],
                    self.track_number_converters[self.current_locale](
                        announcement[ANNOUNCEMENT_TRACK_NUMBER], PREPOSITIONAL
                    )
                ), 9
            )
