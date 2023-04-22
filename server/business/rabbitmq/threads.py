from django.conf import settings

MQ_CONSUMER_THREAD = None

if settings.RABBITMQ_URL is not None:
    import threading

    from .consumer import ConsumeAsync

    MQ_CONSUMER_THREAD = "mq_consumer_thread"

    already_exists = False

    for t in threading.enumerate():
        if t.name == MQ_CONSUMER_THREAD:
            already_exists = True
            break

    if not already_exists:
        t = ConsumeAsync()
        t.daemon = True
        t.name = MQ_CONSUMER_THREAD
        t.start()
        LOGGER_THREAD = t
