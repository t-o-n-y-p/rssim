import json
import codecs
from typing import Final

# load resource strings from JSON file
with codecs.open('resources.json', 'r', 'utf-8-sig') as resource_file:
    I18N_RESOURCES: Final = json.load(resource_file)


def value_between_1_and_99(fn):
    def _convert_numbers(*args, **kwargs):
        if 0 < args[0] < 100:
            return fn(*args, **kwargs)

    return _convert_numbers


NOMINATIVE: Final = 'nominative'
GENITIVE: Final = 'genitive'
DATIVE: Final = 'dative'
PREPOSITIONAL: Final = 'prepositional'

ENGLISH: Final = 'en'
RUSSIAN: Final = 'ru'

ZERO: Final = 'zero'
ONE: Final = 'one'
TWO: Final = 'two'
FEW: Final = 'few'
MANY: Final = 'many'
OTHER: Final = 'other'


def i18n_number_category(x, locale):
    """
    Returns localization category of a given number in the given locale.
    Source of expectations: https://www.unicode.org/cldr/charts/34/supplemental/language_plural_rules.html

    :param locale:      current locale selected by player
    :param x:           given number
    :return:            group ID, possible values: 'zero', 'one', 'two', 'few', 'many', 'other'
    """
    if type(x) is float:
        return OTHER
    elif type(x) is int:
        if locale == ENGLISH:
            if x == 1:
                return ONE
            else:
                return OTHER

        elif locale == RUSSIAN:
            if x % 10 == 1 and x % 100 != 11:
                return ONE
            elif x % 10 in (2, 3, 4) and x % 100 not in (12, 13, 14):
                return FEW
            else:
                return MANY
