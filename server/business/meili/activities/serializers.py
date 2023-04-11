from activities.models import Activity
from rest_framework import serializers


class ActivityIndexSerializer(serializers.ModelSerializer):
    """
    activity 索引序列化器
    """

    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "introduction",
            "information",
            "start_time",
            "end_time",
            "time_node",
        ]
