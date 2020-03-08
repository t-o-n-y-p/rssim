from logging import getLogger

from midi_player.instruments import Harp
from music_track import *

NARRATOR_INTRO_SCORE_SHEET: Final = ScoreSheet(
    [
        Staff(Harp(), [
            Bar(Fraction(4, 4), [
                Note(G4, duration=QUARTER_DOTTED, volume=127, offset=0),
                Note(H4, duration=QUARTER_DOTTED, volume=105, offset=THIRTY_SECOND),
                Note(D5, duration=QUARTER_DOTTED, volume=84, offset=THIRTY_SECOND * 2),
                Note(G5, duration=QUARTER_DOTTED, volume=63, offset=THIRTY_SECOND * 3)
            ])
        ])
    ]
)


@final
class NarratorIntro(MusicTrack):
    def __init__(self):
        super().__init__(NARRATOR_INTRO_SCORE_SHEET, logger=getLogger('root.narrator_intro'))
