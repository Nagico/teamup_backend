from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "introduction",
            "information",
            "logo",
            "start_time",
            "end_time",
            "time_node",
        ]


class ActivityInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            "id",
            "title",
            "logo",
            "start_time",
            "end_time",
            "time_node",
        ]
