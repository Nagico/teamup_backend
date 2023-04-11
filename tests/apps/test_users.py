from uuid import uuid4

import pytest
from users.models import User
from zq_django_util.response import ResponseType


@pytest.fixture
def user(db):
    from users.models import User

    return User.objects.create(
        username="nagico",
        phone="18312341234",
        student_id="2020302111234",
        is_active=True,
        is_staff=False,
        contact=[{"type": "phone", "value": "18312341234"}],
    )


@pytest.fixture
def image():
    def _image(size: int = 300):
        from PIL import Image

        image = Image.new("RGB", (size, size), "white")
        import tempfile

        file = tempfile.NamedTemporaryFile(suffix=".jpg")

        image.save(file)
        file.seek(0)

        return file

    return _image


def test_get_user_info__self(user, api_client):
    api_client.force_authenticate(user=user)
    data = api_client.get("/users/").json()["data"]

    assert data == {
        "id": 1,
        "avatar": "http://testserver/media/user/avatar/default.jpg",
        "nickname": "",
        "name": "",
        "student_id": "2020302111234",
        "contact": [{"type": "phone", "value": "18312341234"}],
        "academy": None,
        "degree": 0,
        "grade": 0,
        "introduction": "",
        "experience": [],
    }


def test_update_user_info(user, api_client):
    api_client.force_authenticate(user=user)
    data = api_client.patch(
        f"/users/{user.id}/",
        {
            "nickname": "nagico",
            "contact": [
                {"type": "email", "value": "test@example.com"},
                {"type": "qq", "value": "12345"},
            ],
            "academy": 19,
            "degree": 1,
            "grade": 2020,
            "introduction": "1234567",
            "experience": ["12344", "12312312"],
        },
        format="json",
    ).json()["data"]

    assert data == {
        "id": 1,
        "avatar": "http://testserver/media/user/avatar/default.jpg",
        "nickname": "nagico",
        "name": "",
        "student_id": "2020302111234",
        "contact": [
            {"type": "email", "value": "test@example.com"},
            {"type": "qq", "value": "12345"},
        ],
        "academy": "政治与公共管理学院",
        "degree": 1,
        "grade": 2020,
        "introduction": "1234567",
        "experience": ["12344", "12312312"],
    }


def test_update_user_info__invalid_nickname(user, api_client):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/users/{user.id}/", {"nickname": "n"}, format="json"
    ).json()

    assert response["code"] == ResponseType.ParamValidationFailed.code


def test_update_user_info__invalid_academy(user, api_client):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/users/{user.id}/", {"academy": 100}, format="json"
    ).json()

    assert response["code"] == ResponseType.ParamValidationFailed.code


def test_update_user_info__invalid_degree(user, api_client):
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/users/{user.id}/", {"degree": 100}, format="json"
    ).json()

    assert response["code"] == ResponseType.ParamValidationFailed.code


def test_update_user_avatar(user, api_client, image):
    api_client.force_authenticate(user=user)

    avatar = image(size=500)

    response = api_client.patch(
        f"/users/{user.id}/", {"avatar": avatar}, format="multipart"
    ).json()["data"]

    assert response["avatar"].startswith("http://testserver/media/user/avatar/")
    assert response["avatar"].endswith(".jpg")


def test_update_user_avatar__invalid_size(user, api_client, image):
    api_client.force_authenticate(user=user)

    avatar = image(size=50000)

    response = api_client.patch(
        f"/users/{user.id}/", {"avatar": avatar}, format="multipart"
    ).json()

    assert response["code"] == ResponseType.ParamValidationFailed.code


def test_update_user_avatar__invalid_type(user, api_client, image):
    api_client.force_authenticate(user=user)

    avatar = image(size=500)
    avatar.name = "test.ttf"

    response = api_client.patch(
        f"/users/{user.id}/", {"avatar": avatar}, format="multipart"
    ).json()

    assert response["code"] == ResponseType.ParamValidationFailed.code


def test_get_user_info__other(user, api_client):
    data = api_client.get(f"/users/{user.id}/").json()["data"]

    assert data == {
        "id": 1,
        "avatar": "http://testserver/media/user/avatar/default.jpg",
        "nickname": "",
        "academy": None,
        "degree": 0,
        "grade": 0,
    }


def test_get_user_info__not_found(user, api_client):
    response = api_client.get(f"/users/{user.id + 1}/").json()

    assert response["code"] == ResponseType.APINotFound.code


def test_bind_wechat(user, api_client, wechat_code, user_openid):
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/users/wechat/", {"code": wechat_code}, format="json"
    )

    assert response.status_code == 201
    user.refresh_from_db()
    assert user.openid == user_openid


def test_bind_wechat__exist(user, api_client, wechat_code, user_openid):
    old_user = User.objects.create(
        username="test", openid=user_openid, union_id=uuid4()
    )

    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/users/wechat/", {"code": wechat_code}, format="json"
    )

    old_user.refresh_from_db()
    user.refresh_from_db()

    assert response.status_code == 201
    assert user.openid == user_openid
    assert old_user.openid is None


def test_unbind_wechat(user, api_client, wechat_code):
    api_client.force_authenticate(user=user)
    api_client.post("/users/wechat/", {"code": wechat_code}, format="json")

    response = api_client.delete("/users/wechat/")

    assert response.status_code == 204
    user.refresh_from_db()
    assert user.openid is None
