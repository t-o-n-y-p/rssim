import json
import codecs

# load resource strings from JSON file
with codecs.open('resources.json', 'r', 'utf-8-sig') as resource_file:
    I18N_RESOURCES = json.load(resource_file)


def i18n_number_category(x, locale):
    """
    Returns localization category of a given number in the given locale.
    Source of expectations: https://www.unicode.org/cldr/charts/34/supplemental/language_plural_rules.html

    :param locale:      current locale selected by player
    :param x:           given number
    :return:            group ID, possible values: 'zero', 'one', 'two', 'few', 'many', 'other'
    """
    if type(x) is float:
        return 'other'
    elif type(x) is int:
        if locale == 'en':
            if x == 1:
                return 'one'
            else:
                return 'other'

        elif locale == 'ru':
            if x % 10 == 1 and x % 100 != 11:
                return 'one'
            elif x % 10 in (2, 3, 4) and x % 100 not in (12, 13, 14):
                return 'few'
            else:
                return 'many'
