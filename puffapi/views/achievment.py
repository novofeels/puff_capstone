# views.py
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from puffapi.models import Achievement, UserAchievement
from django.contrib.auth.models import User


# Serializers
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "badge_image", "description"]


class UserAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer()

    class Meta:
        model = UserAchievement
        fields = ["id", "achievement", "time_achieved"]


# Views
class ListAchievementsView(generics.ListAPIView):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserAchievementsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_achievements = UserAchievement.objects.filter(user=user)
        serializer = UserAchievementSerializer(user_achievements, many=True)
        return Response(serializer.data)
