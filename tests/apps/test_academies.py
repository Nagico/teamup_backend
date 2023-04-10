def test_get_academy_list(db, api_client):
    """
    获取院系列表
    """

    data = api_client.get("/academies/").json()["data"]

    assert len(data) != 0
    assert "id" in data[0]
    assert "name" in data[0]
    assert "children" in data[0]


def test_get_academy_detail(db, api_client):
    """
    获取院系详情
    """

    data = api_client.get("/academies/1/").json()["data"]

    assert data == {
        "id": 1,
        "name": "人文科学学部",
        "parent": None,
    }


def test_get_academy_detail_not_found(db, api_client):
    """
    获取院系详情，不存在
    """

    response = api_client.get("/academies/999/")

    assert response.status_code == 404
