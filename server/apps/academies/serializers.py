from academies import models
from rest_framework import serializers


class AcademySerializer(serializers.ModelSerializer):
    """
    院系简要序列化器
    """

    class Meta:
        model = models.Academy
        exclude = ["level"]
