import datetime
import json
from uuid import UUID

from django.utils import timezone
from loguru import logger

from server.utils.choices.types import MessageType


class MQHandler:
    @staticmethod
    def handle_message(body):
        try:
            data = json.loads(body)

            if data["content"]["type"] == MessageType.READ.value:  # 已读回执
                MQHandler.read(data["content"]["content"])
            else:
                MQHandler.create(data)

        except Exception as e:
            logger.error(e)

    @staticmethod
    def create(data):
        from chat.models import Message

        Message.objects.create(
            id=UUID(data["id"]),
            sender_id=data["sender"],
            receiver_id=data["receiver"],
            type=data["content"]["type"],
            content=data["content"]["content"],
            create_time=datetime.datetime.fromtimestamp(
                data["createTime"] / 1000, tz=timezone.utc
            ),
        )

        logger.debug(f"Add message {data['id']} to database.")

    @staticmethod
    def read(uuid):
        from chat.models import Message

        try:
            Message.objects.filter(id=UUID(uuid)).update(is_read=True)
        except Exception as e:
            logger.error(f"Message {uuid} not found.\n {e}")
