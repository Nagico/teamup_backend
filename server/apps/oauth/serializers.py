from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from oauth.backends import UnionIdBackend
from rest_framework_simplejwt.serializers import PasswordField
from users.models import User
from zq_auth_sdk import UserNotFoundException
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType
from zq_django_util.utils.auth.backends import OpenIdBackend
from zq_django_util.utils.auth.serializers import (
    OpenIdLoginSerializer as DefaultOpenIdLoginSerializer,
)

import server.business.ziqiang.auth as zq_auth
from server.business.wechat.wxa import get_openid


def generate_token_result(
    user: User,
    user_id_field: str,
    expire_time: datetime,
    access: str,
    refresh: str,
) -> dict:
    return dict(
        id=getattr(user, user_id_field),
        username=user.username,
        is_active=user.is_active,
        is_staff=user.is_staff,
        expire_time=expire_time,
        access=access,
        refresh=refresh,
    )


class OpenIdLoginSerializer(DefaultOpenIdLoginSerializer):
    """
    OpenID Token 获取序列化器 (直接用 openid 获取登录 token，用于测试)
    """

    backend = OpenIdBackend(User)  # 自定义验证后端，用于指定不同类型的用户模型

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_token_result(
        self,
        user: User,
        user_id_field: str,
        expire_time: datetime,
        access: str,
        refresh: str,
    ) -> dict:
        return generate_token_result(
            user, user_id_field, expire_time, access, refresh
        )


class WechatLoginSerializer(OpenIdLoginSerializer):
    """
    微信登录序列化器
    """

    code = PasswordField(label="前端获取code")  # 前端传入 code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop("openid")  # 删除 openid 字段

    def get_open_id(self, attrs: Dict[str, Any]) -> str:
        """
        重写获取 open_id 方法
        """
        return get_openid(attrs["code"])


class UnionIdLoginSerializer(DefaultOpenIdLoginSerializer):
    """
    自强Auth union id 登录序列化器
    """

    backend = UnionIdBackend(User)
    openid = None
    openid_field = "union_id"
    union_id = PasswordField(label="union_id")  # union_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_token_result(
        self,
        user: User,
        user_id_field: str,
        expire_time: datetime,
        access: str,
        refresh: str,
    ) -> dict:
        return generate_token_result(
            user, user_id_field, expire_time, access, refresh
        )

    def get_open_id(self, attrs: Dict[str, Any]) -> UUID:
        """
        重写获取 open_id 方法
        """
        return UUID(attrs["union_id"])

    def handle_new_openid(self, union_id: UUID) -> User:
        """
        重写处理新 union id 方法
        """
        try:
            user_data = zq_auth.fetch_user_info(union_id)
            data = {
                "union_id": union_id,
                "username": f"{user_data['name']}_{user_data['student_id']}",
                "name": user_data["name"],
                "phone": user_data["phone"],
                "student_id": user_data["student_id"],
                "contact": [{"type": "phone", "value": user_data["phone"]}],
            }
            instance = User.objects.create(
                **data, is_active=True, is_staff=False
            )
            return instance
        except UserNotFoundException:
            raise ApiException(ResponseType.ThirdServiceError, "用户不存在")


class ZqAuthLoginSerializer(UnionIdLoginSerializer):
    """
    自强Auth登录序列化器
    """

    code = PasswordField(label="前端获取code")  # 前端传入 code
    union_id = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_open_id(self, attrs: Dict[str, Any]) -> UUID:
        """
        重写获取 open_id 方法
        """
        return zq_auth.get_union_id(attrs["code"])
