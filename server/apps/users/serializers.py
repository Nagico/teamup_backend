from rest_framework import serializers
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from server.utils.images import compress_image, validate_image

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "nickname",
            "name",
            "student_id",
            "contact",
            "academy",
            "degree",
            "grade",
            "introduction",
            "experience",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
            "student_id": {"read_only": True},
        }

    def validate_nickname(self, value):
        if len(value) < 2:
            raise ApiException(ResponseType.ParamValidationFailed, "昵称不能少于2个字符")
        if len(value) > 20:
            raise ApiException(
                ResponseType.ParamValidationFailed, "昵称不能超过20个字符"
            )

        return value

    def validate_avatar(self, value):
        """
        检查并压缩头像
        """
        if value:
            value = validate_image(
                value,
                max_size=1024 * 1024 * 4,
            )
            value = compress_image(value, "avatar", width=300)

        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["academy"] = instance.academy.name if instance.academy else None
        return data


class UserInfoSerializer(serializers.ModelSerializer):
    academy = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "nickname",
            "academy",
            "degree",
            "grade",
        ]


class UserLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "avatar",
            "nickname",
            "academy",
            "degree",
            "grade",
            "introduction",
            "experience",
        ]

    def to_representation(self, instance):
        from academies.serializers import AcademySerializer

        data = super().to_representation(instance)
        data["academy"] = (
            AcademySerializer(instance.academy).data
            if instance.academy
            else None
        )
        return data


class UserTeamMemberSerializer(UserLeaderSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "academy",
            "degree",
            "grade",
            "introduction",
            "experience",
        ]
