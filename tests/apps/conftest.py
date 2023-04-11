from uuid import UUID

import pytest


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
