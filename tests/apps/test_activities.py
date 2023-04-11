import pytest
from model_bakery import baker


@pytest.fixture
def activities(db):
    return baker.make(
        "activities.Activity",
        information=[{"name": "官网", "url": "https://www.baidu.com"}],
        time_node=[{"name": "报名", "date": "2021-01-01"}],
        _quantity=10,
    )


def test_get_activities(api_client, activities):
    data = api_client.get("/activities/").json()["data"]
    assert data["count"] == 10
    assert int(data["results"][0]["id"]) == activities[-1].id


def test_get_activity(api_client, activities):
    data = api_client.get("/activities/1/").json()["data"]
    assert int(data["id"]) == activities[0].id
    assert data["information"] == activities[0].information
    assert data["time_node"] == activities[0].time_node
    assert data["title"] == activities[0].title
