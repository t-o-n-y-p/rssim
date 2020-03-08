from midi_player.instruments import Harp
from music_track import *

NARRATOR_INTRO_SCORE_SHEET: Final = ScoreSheet(
    [
        Staff(Harp(), [
            Bar(Fraction(4, 4), [
                Note(C4, WHOLE, 127, 0),
                Note(E4, WHOLE, 127, SIXTEENTH),
                Note(G4, WHOLE, 127, SIXTEENTH * 2),
                Note(C5, WHOLE, 127, SIXTEENTH * 3)
            ])
        ])
    ]
)


class NarratorIntro(MusicTrack):
    def __init__(self):
        super().__init__(NARRATOR_INTRO_SCORE_SHEET)
