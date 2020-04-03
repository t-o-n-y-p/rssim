import ctypes
from operator import itemgetter
from time import perf_counter

from score import *

MESSAGE_VOLUME: Final = 0
MESSAGE_PAYLOAD: Final = 1
MESSAGE_TIME: Final = 2

NOTE_ON_MESSAGE_ID: Final = 0x90
NOTE_OFF_MESSAGE_ID: Final = 0x80


class MusicTrack:
    def __init__(self, score_sheet, logger, tempo=120):
        self.logger = logger
        self.is_playing = False
        self.playback_finish_callback = None
        self.tempo = tempo
        self.playback_start_time = 0.0
        self.messages = []
        score = score_sheet.get_score()
        for note in score:
            self.messages.append([
                note[NOTE_VOLUME], note[NOTE_TONE] << 8 | NOTE_ON_MESSAGE_ID | note[NOTE_INSTRUMENT].channel_id,
                float(note[NOTE_OFFSET] / Fraction(1, 4) * Fraction(60 / self.tempo))
            ])
            self.messages.append([
                note[NOTE_VOLUME], note[NOTE_TONE] << 8 | NOTE_OFF_MESSAGE_ID | note[NOTE_INSTRUMENT].channel_id,
                float((note[NOTE_OFFSET] + note[NOTE_DURATION]) / Fraction(1, 4) * Fraction(60 / self.tempo))
            ])

        self.messages = sorted(self.messages, key=itemgetter(MESSAGE_TIME))

    @final
    def on_tempo_update(self, tempo):
        for m in self.messages:
            m[MESSAGE_TIME] /= (tempo / self.tempo)

        self.tempo = tempo

    @final
    def play(self, midi_device, volume_multiplier):
        if not self.is_playing and len(self.messages) > 0:
            self.is_playing = True
            self.playback_start_time = perf_counter()

        if self.is_playing:
            while self.messages[0][MESSAGE_TIME] <= perf_counter() - self.playback_start_time:
                ctypes.windll.winmm.midiOutShortMsg(
                    midi_device,
                    round(self.messages[0][MESSAGE_VOLUME] * volume_multiplier)
                    << 16 | self.messages[0][MESSAGE_PAYLOAD]
                )
                self.messages.pop(0)
                if len(self.messages) == 0:
                    self.is_playing = False
                    self.playback_finish_callback()
                    break
