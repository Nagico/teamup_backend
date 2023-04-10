from academies import models
from rest_framework import serializers


class AcademyInfoSerializer(serializers.ModelSerializer):
    """
    院系简要序列化器
    """

    class Meta:
        model = models.Academy
        exclude = ["logo", "level"]


class AcademyDetailSerializer(serializers.ModelSerializer):
    """
    院系详情序列化器
    """

    class Meta:
        model = models.Academy
        exclude = ["level"]
