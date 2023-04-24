import urllib

import pika
from chat.utils import MQHandler
from loguru import logger


class RabbitMQ:
    SAVE_EXCHANGE_NAME = "teamup.direct.save"
    SAVE_QUEUE_NAME = "teamup.message.save"

    def __init__(self, url: str):
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        logger.success(
            f"RabbitMQ connected to {urllib.parse.urlparse(url).hostname}"
        )
        self.channel = self.connection.channel()

        self.channel.basic_consume(
            queue=self.SAVE_QUEUE_NAME,
            on_message_callback=self.callback,
            auto_ack=False,
        )
        logger.success(f"RabbitMQ starting consuming {self.SAVE_QUEUE_NAME}")

    def callback(self, ch, method, properties, body):
        try:
            MQHandler.handle_message(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logger.error(e)

    def start(self):
        self.channel.start_consuming()
