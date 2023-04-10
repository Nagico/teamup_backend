import pytest
from roles.models import Role


@pytest.fixture
def roles(db):
    Role.objects.create(name="1", level=0, description="1", parent=None)
    Role.objects.create(name="2", level=0, description="2", parent=None)

    Role.objects.create(
        name="1.1",
        level=1,
        description="1.1",
        parent=Role.objects.get(name="1"),
    )
    Role.objects.create(
        name="1.2",
        level=1,
        description="1.2",
        parent=Role.objects.get(name="1"),
    )
    Role.objects.create(
        name="2.1",
        level=1,
        description="2.1",
        parent=Role.objects.get(name="2"),
    )


def test_get_roles__root(roles, api_client):
    data = api_client.get("/roles/?parent__isnull=true").json()["data"]

    assert data["count"] == 2
    assert data["results"][0]["name"] == "1"
    assert data["results"][1]["name"] == "2"

    assert data["results"][0]["children_count"] == 2
    assert data["results"][1]["children_count"] == 1


def test_get_roles__children(roles, api_client):
    role1 = Role.objects.get(name="1")
    data = api_client.get(f"/roles/?parent={role1.id}").json()["data"]

    assert data["count"] == 2
    assert data["results"][0]["name"] == "1.1"
    assert data["results"][1]["name"] == "1.2"


def test_get_roles__single(roles, api_client):
    role1 = Role.objects.get(name="1")
    data = api_client.get(f"/roles/{role1.id}/").json()["data"]

    assert data == {
        "id": role1.id,
        "name": "1",
        "description": "1",
        "parent": None,
        "children_count": 2,
    }
