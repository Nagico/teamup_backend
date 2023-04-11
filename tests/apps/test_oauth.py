from uuid import UUID, uuid4

import pytest
from users.models import User
from zq_django_util.response import ResponseType


@pytest.fixture
def user_uuid():
    return UUID("678574dd4a274d3cbfac10666b7613ef")


@pytest.fixture
def user_openid():
    return "oQKgO0Zr0yqLrW1qX1qX1qX1qX1q"


@pytest.fixture
def user_info(mocker):
    user_info = {
        "name": "张三",
        "student_id": "2020302111234",
        "phone": "18312341234",
        "update_time": "2033-01-01T00:00:00",
    }

    from server.business.ziqiang import zq_client

    zq_client.app.user_info = mocker.Mock(return_value=user_info)

    return user_info


@pytest.fixture
def zq_auth_code(mocker, user_uuid, user_info):
    zq_auth_code = "123123"

    from server.business.ziqiang import zq_client

    zq_client.app.sso = mocker.Mock(return_value={"union_id": user_uuid.hex})

    return zq_auth_code


@pytest.fixture
def wechat_code(mocker, user_openid):
    wechat_code = "123123"

    from server.business.wechat import wechat_client

    wechat_client.wxa.code_to_session = mocker.Mock(
        return_value={"openid": user_openid}
    )

    return wechat_code


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
