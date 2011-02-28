# domains specified as regular expressions
# these are the domains that are allowed to use the service
ALLOWED_DOMAINS = [
    'localhost',
    'acmethumbs.appspot.com',
    '(.+)[.]globo[.]com',
    '(.+)[.]globoi[.]com'
]

# domains specified as regular expressions
# these are the allowed image sources
ALLOWED_SOURCES = [
    '(.+)[.]globo[.]com',
    '(.+)[.]globoi[.]com',
    's[.]glbimg[.]com'
]

# Make the app running in debug mode.
# default is True.
DEBUG = True

# this setting specifies the quality of the generated
# image. From 1 to 100.
QUALITY = 95

# Expiration in seconds for the image cache.
# Defaults to 1 month.
EXPIRATION = 30 * 24 * 60 * 60

# Expiration in seconds for the database.
# Defaults to 1 month.
EXPIRATION_DB = 30 * 24 * 60 * 60
