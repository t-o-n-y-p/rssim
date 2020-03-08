from fractions import Fraction
from typing import final, Final

NOTE_TONE: Final = 0
NOTE_DURATION: Final = 1
NOTE_VOLUME: Final = 2
NOTE_OFFSET: Final = 3
NOTE_INSTRUMENT: Final = 4

C0: Final = 12
CIS0: Final = 13
CISIS0: Final = 14
DESES0: Final = 12
DES0: Final = 13
D0: Final = 14
DIS0: Final = 15
DISIS0: Final = 16
ESES0: Final = 14
ES0: Final = 15
E0: Final = 16
EIS0: Final = 17
EISIS0: Final = 18
FESES0: Final = 15
FES0: Final = 16
F0: Final = 17
FIS0: Final = 18
FISIS0: Final = 19
GESES0: Final = 17
GES0: Final = 18
G0: Final = 19
GIS0: Final = 20
GISIS0: Final = 21
ASAS0: Final = 19
AS0: Final = 20
A0: Final = 21
AIS0: Final = 22
AISIS0: Final = 23
HESES0: Final = 21
B0: Final = 22
H0: Final = 23
HIS0: Final = 24
HISIS0: Final = 25
CESES1: Final = 22
CES1: Final = 23
C1: Final = 24
CIS1: Final = 25
CISIS1: Final = 26
DESES1: Final = 24
DES1: Final = 25
D1: Final = 26
DIS1: Final = 27
DISIS1: Final = 28
ESES1: Final = 26
ES1: Final = 27
E1: Final = 28
EIS1: Final = 29
EISIS1: Final = 30
FESES1: Final = 27
FES1: Final = 28
F1: Final = 29
FIS1: Final = 30
FISIS1: Final = 31
GESES1: Final = 29
GES1: Final = 30
G1: Final = 31
GIS1: Final = 32
GISIS1: Final = 33
ASAS1: Final = 31
AS1: Final = 32
A1: Final = 33
AIS1: Final = 34
AISIS1: Final = 35
HESES1: Final = 33
B1: Final = 34
H1: Final = 35
HIS1: Final = 36
HISIS1: Final = 37
CESES2: Final = 34
CES2: Final = 35
C2: Final = 36
CIS2: Final = 37
CISIS2: Final = 38
DESES2: Final = 36
DES2: Final = 37
D2: Final = 38
DIS2: Final = 39
DISIS2: Final = 40
ESES2: Final = 38
ES2: Final = 39
E2: Final = 40
EIS2: Final = 41
EISIS2: Final = 42
FESES2: Final = 39
FES2: Final = 40
F2: Final = 41
FIS2: Final = 42
FISIS2: Final = 43
GESES2: Final = 41
GES2: Final = 42
G2: Final = 43
GIS2: Final = 44
GISIS2: Final = 45
ASAS2: Final = 43
AS2: Final = 44
A2: Final = 45
AIS2: Final = 46
AISIS2: Final = 47
HESES2: Final = 45
B2: Final = 46
H2: Final = 47
HIS2: Final = 48
HISIS2: Final = 49
CESES3: Final = 46
CES3: Final = 47
C3: Final = 48
CIS3: Final = 49
CISIS3: Final = 50
DESES3: Final = 48
DES3: Final = 49
D3: Final = 50
DIS3: Final = 51
DISIS3: Final = 52
ESES3: Final = 50
ES3: Final = 51
E3: Final = 52
EIS3: Final = 53
EISIS3: Final = 54
FESES3: Final = 51
FES3: Final = 52
F3: Final = 53
FIS3: Final = 54
FISIS3: Final = 55
GESES3: Final = 53
GES3: Final = 54
G3: Final = 55
GIS3: Final = 56
GISIS3: Final = 57
ASAS3: Final = 55
AS3: Final = 56
A3: Final = 57
AIS3: Final = 58
AISIS3: Final = 59
HESES3: Final = 57
B3: Final = 58
H3: Final = 59
HIS3: Final = 60
HISIS3: Final = 61
CESES4: Final = 58
CES4: Final = 59
C4: Final = 60
CIS4: Final = 61
CISIS4: Final = 62
DESES4: Final = 60
DES4: Final = 61
D4: Final = 62
DIS4: Final = 63
DISIS4: Final = 64
ESES4: Final = 62
ES4: Final = 63
E4: Final = 64
EIS4: Final = 65
EISIS4: Final = 66
FESES4: Final = 63
FES4: Final = 64
F4: Final = 65
FIS4: Final = 66
FISIS4: Final = 67
GESES4: Final = 65
GES4: Final = 66
G4: Final = 67
GIS4: Final = 68
GISIS4: Final = 69
ASAS4: Final = 67
AS4: Final = 68
A4: Final = 69
AIS4: Final = 70
AISIS4: Final = 71
HESES4: Final = 69
B4: Final = 70
H4: Final = 71
HIS4: Final = 72
HISIS4: Final = 73
CESES5: Final = 70
CES5: Final = 71
C5: Final = 72
CIS5: Final = 73
CISIS5: Final = 74
DESES5: Final = 72
DES5: Final = 73
D5: Final = 74
DIS5: Final = 75
DISIS5: Final = 76
ESES5: Final = 74
ES5: Final = 75
E5: Final = 76
EIS5: Final = 77
EISIS5: Final = 78
FESES5: Final = 75
FES5: Final = 76
F5: Final = 77
FIS5: Final = 78
FISIS5: Final = 79
GESES5: Final = 77
GES5: Final = 78
G5: Final = 79
GIS5: Final = 80
GISIS5: Final = 81
ASAS5: Final = 79
AS5: Final = 80
A5: Final = 81
AIS5: Final = 82
AISIS5: Final = 83
HESES5: Final = 81
B5: Final = 82
H5: Final = 83
HIS5: Final = 84
HISIS5: Final = 85
CESES6: Final = 82
CES6: Final = 83
C6: Final = 84
CIS6: Final = 85
CISIS6: Final = 86
DESES6: Final = 84
DES6: Final = 85
D6: Final = 86
DIS6: Final = 87
DISIS6: Final = 88
ESES6: Final = 86
ES6: Final = 87
E6: Final = 88
EIS6: Final = 89
EISIS6: Final = 90
FESES6: Final = 87
FES6: Final = 88
F6: Final = 89
FIS6: Final = 90
FISIS6: Final = 91
GESES6: Final = 89
GES6: Final = 90
G6: Final = 91
GIS6: Final = 92
GISIS6: Final = 93
ASAS6: Final = 91
AS6: Final = 92
A6: Final = 93
AIS6: Final = 94
AISIS6: Final = 95
HESES6: Final = 93
B6: Final = 94
H6: Final = 95
HIS6: Final = 96
HISIS6: Final = 97
CESES7: Final = 94
CES7: Final = 95
C7: Final = 96
CIS7: Final = 97
CISIS7: Final = 98
DESES7: Final = 96
DES7: Final = 97
D7: Final = 98
DIS7: Final = 99
DISIS7: Final = 100
ESES7: Final = 98
ES7: Final = 99
E7: Final = 100
EIS7: Final = 101
EISIS7: Final = 102
FESES7: Final = 99
FES7: Final = 100
F7: Final = 101
FIS7: Final = 102
FISIS7: Final = 103
GESES7: Final = 101
GES7: Final = 102
G7: Final = 103
GIS7: Final = 104
GISIS7: Final = 105
ASAS7: Final = 103
AS7: Final = 104
A7: Final = 105
AIS7: Final = 106
AISIS7: Final = 107
HESES7: Final = 105
B7: Final = 106
H7: Final = 107
HIS7: Final = 108
HISIS7: Final = 109
CESES8: Final = 106
CES8: Final = 107
C8: Final = 108
CIS8: Final = 109
CISIS8: Final = 110
DESES8: Final = 108
DES8: Final = 109
D8: Final = 110
DIS8: Final = 111
DISIS8: Final = 112
ESES8: Final = 110
ES8: Final = 111
E8: Final = 112
EIS8: Final = 113
EISIS8: Final = 114
FESES8: Final = 111
FES8: Final = 112
F8: Final = 113
FIS8: Final = 114
FISIS8: Final = 115
GESES8: Final = 113
GES8: Final = 114
G8: Final = 115
GIS8: Final = 116
GISIS8: Final = 117
ASAS8: Final = 115
AS8: Final = 116
A8: Final = 117
AIS8: Final = 118
AISIS8: Final = 119
HESES8: Final = 117
B8: Final = 118
H8: Final = 119
HIS8: Final = 120
HISIS8: Final = 121
CESES9: Final = 118
CES9: Final = 119
C9: Final = 120

WHOLE: Final = Fraction(1, 1)
WHOLE_DOTTED: Final = Fraction(3, 2)
WHOLE_DOUBLE_DOTTED: Final = Fraction(7, 4)
WHOLE_TRIPLE_DOTTED: Final = Fraction(15, 8)
HALF: Final = Fraction(1, 2)
HALF_DOTTED: Final = Fraction(3, 4)
HALF_DOUBLE_DOTTED: Final = Fraction(7, 8)
HALF_TRIPLE_DOTTED: Final = Fraction(15, 16)
QUARTER: Final = Fraction(1, 4)
QUARTER_DOTTED: Final = Fraction(3, 8)
QUARTER_DOUBLE_DOTTED: Final = Fraction(7, 16)
QUARTER_TRIPLE_DOTTED: Final = Fraction(15, 32)
EIGHTH: Final = Fraction(1, 8)
EIGHTH_DOTTED: Final = Fraction(3, 16)
EIGHTH_DOUBLE_DOTTED: Final = Fraction(7, 32)
EIGHTH_TRIPLE_DOTTED: Final = Fraction(15, 64)
SIXTEENTH: Final = Fraction(1, 16)
SIXTEENTH_DOTTED: Final = Fraction(3, 32)
SIXTEENTH_DOUBLE_DOTTED: Final = Fraction(7, 64)
SIXTEENTH_TRIPLE_DOTTED: Final = Fraction(15, 128)
THIRTY_SECOND: Final = Fraction(1, 32)
THIRTY_SECOND_DOTTED: Final = Fraction(3, 64)
THIRTY_SECOND_DOUBLE_DOTTED: Final = Fraction(7, 128)
THIRTY_SECOND_TRIPLE_DOTTED: Final = Fraction(15, 256)
SIXTY_FOURTH: Final = Fraction(1, 64)
SIXTY_FOURTH_DOTTED: Final = Fraction(3, 128)
SIXTY_FOURTH_DOUBLE_DOTTED: Final = Fraction(7, 256)
SIXTY_FOURTH_TRIPLE_DOTTED: Final = Fraction(15, 512)
HUNDRED_TWENTY_EIGHTH: Final = Fraction(1, 128)
HUNDRED_TWENTY_EIGHTH_DOTTED: Final = Fraction(3, 256)
HUNDRED_TWENTY_EIGHTH_DOUBLE_DOTTED: Final = Fraction(7, 512)
HUNDRED_TWENTY_EIGHTH_TRIPLE_DOTTED: Final = Fraction(15, 1024)
TWO_HUNDRED_FIFTY_SIXTH: Final = Fraction(1, 256)
TWO_HUNDRED_FIFTY_SIXTH_DOTTED: Final = Fraction(3, 512)
TWO_HUNDRED_FIFTY_SIXTH_DOUBLE_DOTTED: Final = Fraction(7, 1024)
TWO_HUNDRED_FIFTY_SIXTH_TRIPLE_DOTTED: Final = Fraction(15, 2048)


def get_tuplet(value, tuplet_size, normal_size):
    return value * normal_size / tuplet_size


@final
class Note:
    def __init__(self, tone, duration, volume, offset):
        self.tone = tone
        self.duration = duration
        self.volume = volume
        self.offset = offset

    def get_score(self, instrument):
        return [self.tone, self.duration, self.volume, self.offset, instrument]


@final
class Bar:
    def __init__(self, time_signature, notes=()):
        self.time_signature = time_signature
        self.notes = notes

    def get_score(self, instrument):
        score = []
        for n in self.notes:
            score.append(n.get_score(instrument))

        return score

    def on_offset_update(self, offset):
        for n in self.notes:
            n.offset += offset


@final
class Staff:
    def __init__(self, instrument, bars):
        self.instrument = instrument
        self.bars = bars
        for i in range(len(self.bars) - 1):
            for j in range(i + 1, len(self.bars)):
                self.bars[j].on_offset_update(self.bars[i].time_signature)

    def get_score(self):
        score = []
        for b in self.bars:
            score.extend(b.get_score(self.instrument))

        return score


@final
class ScoreSheet:
    def __init__(self, staves):
        self.staves = staves

    def get_score(self):
        score = []
        for s in self.staves:
            score.extend(s.get_score())

        return score
