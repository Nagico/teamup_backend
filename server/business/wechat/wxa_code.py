from django.core.files.base import ContentFile

from server.business.wechat.wxa import get_wxa_code


def get_wxa_code_bytes(
    field: str, obj_id: int, width: int = 400, env_version: str | None = None
) -> ContentFile:
    """
    获取小程序码
    :return: 图片
    """
    _img = get_wxa_code(
        f"pages/index/{field}",
        f"{obj_id}",
        width=width,
        env_version=env_version,
        auto_color=True,
        is_hyaline=True,
    )
    return ContentFile(_img)
