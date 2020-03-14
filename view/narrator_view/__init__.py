from logging import getLogger

from i18n import I18N_RESOURCES, ENGLISH, numbers_to_speech_en, RUSSIAN, numbers_to_speech_ru, DATIVE, NOMINATIVE, \
    GENITIVE
from music_track.narrator_intro import NarratorIntro
from view import *


class NarratorView(MapBaseView, ABC):
    def __init__(self, controller, map_id):
        super().__init__(controller, map_id, logger=getLogger(f'root.app.game.map.{map_id}.narrator.view'))
        self.narrator_queue = NARRATOR_QUEUE[self.map_id]
        self.is_speaking = False
        self.track_number_converters = {
            ENGLISH: numbers_to_speech_en.to_cardinal,
            RUSSIAN: numbers_to_speech_ru.to_ordinal
        }
        self.on_append_window_handlers()

    @final
    def on_update(self):
        if SPEAKER.Status.RunningState == 1 and self.is_speaking:
            self.is_speaking = False
            self.controller.on_announcement_playback_finish()

    @final
    @view_is_active
    def on_narrator_intro_play(self):
        MIDI_PLAYER.add_narrator_intro(NarratorIntro())

    @final
    @view_is_active
    def on_announcement_play(self, announcement):
        self.is_speaking = True
        if announcement[ANNOUNCEMENT_TYPE] == PASS_THROUGH_ANNOUNCEMENT:
            SPEAKER.Speak(
                I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string'][self.current_locale]
                .format(
                    self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_ARGUMENTS][0], DATIVE)),
                1
            )
        elif announcement[ANNOUNCEMENT_TYPE] in (ARRIVAL_ANNOUNCEMENT, ARRIVAL_FINISHED_ANNOUNCEMENT):
            SPEAKER.Speak(
                I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string'][self.current_locale]
                .format(' '.join(str(announcement[ANNOUNCEMENT_ARGUMENTS][0])),
                        self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_ARGUMENTS][1],
                                                                          NOMINATIVE)),
                1
            )
        elif announcement[ANNOUNCEMENT_TYPE] == DEPARTURE_ANNOUNCEMENT:
            track_number_category = 'other'
            if self.current_locale == RUSSIAN and announcement[ANNOUNCEMENT_ARGUMENTS][1] == 2:
                track_number_category = 'two'

            SPEAKER.Speak(
                I18N_RESOURCES[announcement[ANNOUNCEMENT_TYPE] + '_announcement_string']
                [self.current_locale][track_number_category]
                .format(' '.join(str(announcement[ANNOUNCEMENT_ARGUMENTS][0])),
                        self.track_number_converters[self.current_locale](announcement[ANNOUNCEMENT_ARGUMENTS][1],
                                                                          GENITIVE)),
                1
            )
