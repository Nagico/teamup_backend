from chat.models import Message
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "sender",
            "receiver",
            "content",
            "type",
            "is_read",
            "create_time",
        ]
        read_only_fields = [
            "id",
            "sender",
            "read",
        ]
