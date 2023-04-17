from activities.serializers import ActivityInfoSerializer
from rest_framework import serializers
from teams.models import Team
from users.serializers import UserInfoSerializer


class TeamIndexSerializer(serializers.ModelSerializer):
    """
    team 索引序列化器
    """

    activity = ActivityInfoSerializer()
    leader = UserInfoSerializer()
    has_teacher = serializers.SerializerMethodField()
    activity_id = serializers.SerializerMethodField()
    role_ids = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "activity",
            "leader",
            "introduction",
            "teacher",
            "contact",
            "public",
            "has_teacher",
            "activity_id",
            "role_ids",
        ]

    def get_has_teacher(self, obj) -> bool:
        return bool(obj.teacher)

    def get_activity_id(self, obj) -> int:
        return obj.activity.id if obj.activity else None

    def get_role_ids(self, obj) -> list:
        return list(obj.demands.values_list("role_id", flat=True).distinct())
