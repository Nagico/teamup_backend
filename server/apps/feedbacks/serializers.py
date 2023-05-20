from feedbacks.models import Feedback
from rest_framework import serializers


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["content", "type"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Feedback.objects.create(user=user, **validated_data)
