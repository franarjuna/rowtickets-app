from django.conf import settings

COUNTRY_LANGUAGES = settings.COUNTRY_LANGUAGES


def get_country_from_language_code(language_code):

    return list(filter(lambda x: COUNTRY_LANGUAGES[x] == language_code, COUNTRY_LANGUAGES))[0]


def get_language_code_from_country(country):
    return COUNTRY_LANGUAGES[country]
