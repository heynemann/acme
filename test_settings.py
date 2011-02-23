from re import compile as re_compile, error as RegexError
import settings

def test_has_debug_config():
    assert hasattr(settings, "DEBUG")

def test_debug_config_is_properly_configured():
    assert type(settings.DEBUG) is bool

def test_has_allowed_domains_config():
    assert hasattr(settings, "ALLOWED_DOMAINS")

def test_allowed_domains_config_is_properly_configured():
    assert type(settings.ALLOWED_DOMAINS) is list

def test_allowed_domains_is_all_strings():
    assert not False in map(lambda urlpattern: type(urlpattern) is str, settings.ALLOWED_DOMAINS)

def test_allowed_domains_has_only_valid_regular_expressions():
    try:
        map(lambda urlpattern: re_compile(urlpattern), settings.ALLOWED_DOMAINS)
    except RegexError, e:
        assert False

def test_has_allowed_sources_config():
    assert hasattr(settings, "ALLOWED_SOURCES")

def test_allowed_sources_config_is_properly_configured():
    assert type(settings.ALLOWED_SOURCES) is list

def test_allowed_sources_is_all_strings():
    assert not False in map(lambda urlpattern: type(urlpattern) is str, settings.ALLOWED_SOURCES)

def test_allowed_sources_has_only_valid_regular_expressions():
    try:
        map(lambda urlpattern: re_compile(urlpattern), settings.ALLOWED_SOURCES)
    except RegexError, e:
        assert False

def test_has_quality_config():
    assert hasattr(settings, "QUALITY")

def test_quality_config_is_integer_value():
    assert type(settings.QUALITY) is int

def test_quality_config_is_properly_configured():
    assert settings.QUALITY >= 0 and settings.QUALITY <= 100

def test_has_expiration_config():
    assert hasattr(settings, "EXPIRATION")

def test_expiration_is_properly_configured():
    assert type(settings.EXPIRATION) is int

def test_has_expiration_config():
    assert hasattr(settings, "EXPIRATION_DB")

def test_expiration_db_is_properly_configured():
    assert type(settings.EXPIRATION_DB) is int

