from django.contrib.auth.models import User
from django.db import models


from django.contrib.auth.models import User
from django.db import models


class Achievement(models.Model):
    badge_image = models.ImageField(upload_to="badges/")
    description = models.CharField(max_length=255)
    users = models.ManyToManyField(
        User, through="UserAchievement", related_name="achievements"
    )

    def __str__(self):
        return self.description
