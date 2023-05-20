from feedbacks.models import Feedback
from feedbacks.serializers import FeedbackSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by("-id")
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)
