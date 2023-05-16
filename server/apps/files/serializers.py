from files.models import File
from rest_framework import serializers
from zq_django_util.utils.oss.utils import get_random_name, split_file_name


class FileSerializer(serializers.ModelSerializer):
    """
    文件序列化器
    """

    class Meta:
        model = File
        exclude = ["user"]
        read_only_fields = ["ext", "size"]

    def validate(self, attrs):
        """
        自动添加文件名、用户
        """
        attrs["user"] = self.context["request"].user

        if "file" in attrs:
            attrs["name"], attrs["ext"] = split_file_name(
                attrs["name"]
            )  # 获取文件名与扩展名
            attrs["file"].name = get_random_name(attrs["file"].name)  # 文件名随机化
            attrs["size"] = attrs["file"].size  # 获取文件大小

        return attrs
