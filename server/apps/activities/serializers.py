from rest_framework import serializers

from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    favorite = serializers.SerializerMethodField()

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
            "favorite",
        ]

    def get_favorite(self, obj):
        return obj.users.filter(id=self.context["request"].user.id).exists()


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
