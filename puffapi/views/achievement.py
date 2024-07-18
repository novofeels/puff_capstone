from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from puffapi.models import Achievement, UserAchievement
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.utils import timezone


# Serializer for Achievement
class AchievementSerializer(serializers.ModelSerializer):
    achieved = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = ["id", "badge_image", "description", "achieved"]

    def get_achieved(self, obj):
        user = self.context["request"].user
        return UserAchievement.objects.filter(user=user, achievement=obj).exists()


class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ["id", "date_achieved"]


# ViewSet for Achievement
class Achievements(ViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        achievements = Achievement.objects.all()
        serializer = AchievementSerializer(
            achievements, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        achievement_id = request.data.get("achievement_id")

        if not achievement_id:
            return Response(
                {"error": "achievement_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            achievement = Achievement.objects.get(pk=achievement_id)
        except Achievement.DoesNotExist:
            return Response(
                {"error": "Invalid achievement_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        if UserAchievement.objects.filter(user=user, achievement=achievement).exists():
            return Response(
                {"message": "Badge already obtained"}, status=status.HTTP_200_OK
            )

        UserAchievement.objects.create(
            user=user, achievement=achievement, date_achieved=timezone.now()
        )
        return Response(
            {"message": "UserAchievement created successfully"},
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, pk=None):
        user = request.user
        try:
            achievement = Achievement.objects.get(pk=pk)
            user_achievement = UserAchievement.objects.get(
                user=user, achievement=achievement
            )
            user_achievement.delete()
            return Response(
                {"message": "UserAchievement deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Achievement.DoesNotExist:
            return Response(
                {"error": "Achievement does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except UserAchievement.DoesNotExist:
            return Response(
                {"error": "UserAchievement does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
