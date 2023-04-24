import uuid
from uuid import UUID

import pytest
from model_bakery import baker

from server.utils.choices.types import DegreeType


@pytest.fixture
def roles(db):
    from roles.models import Role

    Role.objects.create(name="1", description="1", parent=None)
    Role.objects.create(name="2", description="2", parent=None)

    Role.objects.create(
        name="1.1",
        description="1.1",
        parent=Role.objects.get(name="1"),
    )
    Role.objects.create(
        name="1.2",
        description="1.2",
        parent=Role.objects.get(name="1"),
    )
    Role.objects.create(
        name="2.1",
        description="2.1",
        parent=Role.objects.get(name="2"),
    )

    return Role.objects.all()


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
def user(db, user_uuid, user_openid):
    from academies.models import Academy
    from users.models import User

    return User.objects.create(
        union_id=user_uuid,
        openid=user_openid,
        username="test",
        nickname="t1",
        name="张三",
        student_id="2020302111234",
        academy=Academy.objects.get(name="计算机学院"),
        degree=DegreeType.BACHELOR,
        grade=2021,
        introduction="test1",
        experience=["1111", "111111"],
        phone="18312341234",
        update_time="2033-01-01T00:00:00",
        is_active=True,
        is_staff=False,
        contact=[
            {
                "type": "phone",
                "value": "18312341234",
            },
            {"type": "email", "value": "123@example.com"},
        ],
    )


@pytest.fixture
def user2(db):
    from academies.models import Academy
    from users.models import User

    return User.objects.create(
        union_id=uuid.uuid4(),
        openid="2222",
        nickname="t2",
        username="test2",
        name="张三2",
        student_id="2020302112234",
        academy=Academy.objects.get(name="计算机学院"),
        degree=DegreeType.BACHELOR,
        grade=2020,
        introduction="test",
        experience=["test", "111222"],
        phone="18312341235",
        update_time="2033-01-01T00:00:00",
        is_active=True,
        is_staff=False,
        contact=[
            {
                "type": "phone",
                "value": "18312341235",
            },
            {"type": "email", "value": "123123@123.com"},
        ],
    )


@pytest.fixture
def activity(db):
    from activities.models import Activity

    return baker.make(Activity)


@pytest.fixture
def team(db, user, activity):
    from teams.models import Team

    return Team.objects.create(
        leader=user,
        name="test",
        introduction="tttest",
        activity=activity,
        teacher="test",
        contact=[{"type": "qq", "value": "123"}],
        public=True,
    )
