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
            "read",
            "create_time",
        ]
        read_only_fields = [
            "id",
            "sender",
            "read",
        ]

    def create(self, validated_data):
        validated_data["sender"] = self.context["request"].user
        return super().create(validated_data)
