from rest_framework import serializers

from . import models


class RoleSerializer(serializers.ModelSerializer):
    """
    角色序列化器
    """

    children_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Role
        exclude = ["level"]

    def get_children_count(self, obj) -> int:
        return obj.sub_roles.count()
