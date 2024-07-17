# views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from puffapi.models import Score
from django.contrib.auth.models import User
from rest_framework import serializers


# Serializer for Score
class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["score", "date"]


class SubmitScoreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        score = request.data.get("score")

        if score is None:
            return Response(
                {"error": "score is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            score = Score.objects.get(user=user)
            if score > score.score:
                score.score = score
                score.save()
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
            Score.objects.create(user=user, score=score)
            return Response(
                {"message": "Score submitted successfully"},
                status=status.HTTP_201_CREATED,
            )
