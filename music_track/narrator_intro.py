from fractions import Fraction
from logging import getLogger
from typing import final, Final

from midi_player.instruments import Harp
from music_track import MusicTrack
from score import ScoreSheet, Staff, Bar, Note, G4, H4, D5, G5, QUARTER_DOTTED, THIRTY_SECOND


@final
class NarratorIntro(MusicTrack):
    NARRATOR_INTRO_SCORE_SHEET: Final = ScoreSheet(
        [
            Staff(
                Harp(),
                [
                    Bar(
                        Fraction(4, 4),
                        [
                            Note(G4, duration=QUARTER_DOTTED, volume=127, offset=0),
                            Note(H4, duration=QUARTER_DOTTED, volume=105, offset=THIRTY_SECOND),
                            Note(D5, duration=QUARTER_DOTTED, volume=84, offset=THIRTY_SECOND * 2),
                            Note(G5, duration=QUARTER_DOTTED, volume=63, offset=THIRTY_SECOND * 3)
                        ]
                    )
                ]
            )
        ]
    )

    def __init__(self):
        super().__init__(self.NARRATOR_INTRO_SCORE_SHEET, logger=getLogger('root.narrator_intro'))
