from rest_framework_extensions.routers import ExtendedSimpleRouter

from . import views

router = ExtendedSimpleRouter()

urlpatterns = []

team_routes = router.register(r"", views.TeamViewSet, basename="team")
team_routes.register(  # 队员
    r"members",
    views.TeamMemberViewSet,
    basename="team-member",
    parents_query_lookups=["team__id"],
)

team_routes.register(  # 需求
    r"demands",
    views.TeamDemandViewSet,
    basename="team-demand",
    parents_query_lookups=["team__id"],
)


urlpatterns += router.urls
