from banners.models import Banner
from rest_framework import serializers

from server.utils.images import compress_image, validate_image


class BannerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ["id", "title", "cover"]


class BannerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = [
            "id",
            "title",
            "subtitle",
            "cover",
            "photo",
            "content",
            "score",
        ]

    def validate_cover(self, value):
        """
        封面检测
        """
        if value:
            value = validate_image(
                value,
                min_size=1024 * 10,
                max_size=1024 * 1024 * 8,
            )

            value = compress_image(value, "cover", width=780)

        return value

    def validate_photo(self, value):
        """
        背景图检测
        """
        if value:
            value = validate_image(
                value,
                min_size=1024 * 10,
                max_size=1024 * 1024 * 8,
            )

            value = compress_image(value, "photo", width=780)

        return value
