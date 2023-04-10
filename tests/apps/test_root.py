def test_root(db, api_client):
    data = api_client.get("/").data

    assert data == {
        "user": None,
        "time": data["time"],
    }
