from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField('self', through="IsFriendsWith")


class IsFriendsWith(models.Model):
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user1'
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user2'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["user1", "user2"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_add",
                check=~models.Q(user1=models.F("user2")),
            ),
        ]
