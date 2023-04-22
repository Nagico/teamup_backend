from server.settings.util import config

CHAT_DEFAULT_HOSTS = config("CHAT_DEFAULT_HOSTS", default=[], cast=list)

CHAT_FINDER_ENABLED = config("CHAT_FINDER_ENABLED", default=False, cast=bool)
