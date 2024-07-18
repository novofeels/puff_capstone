from django.contrib.auth.models import User
from django.db import models
from .achievement import Achievement


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_achieved = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.achievement.description}"
