from rest_framework import serializers
from puffapi.models import Feedback
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ["id", "user", "date", "feedback"]
        read_only_fields = ["user", "date"]


class FeedbackViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        feedback = Feedback()
        feedback.user = request.user
        feedback.feedback = request.data["feedback"]
        feedback.save()

        serializer = FeedbackSerializer(feedback, context={"request": request})
        return Response(serializer.data)

    def list(self, request):
        feedback = Feedback.objects.all()
        serializer = FeedbackSerializer(
            feedback, many=True, context={"request": request}
        )
        return Response(serializer.data)
