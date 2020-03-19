from typing import Final

from i18n import value_between_1_and_99

ONE_WORD_CARDINAL: Final = {
    1: 'one',
    2: 'two',
    3: 'three',
    4: 'four',
    5: 'five',
    6: 'six',
    7: 'seven',
    8: 'eight',
    9: 'nine',
    10: 'ten',
    11: 'eleven',
    12: 'twelve',
    13: 'thirteen',
    14: 'fourteen',
    15: 'fifteen',
    16: 'sixteen',
    17: 'seventeen',
    18: 'eighteen',
    19: 'nineteen',
    20: 'twenty',
    30: 'thirty',
    40: 'forty',
    50: 'fifty',
    60: 'sixty',
    70: 'seventy',
    80: 'eighty',
    90: 'ninety'
}


@value_between_1_and_99
def to_cardinal(value, case):
    try:
        return ONE_WORD_CARDINAL[value]
    except KeyError:
        nearest_one_word_number = max(k for k in ONE_WORD_CARDINAL if k < value)
        return ONE_WORD_CARDINAL[nearest_one_word_number] + '-' + to_cardinal(value - nearest_one_word_number, case)
