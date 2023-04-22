import datetime
import json
from uuid import UUID

from django.utils import timezone
from loguru import logger


class MQHandler:
    @staticmethod
    def handle_message(body):
        try:
            data = json.loads(body)

            if data["type"] == 0:  # Message
                MQHandler.create(data)
            else:
                MQHandler.ack(data)
        except Exception as e:
            logger.error(e)

    @staticmethod
    def create(data):
        from chat.models import Message

        Message.objects.create(
            id=UUID(data["id"]),
            sender_id=data["sender"],
            receiver_id=data["receiver"],
            type=data["type"],
            content=json.loads(data["content"]),
            create_time=datetime.datetime.fromtimestamp(
                data["createTime"] / 1000, tz=timezone.utc
            ),
        )

    @staticmethod
    def ack(data):
        from chat.models import Message

        Message.objects.filter(id=UUID(data["id"])).update(is_read=True)
