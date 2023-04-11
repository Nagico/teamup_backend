from academies.serializers import AcademySerializer
from rest_framework import serializers
from roles.serializers import RoleInfoSerializer
from users.serializers import UserInfoSerializer, UserTeamMemberSerializer
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from .models import Team, TeamDemand, TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "user",
            "nickname",
            "academy",
            "degree",
            "grade",
            "introduction",
            "experience",
        ]

    def create(self, validated_data):
        return TeamMember.objects.create(
            **validated_data,
            team=self.context["request"].team,
        )

    def validate_user(self, value):
        if value and value.id in self.context[
            "request"
        ].team.members.values_list("user", flat=True):
            raise ApiException(
                ResponseType.ParamValidationFailed, msg="该队员已在队伍中"
            )
        if value and value.id == self.context["request"].team.leader.id:
            raise ApiException(
                ResponseType.ParamValidationFailed, msg="队长无需加入队伍"
            )
        return value

    def to_representation(self, instance):
        if instance.user:  # 处理导入队员信息
            data = UserTeamMemberSerializer(instance.user).data
            data["id"] = instance.id
            data["user"] = instance.user.id
        else:
            data = super().to_representation(instance)
            data["academy"] = AcademySerializer(instance.academy).data
        return data


class TeamDemandSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamDemand
        fields = [
            "id",
            "role",
            "number",
            "detail",
        ]

    def create(self, validated_data):
        return TeamDemand.objects.create(
            **validated_data,
            team=self.context["request"].team,
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["role"] = RoleInfoSerializer(instance.role).data
        return data


class TeamInfoSerializer(serializers.ModelSerializer):
    leader = UserInfoSerializer(read_only=True)
    favorite = serializers.SerializerMethodField()
    demand_tags = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "introduction",
            "leader",
            "activity",
            "demand_tags",
            "favorite",
            "update_time",
        ]

    def get_favorite(self, obj: Team) -> bool:
        if self.context["request"].user.is_authenticated:
            return obj.users.filter(id=self.context["request"].user.id).exists()
        else:
            return False

    def get_demand_tags(self, obj: Team) -> list:
        return obj.demands.values_list("role__name", flat=True).distinct()

    def to_representation(self, instance):
        from activities.serializers import ActivityInfoSerializer

        data = super().to_representation(instance)
        data["activity"] = ActivityInfoSerializer(instance.activity).data
        return data


class TeamSerializer(TeamInfoSerializer):
    members = TeamMemberSerializer(many=True, read_only=True)
    demands = TeamDemandSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            "id",
            "name",
            "activity",
            "introduction",
            "teacher",
            "contact",
            "public",
            "leader",
            "members",
            "demands",
            "favorite",
        ]

    def create(self, validated_data):
        return Team.objects.create(
            **validated_data,
            leader=self.context["request"].user,
        )
