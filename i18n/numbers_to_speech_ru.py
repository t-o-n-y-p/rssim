from typing import Final

from i18n import value_between_1_and_99, NOMINATIVE, GENITIVE, DATIVE, PREPOSITIONAL

ONE_WORD_CARDINAL: Final = {
    1: 'один',
    2: 'два',
    3: 'три',
    4: 'четыре',
    5: 'пять',
    6: 'шесть',
    7: 'семь',
    8: 'восемь',
    9: 'девять',
    10: 'десять',
    11: 'одиннадцать',
    12: 'двенадцать',
    13: 'тринадцать',
    14: 'четырнадцать',
    15: 'пятнадцать',
    16: 'шестнадцать',
    17: 'семнадцать',
    18: 'восемнадцать',
    19: 'девятнадцать',
    20: 'двадцать',
    30: 'тридцать',
    40: 'сорок',
    50: 'пятьдесят',
    60: 'шестьдесят',
    70: 'семьдесят',
    80: 'восемьдесят',
    90: 'девяносто'
}
ONE_WORD_ORDINAL: Final = {
    ONE_WORD_CARDINAL[1]: {
        NOMINATIVE: 'первый',
        GENITIVE: 'первого',
        DATIVE: 'первому',
        PREPOSITIONAL: 'первом'
    },
    ONE_WORD_CARDINAL[2]: {
        NOMINATIVE: 'второй',
        GENITIVE: 'второго',
        DATIVE: 'второму',
        PREPOSITIONAL: 'втором'
    },
    ONE_WORD_CARDINAL[3]: {
        NOMINATIVE: 'третий',
        GENITIVE: 'третьего',
        DATIVE: 'третьему',
        PREPOSITIONAL: 'третьем'
    },
    ONE_WORD_CARDINAL[4]: {
        NOMINATIVE: 'четвёртый',
        GENITIVE: 'четвёртого',
        DATIVE: 'четвёртому',
        PREPOSITIONAL: 'четвёртом'
    },
    ONE_WORD_CARDINAL[5]: {
        NOMINATIVE: 'пятый',
        GENITIVE: 'пятого',
        DATIVE: 'пятому',
        PREPOSITIONAL: 'пятом'
    },
    ONE_WORD_CARDINAL[6]: {
        NOMINATIVE: 'шестой',
        GENITIVE: 'шестого',
        DATIVE: 'шестому',
        PREPOSITIONAL: 'шестом'
    },
    ONE_WORD_CARDINAL[7]: {
        NOMINATIVE: 'седьмой',
        GENITIVE: 'седьмого',
        DATIVE: 'седьмому',
        PREPOSITIONAL: 'седьмом'
    },
    ONE_WORD_CARDINAL[8]: {
        NOMINATIVE: 'восьмой',
        GENITIVE: 'восьмого',
        DATIVE: 'восьмому',
        PREPOSITIONAL: 'восьмом'
    },
    ONE_WORD_CARDINAL[9]: {
        NOMINATIVE: 'девятый',
        GENITIVE: 'девятого',
        DATIVE: 'девятому',
        PREPOSITIONAL: 'девятом'
    },
    ONE_WORD_CARDINAL[10]: {
        NOMINATIVE: 'десятый',
        GENITIVE: 'десятого',
        DATIVE: 'десятому',
        PREPOSITIONAL: 'десятом'
    },
    ONE_WORD_CARDINAL[11]: {
        NOMINATIVE: 'одиннадцатый',
        GENITIVE: 'одиннадцатого',
        DATIVE: 'одиннадцатому',
        PREPOSITIONAL: 'одиннадцатом'
    },
    ONE_WORD_CARDINAL[12]: {
        NOMINATIVE: 'двенадцатый',
        GENITIVE: 'двенадцатого',
        DATIVE: 'двенадцатому',
        PREPOSITIONAL: 'двенадцатом'
    },
    ONE_WORD_CARDINAL[13]: {
        NOMINATIVE: 'тринадцатый',
        GENITIVE: 'тринадцатого',
        DATIVE: 'тринадцатому',
        PREPOSITIONAL: 'тринадцатом'
    },
    ONE_WORD_CARDINAL[14]: {
        NOMINATIVE: 'четырнадцатый',
        GENITIVE: 'четырнадцатого',
        DATIVE: 'четырнадцатому',
        PREPOSITIONAL: 'четырнадцатом'
    },
    ONE_WORD_CARDINAL[15]: {
        NOMINATIVE: 'пятнадцатый',
        GENITIVE: 'пятнадцатого',
        DATIVE: 'пятнадцатому',
        PREPOSITIONAL: 'пятнадцатом'
    },
    ONE_WORD_CARDINAL[16]: {
        NOMINATIVE: 'шестнадцатый',
        GENITIVE: 'шестнадцатого',
        DATIVE: 'шестнадцатому',
        PREPOSITIONAL: 'шестнадцатом'
    },
    ONE_WORD_CARDINAL[17]: {
        NOMINATIVE: 'семнадцатый',
        GENITIVE: 'семнадцатого',
        DATIVE: 'семнадцатому',
        PREPOSITIONAL: 'семнадцатом'
    },
    ONE_WORD_CARDINAL[18]: {
        NOMINATIVE: 'восемнадцатый',
        GENITIVE: 'восемнадцатого',
        DATIVE: 'восемнадцатому',
        PREPOSITIONAL: 'восемнадцатом'
    },
    ONE_WORD_CARDINAL[19]: {
        NOMINATIVE: 'девятнадцатый',
        GENITIVE: 'девятнадцатого',
        DATIVE: 'девятнадцатому',
        PREPOSITIONAL: 'девятнадцатом'
    },
    ONE_WORD_CARDINAL[20]: {
        NOMINATIVE: 'двадцатый',
        GENITIVE: 'двадцатого',
        DATIVE: 'двадцатому',
        PREPOSITIONAL: 'двадцатом'
    },
    ONE_WORD_CARDINAL[30]: {
        NOMINATIVE: 'тридцатый',
        GENITIVE: 'тридцатого',
        DATIVE: 'тридцатому',
        PREPOSITIONAL: 'тридцатом'
    },
    ONE_WORD_CARDINAL[40]: {
        NOMINATIVE: 'сороковой',
        GENITIVE: 'сорокового',
        DATIVE: 'сороковому',
        PREPOSITIONAL: 'сороковом'
    },
    ONE_WORD_CARDINAL[50]: {
        NOMINATIVE: 'пятидесятый',
        GENITIVE: 'пятидесятого',
        DATIVE: 'пятидесятому',
        PREPOSITIONAL: 'пятидесятом'
    },
    ONE_WORD_CARDINAL[60]: {
        NOMINATIVE: 'шестидесятый',
        GENITIVE: 'шестидесятого',
        DATIVE: 'шестидесятому',
        PREPOSITIONAL: 'шестидесятом'
    },
    ONE_WORD_CARDINAL[70]: {
        NOMINATIVE: 'семидесятый',
        GENITIVE: 'семидесятого',
        DATIVE: 'семидесятому',
        PREPOSITIONAL: 'семидесятом'
    },
    ONE_WORD_CARDINAL[80]: {
        NOMINATIVE: 'восьмидесятый',
        GENITIVE: 'восьмидесятого',
        DATIVE: 'восьмидесятому',
        PREPOSITIONAL: 'восьмидесятом'
    },
    ONE_WORD_CARDINAL[90]: {
        NOMINATIVE: 'девяностый',
        GENITIVE: 'девяностого',
        DATIVE: 'девяностому',
        PREPOSITIONAL: 'девяностом'
    }
}


@value_between_1_and_99
def to_cardinal(value, case):
    try:
        return ONE_WORD_CARDINAL[value]
    except KeyError:
        nearest_one_word_number = max(k for k in ONE_WORD_CARDINAL if k < value)
        return ONE_WORD_CARDINAL[nearest_one_word_number] + ' ' + to_cardinal(value - nearest_one_word_number, case)


@value_between_1_and_99
def to_ordinal(value, case):
    result = to_cardinal(value, case)
    for last_word in ONE_WORD_ORDINAL:
        if result.endswith(last_word):
            return result[:-len(last_word)] + ONE_WORD_ORDINAL[last_word][case]
