from django.contrib.auth.models import User
from django.db import models


class Score(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    score = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.score}"
