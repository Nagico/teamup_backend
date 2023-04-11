import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType
from zq_django_util.utils.oss.utils import get_random_name


def compress_image(
    content: InMemoryUploadedFile,
    field_name: str,
    width: int | None = None,
    height: int | None = None,
) -> InMemoryUploadedFile:
    """
    重写文件处理，压缩图片

    :param content: 上传的图片
    :param field_name: 字段名
    :param width: 压缩后的宽度（可选）
    :param height: 压缩后的高度（可选）
    :return: 压缩后的图片
    """
    image = Image.open(content.file)

    if width and not height:  # 比例压缩宽度
        width_percent = width / float(image.size[0])
        height = int((float(image.size[1]) * float(width_percent)))
    elif not width and height:  # 比例压缩高度
        height_percent = height / float(image.size[1])
        width = int((float(image.size[0]) * float(height_percent)))

    if width and height:  # 压缩
        image = image.resize((width, height), Image.ANTIALIAS)

    # 保存
    new_file = io.BytesIO()
    image.save(new_file, format=content.image.format)  # type: ignore
    size = new_file.tell()
    new_file.seek(0)
    new_content = InMemoryUploadedFile(
        new_file,
        field_name,
        get_random_name(content.name),
        content.content_type,
        size,
        None,
    )
    return new_content


def validate_image(
    value: InMemoryUploadedFile,
    min_size: int | None = None,
    max_size: int | None = None,
):
    """
    图片校验
    :param value: 图片
    :param min_size: 最小大小
    :param max_size: 最大大小
    :return:
    """
    if value.content_type not in ["image/jpeg", "image/png"]:  # 文件类型不正确
        raise ApiException(
            ResponseType.UnsupportedMediaType, "请选择jpg或png格式的图片重新上传"
        )

    if max_size is not None and value.size > max_size:
        raise ApiException(ResponseType.UnsupportedMediaSize, "文件大小超过限制，请重新上传")

    if min_size is not None and value.size < min_size:
        raise ApiException(ResponseType.UnsupportedMediaSize, "文件大小不足，请重新上传")

    return value
