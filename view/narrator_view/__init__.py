from logging import getLogger

from i18n import I18N_RESOURCES, ENGLISH, numbers_to_speech_en, RUSSIAN, numbers_to_speech_ru, DATIVE, NOMINATIVE, \
    GENITIVE
from music_track.narrator_intro import NarratorIntro
from view import *
from database import NARRATOR_QUEUE


class NarratorView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.view'))
        self.narrator_queue = NARRATOR_QUEUE[self.map_id]
        self.is_speaking = False
        self.is_playing_announcement = False
        self.playback_start_time = 0
        self.track_number_converters = {
            ENGLISH: numbers_to_speech_en.to_cardinal,
            RUSSIAN: numbers_to_speech_ru.to_ordinal
        }
        self.on_append_window_handlers()

    @final
    def on_update(self):
        if SPEAKER.Status.RunningState == 1 and self.is_speaking:
            self.is_speaking = False
            self.is_playing_announcement = False

    @final
    def on_update_time(self, dt):
        super().on_update_time(dt)
        if len(self.narrator_queue) > 0:
            self.logger.debug(f'{self.game_time=}')
            self.logger.debug(f'{self.narrator_queue=}')
            if self.game_time >= self.narrator_queue[0][ANNOUNCEMENT_TIME] and not self.is_playing_announcement:
                self.is_playing_announcement = True
                self.playback_start_time = self.game_time
                MIDI_PLAYER.add_narrator_intro(NarratorIntro())

            if self.game_time >= self.playback_start_time + self.dt_multiplier * 1.5 and self.is_playing_announcement:
                self.on_announcement_play(self.narrator_queue[0])
                self.narrator_queue.pop(0)

    @final
    @view_is_active
    def on_announcement_play(self, announcement):
        self.is_speaking = True
        if announcement[ANNOUNCEMENT_TYPE] == PASS_THROUGH_ANNOUNCEMENT:
            SPEAKER.Speak(
                I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string'][self.current_locale]
                .format(self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_TRACK_NUMBER],
                                                                          DATIVE)),
                9
            )
        elif announcement[ANNOUNCEMENT_TYPE] in (ARRIVAL_ANNOUNCEMENT, ARRIVAL_FINISHED_ANNOUNCEMENT):
            SPEAKER.Speak(
                I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string'][self.current_locale]
                .format(announcement[ANNOUNCEMENT_TRAIN_ID],
                        self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_TRACK_NUMBER],
                                                                          NOMINATIVE)),
                9
            )
        elif announcement[ANNOUNCEMENT_TYPE] == DEPARTURE_ANNOUNCEMENT:
            track_number_category = 'other'
            if self.current_locale == RUSSIAN and announcement[ANNOUNCEMENT_TRACK_NUMBER] == 2:
                track_number_category = 'two'

            SPEAKER.Speak(
                I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string']
                [self.current_locale][track_number_category]
                .format(announcement[ANNOUNCEMENT_TRAIN_ID],
                        self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_TRACK_NUMBER],
                                                                          GENITIVE)),
                9
            )
