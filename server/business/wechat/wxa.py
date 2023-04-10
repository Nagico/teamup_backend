import copy
import zoneinfo

from wechatpy import WeChatClientException
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType

from server.business.wechat import ENV_VERSION, wechat_client


def get_openid(code: str) -> str:
    """
    获取小程序登录后 openid
    :param code: 临时 code
    :return: openid
    """
    try:
        return wechat_client.wxa.code_to_session(code)["openid"]
    except WeChatClientException as e:
        if e.errcode == 40029:
            raise ApiException(ResponseType.ThirdLoginExpired, "微信登录失败，请重新登录")
        raise ApiException(
            ResponseType.ThirdLoginFailed,
            f"微信登录失败 [{e.errcode}] {e.errmsg}",
            record=True,
        )


tz = zoneinfo.ZoneInfo("Asia/Shanghai")


def check_text(
    content: str,
    openid: str,
    scene: int = 2,
    nickname: str = None,
    title: str = None,
) -> bool:
    """
    检查文本是否包含敏感词
    :param content: 文本
    :param openid: 用户 openid
    :param scene: 场景，1 资料；2 评论(默认)；3 论坛；4 社交日志
    :param nickname: 用户昵称(可选)
    :param title: 标题(可选)
    :return: 是否包含敏感词
    """
    try:
        data = {
            "content": content,
            "version": 2,
            "scene": scene,
            "openid": openid,
        }

        if nickname:
            data["nickname"] = nickname
        if title:
            data["title"] = title

        result = wechat_client.wxa._post("wxa/msg_sec_check", data=data)

        if result["errcode"] == 0:
            return result["result"]["suggest"] != "risky"
        else:
            return False
    except WeChatClientException:
        return False


def check_image(media):
    """
    检查图片
    """
    try:
        tmp = copy.deepcopy(media)
        result = wechat_client.wxa.check_image_security(tmp)

        return result["errcode"] == 0
    except WeChatClientException:
        return False


def get_wxa_code(
    page: str,
    scene: str,
    check_path: bool = True,
    width: int = 430,
    env_version: str = None,
    auto_color: bool = False,
    line_color: dict = None,
    is_hyaline: bool = False,
) -> bytes:
    """
    获取小程序码
    :param page: 跳转页面
    :param scene: 场景值
    :param env_version: 环境版本
    :param check_path: 是否检查页面路径
    :param width: 宽度
    :param auto_color: 是否自动配置线条颜色
    :param line_color: 颜色
    :param is_hyaline: 是否透明
    :return: 图片二进制
    """
    try:
        data = {
            "page": page,
            "scene": scene,
            "width": width,
            "auto_color": auto_color,
            "is_hyaline": is_hyaline,
            "check_path": check_path,
            "env_version": env_version or ENV_VERSION,
        }

        if not auto_color:
            data["line_color"] = line_color or {"r": 0, "g": 0, "b": 0}

        result = wechat_client.wxa._post("wxa/getwxacodeunlimit", data=data)

        image = result.content
        return image

    except WeChatClientException as e:
        raise ApiException(
            ResponseType.ThirdServiceError,
            f"获取小程序码失败 [{e.errcode}] {e.errmsg}",
            record=True,
        )


def get_user_phone_num(code: str) -> str:
    """
    获取用户手机号
    :param code: 临时 code
    :return: 手机号
    """
    try:
        data = {
            "code": code,
        }

        result = wechat_client.wxa._post(
            "wxa/business/getuserphonenumber", data=data
        )

        if result["phone_info"]["countryCode"] != "86":
            ApiException(ResponseType.ParamValidationFailed, "仅支持中国大陆手机号")

        return result["phone_info"]["purePhoneNumber"]
    except WeChatClientException as e:
        raise ApiException(
            ResponseType.ThirdServiceError,
            f"获取用户手机号失败 [{e.errcode}] {e.errmsg}",
            record=True,
        )
