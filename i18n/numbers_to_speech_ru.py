from i18n import value_between_1_and_99


NOMINATIVE = 'nominative'
GENITIVE = 'genitive'
ONE_WORD_CARDINAL = {
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
ONE_WORD_ORDINAL = {
    ONE_WORD_CARDINAL[1]: {NOMINATIVE: 'первый', GENITIVE: 'первого'},
    ONE_WORD_CARDINAL[2]: {NOMINATIVE: 'второй', GENITIVE: 'второго'},
    ONE_WORD_CARDINAL[3]: {NOMINATIVE: 'третий', GENITIVE: 'третьего'},
    ONE_WORD_CARDINAL[4]: {NOMINATIVE: 'четвертый', GENITIVE: 'четвертого'},
    ONE_WORD_CARDINAL[5]: {NOMINATIVE: 'пятый', GENITIVE: 'пятого'},
    ONE_WORD_CARDINAL[6]: {NOMINATIVE: 'шестой', GENITIVE: 'шестого'},
    ONE_WORD_CARDINAL[7]: {NOMINATIVE: 'седьмой', GENITIVE: 'седьмого'},
    ONE_WORD_CARDINAL[8]: {NOMINATIVE: 'восьмой', GENITIVE: 'восьмого'},
    ONE_WORD_CARDINAL[9]: {NOMINATIVE: 'девятый', GENITIVE: 'девятого'},
    ONE_WORD_CARDINAL[10]: {NOMINATIVE: 'десятый', GENITIVE: 'десятого'},
    ONE_WORD_CARDINAL[11]: {NOMINATIVE: 'одиннадцатый', GENITIVE: 'одиннадцатого'},
    ONE_WORD_CARDINAL[12]: {NOMINATIVE: 'двенадцатый', GENITIVE: 'двенадцатого'},
    ONE_WORD_CARDINAL[13]: {NOMINATIVE: 'тринадцатый', GENITIVE: 'тринадцатого'},
    ONE_WORD_CARDINAL[14]: {NOMINATIVE: 'четырнадцатый', GENITIVE: 'четырнадцатого'},
    ONE_WORD_CARDINAL[15]: {NOMINATIVE: 'пятнадцатый', GENITIVE: 'пятнадцатого'},
    ONE_WORD_CARDINAL[16]: {NOMINATIVE: 'шестнадцатый', GENITIVE: 'шестнадцатого'},
    ONE_WORD_CARDINAL[17]: {NOMINATIVE: 'семнадцатый', GENITIVE: 'семнадцатого'},
    ONE_WORD_CARDINAL[18]: {NOMINATIVE: 'восемнадцатый', GENITIVE: 'восемнадцатого'},
    ONE_WORD_CARDINAL[19]: {NOMINATIVE: 'девятнадцатый', GENITIVE: 'девятнадцатого'},
    ONE_WORD_CARDINAL[20]: {NOMINATIVE: 'двадцатый', GENITIVE: 'двадцатого'},
    ONE_WORD_CARDINAL[30]: {NOMINATIVE: 'тридцатый', GENITIVE: 'тридцатого'},
    ONE_WORD_CARDINAL[40]: {NOMINATIVE: 'сороковой', GENITIVE: 'сорокового'},
    ONE_WORD_CARDINAL[50]: {NOMINATIVE: 'пятидесятый', GENITIVE: 'пятидесятого'},
    ONE_WORD_CARDINAL[60]: {NOMINATIVE: 'шестидесятый', GENITIVE: 'шестидесятого'},
    ONE_WORD_CARDINAL[70]: {NOMINATIVE: 'семидесятый', GENITIVE: 'семидесятого'},
    ONE_WORD_CARDINAL[80]: {NOMINATIVE: 'восьмидесятый', GENITIVE: 'восьмидесятого'},
    ONE_WORD_CARDINAL[90]: {NOMINATIVE: 'девяностый', GENITIVE: 'девяностого'}
}


@value_between_1_and_99
def to_cardinal(value):
    try:
        return ONE_WORD_CARDINAL[value]
    except KeyError:
        nearest_one_word_number = max(k for k in ONE_WORD_CARDINAL if k < value)
        return ONE_WORD_CARDINAL[nearest_one_word_number] + '-' + to_cardinal(value - nearest_one_word_number)


@value_between_1_and_99
def to_ordinal(value, case):
    result = to_cardinal(value)
    for last_word in ONE_WORD_ORDINAL:
        if result.endswith(last_word):
            return result[:-len(last_word)] + ONE_WORD_ORDINAL[last_word][case]
