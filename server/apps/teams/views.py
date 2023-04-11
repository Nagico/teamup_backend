from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin
from teams.models import Team, TeamDemand, TeamMember
from teams.serializers import (
    TeamDemandSerializer,
    TeamInfoSerializer,
    TeamMemberSerializer,
    TeamSerializer,
)
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType


class TeamViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Team.objects.order_by("-update_time")
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["activity__id"]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return self.queryset.filter(public=True)
        return self.queryset.filter(
            Q(public=True) | Q(leader=self.request.user)
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return TeamInfoSerializer
        return super().get_serializer_class()


class TeamNestedViewSetMixin(NestedViewSetMixin):
    # prepare request.team
    def initial(self, request, *args, **kwargs):
        team_id = self.get_parents_query_dict()["team__id"]
        team = Team.objects.filter(id=team_id).first()
        if not team:
            raise ApiException(ResponseType.APINotFound)

        request.team = team
        return super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(
            team=self.request.team, team__leader=self.request.user
        )


class TeamMemberViewSet(TeamNestedViewSetMixin, viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAuthenticated]


class TeamDemandViewSet(TeamNestedViewSetMixin, viewsets.ModelViewSet):
    queryset = TeamDemand.objects.all()
    serializer_class = TeamDemandSerializer
    permission_classes = [IsAuthenticated]
