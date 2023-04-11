from teams.models import Team, TeamDemand, TeamMember
from zq_django_util.response import ResponseType

from server.utils.choices.types import DegreeType


def test_get_team(api_client, team):
    data = api_client.get(f"/teams/{team.id}/").json()["data"]
    assert data["id"] == team.id
    assert data["name"] == team.name
    assert data["activity"]["id"] == team.activity.id
    assert data["introduction"] == team.introduction
    assert data["teacher"] == team.teacher
    assert data["contact"] == team.contact
    assert data["public"] == team.public
    assert data["leader"]["id"] == team.leader.id
    assert data["members"] == []
    assert data["demands"] == []


def test_create_team__init(api_client, user):
    api_client.force_authenticate(user=user)
    data = api_client.post("/teams/", {}).json()["data"]

    assert data["name"] == ""
    assert data["public"] is False


def test_update_team__anonymous(api_client):
    data = api_client.patch("/teams/1/", {}).json()

    assert data["code"] == ResponseType.NotLogin.code


def test_update_team__not_found(api_client, user):
    api_client.force_authenticate(user=user)
    data = api_client.patch("/teams/1/", {}).json()

    assert data["code"] == ResponseType.APINotFound.code


def test_update_team(db, api_client, user, activity):
    team = Team.objects.create(
        leader=user,
    )

    api_client.force_authenticate(user=user)
    data = api_client.patch(
        f"/teams/{team.id}/",
        {
            "name": "test",
            "activity": activity.id,
            "introduction": "test",
            "teacher": "test",
            "contact": [{"type": "qq", "value": "123"}],
            "public": True,
        },
        format="json",
    ).json()["data"]

    assert data["name"] == "test"
    assert data["activity"]["id"] == activity.id
    assert data["introduction"] == "test"
    assert data["teacher"] == "test"
    assert data["contact"] == [{"type": "qq", "value": "123"}]
    assert data["public"] is True


def test_add_team_member__import(api_client, team, user, user2):
    api_client.force_authenticate(user=user)

    data = api_client.post(
        f"/teams/{team.id}/members/",
        {
            "user": user2.id,
        },
        format="json",
    ).json()["data"]

    assert data["nickname"] == user2.nickname
    assert data["academy"]["id"] == user2.academy.id
    assert data["degree"] == user2.degree
    assert data["grade"] == user2.grade
    assert data["introduction"] == user2.introduction
    assert data["experience"] == user2.experience
    assert data["user"] == user2.id


def test_add_team_member__not_found(api_client, team, user):
    api_client.force_authenticate(user=user)

    data = api_client.post(
        f"/teams/{team.id}/members/",
        {
            "user": 10,
        },
        format="json",
    ).json()

    assert data["code"] == ResponseType.ParamValidationFailed.code


def test_add_team_member__manual(api_client, team, user):
    api_client.force_authenticate(user=user)

    data = api_client.post(
        f"/teams/{team.id}/members/",
        {
            "nickname": "test",
            "academy": 10,
            "degree": DegreeType.BACHELOR,
            "grade": 2021,
            "introduction": "test",
            "experience": ["test"],
        },
        format="json",
    ).json()["data"]

    assert data["nickname"] == "test"
    assert data["academy"]["id"] == 10
    assert data["degree"] == DegreeType.BACHELOR
    assert data["grade"] == 2021
    assert data["introduction"] == "test"
    assert data["experience"] == ["test"]
    assert data["user"] is None


def test_add_team_member__already_in_team(api_client, team, user, user2):
    TeamMember.objects.create(user=user2, team=team)
    api_client.force_authenticate(user=user)

    data = api_client.post(
        f"/teams/{team.id}/members/",
        {
            "user": user2.id,
        },
        format="json",
    ).json()

    assert data["code"] == ResponseType.ParamValidationFailed.code


def test_add_team_member__already_leader(api_client, team, user):
    api_client.force_authenticate(user=user)

    data = api_client.post(
        f"/teams/{team.id}/members/",
        {
            "user": user.id,
        },
        format="json",
    ).json()

    assert data["code"] == ResponseType.ParamValidationFailed.code


def test_delete_team_member(api_client, team, user, user2):
    tm = TeamMember.objects.create(user=user2, team=team)
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/teams/{team.id}/members/{tm.id}/")

    assert response.status_code == 204
    assert TeamMember.objects.filter(id=tm.id).count() == 0


def test_delete_team_member__not_found(api_client, team, user):
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/teams/{team.id}/members/10/")

    assert response.status_code == 404


def test_delete_team_member__not_in_team(api_client, team, user, user2):
    team2 = Team.objects.create(leader=user)
    tm = TeamMember.objects.create(user=user2, team=team2)
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/teams/{team.id}/members/{tm.id}/")

    assert response.status_code == 404


def test_delete_team_member__not_leader(api_client, team, user, user2):
    tm = TeamMember.objects.create(user=user2, team=team)
    api_client.force_authenticate(user=user2)

    response = api_client.delete(f"/teams/{team.id}/members/{tm.id}/")

    assert response.status_code == 404


def test_add_team_demand__anonymous(api_client, team):
    data = api_client.post(f"/teams/{team.id}/demands/", {}).json()

    assert data["code"] == ResponseType.NotLogin.code


def test_add_team_demand__not_found(api_client, user):
    api_client.force_authenticate(user=user)
    data = api_client.post(
        "/teams/1/demands/",
        {
            "role": 1,
            "number": 1,
            "detail": "test",
        },
    ).json()

    assert data["code"] == ResponseType.APINotFound.code


def test_add_team_demand(api_client, team, user, roles):
    api_client.force_authenticate(user=user)
    data = api_client.post(
        f"/teams/{team.id}/demands/",
        {
            "role": 1,
            "number": 1,
            "detail": "test",
        },
        format="json",
    ).json()["data"]

    assert data["role"]["id"] == 1
    assert data["number"] == 1
    assert data["detail"] == "test"


def test_update_team_demand(api_client, team, user, roles):
    td = TeamDemand.objects.create(
        team=team, role=roles[0], number=1, detail="test"
    )
    api_client.force_authenticate(user=user)

    data = api_client.put(
        f"/teams/{team.id}/demands/{td.id}/",
        {
            "role": 2,
            "number": 2,
            "detail": "test2",
        },
        format="json",
    ).json()["data"]

    assert data["role"]["id"] == 2
    assert data["number"] == 2
    assert data["detail"] == "test2"


def test_delete_team_demand(api_client, team, user, roles):
    td = TeamDemand.objects.create(
        team=team, role=roles[0], number=1, detail="test"
    )
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/teams/{team.id}/demands/{td.id}/")

    assert response.status_code == 204
    assert TeamDemand.objects.filter(id=td.id).count() == 0


def test_delete_team_demand__not_found(api_client, team, user):
    api_client.force_authenticate(user=user)

    response = api_client.delete(f"/teams/{team.id}/demands/10/")

    assert response.status_code == 404
