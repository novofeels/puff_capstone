# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from puffapi.models import Score
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone


# Serializer for Score
class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Score
        fields = ["user", "score", "date"]


@method_decorator(csrf_exempt, name="dispatch")
class ScoreViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False, methods=["post"], url_path="submit-score", url_name="submit_score"
    )
    def submit_score(self, request):
        user = request.user
        new_score = request.data.get("score")
        # Update the date

        if new_score is None:
            return Response(
                {"error": "score is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            score_instance = Score.objects.get(user=user)
            if new_score > score_instance.score:
                score_instance.score = new_score
                score_instance.date = timezone.now()
                score_instance.save()
                return Response(
                    {"message": "Score updated successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        "message": "Score not updated as it is not higher than the existing score"
                    },
                    status=status.HTTP_200_OK,
                )
        except Score.DoesNotExist:
            Score.objects.create(user=user, score=new_score, date=timezone.now())
            return Response(
                {"message": "Score submitted successfully"},
                status=status.HTTP_201_CREATED,
            )

    @action(
        detail=False, methods=["get"], url_path="leaderboard", url_name="leaderboard"
    )
    def leaderboard(self, request):
        scores = Score.objects.all().order_by("-score")
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="user-score", url_name="user_score")
    def get_user_score(self, request):
        user = request.user
        try:
            score_instance = Score.objects.get(user=user)
            serializer = ScoreSerializer(score_instance)
            return Response(serializer.data)
        except Score.DoesNotExist:
            return Response(
                {"error": "No score found for the user"},
                status=status.HTTP_404_NOT_FOUND,
            )
