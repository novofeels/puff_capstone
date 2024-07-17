from django.contrib.auth.models import User
from django.db import models


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    feedback = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}"
