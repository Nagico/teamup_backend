from uuid import uuid4

import pytest
from users.models import User
from zq_django_util.response import ResponseType


@pytest.fixture
def user(db, user_uuid, user_info, api_client, user_openid) -> User:
    api_client.post("/auth/zq/unionid/", {"union_id": user_uuid.hex})
    user = User.objects.get(union_id=user_uuid)
    user.openid = user_openid
    user.save()

    return user


def test_zq_auth_union_id__new_user(db, api_client, user_info):
    uuid = uuid4()

    data = api_client.post("/auth/zq/unionid/", {"union_id": uuid.hex}).json()[
        "data"
    ]

    assert data == {
        "id": data["id"],
        "username": f"{user_info['name']}_{user_info['student_id']}",
        "is_active": True,
        "is_staff": False,
        "expire_time": data["expire_time"],
        "access": data["access"],
        "refresh": data["refresh"],
    }


def test_zq_auth_union_id__exist(db, api_client, user_info, user):
    data = api_client.post(
        "/auth/zq/unionid/", {"union_id": user.union_id.hex}
    ).json()["data"]

    assert data == {
        "id": data["id"],
        "username": user.username,
        "is_active": True,
        "is_staff": False,
        "expire_time": data["expire_time"],
        "access": data["access"],
        "refresh": data["refresh"],
    }


def test_zq_auth__new_user(db, api_client, user_info, zq_auth_code):
    data = api_client.post("/auth/zq/", {"code": zq_auth_code}).json()["data"]

    assert data == {
        "id": data["id"],
        "username": f"{user_info['name']}_{user_info['student_id']}",
        "is_active": True,
        "is_staff": False,
        "expire_time": data["expire_time"],
        "access": data["access"],
        "refresh": data["refresh"],
    }


def test_zq_auth__exist(db, api_client, user_info, user, zq_auth_code):
    data = api_client.post("/auth/zq/", {"code": zq_auth_code}).json()["data"]

    assert data == {
        "id": data["id"],
        "username": user.username,
        "is_active": True,
        "is_staff": False,
        "expire_time": data["expire_time"],
        "access": data["access"],
        "refresh": data["refresh"],
    }


def test_wechat_openid__not_exist(db, api_client):
    data = api_client.post("/auth/wechat/openid/", {"openid": "123"}).json()

    assert data["code"] == ResponseType.ThirdLoginFailed.code


def test_wechat_openid__exist(db, api_client, user):
    data = api_client.post(
        "/auth/wechat/openid/", {"openid": user.openid}
    ).json()["data"]

    assert data == {
        "id": data["id"],
        "username": user.username,
        "is_active": True,
        "is_staff": False,
        "expire_time": data["expire_time"],
        "access": data["access"],
        "refresh": data["refresh"],
    }


def test_wechat__not_exist(db, api_client, wechat_code):
    data = api_client.post("/auth/wechat/", {"code": wechat_code}).json()

    assert data["code"] == ResponseType.ThirdLoginFailed.code


def test_wechat__exist(db, api_client, user, wechat_code):
    data = api_client.post("/auth/wechat/", {"code": wechat_code}).json()[
        "data"
    ]

    assert data == {
        "id": data["id"],
        "username": user.username,
        "is_active": True,
        "is_staff": False,
        "expire_time": data["expire_time"],
        "access": data["access"],
        "refresh": data["refresh"],
    }
