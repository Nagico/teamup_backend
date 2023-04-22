from django.conf import settings

CHAT_FINDER_THREAD = None

if settings.CHAT_FINDER_ENABLED:
    import threading

    from .finder import FindHostAsync

    FINDER_THREAD_NAME = "chat_finder_thread"

    already_exists = False

    for t in threading.enumerate():
        if t.name == FINDER_THREAD_NAME:
            already_exists = True
            break

    if not already_exists:
        t = FindHostAsync()
        t.daemon = True
        t.name = FINDER_THREAD_NAME
        t.start()
        LOGGER_THREAD = t
