from django.db import models
from user.models import User


class Chat(models.Model):
    name = models.CharField(max_length=301, unique=True)
    members = models.ManyToManyField(User)
    private = models.BooleanField(default=True)

    def add_user(self, user):
        if self.private and self.members.count() > 2:
            raise Exception(
                "Tried to add more than 2 members on a private chat"
            )
        self.members.add(user)

    def remove_user(self, user):
        self.members.remove(user)

    def __str__(self):
        return self.name


class Message(models.Model):
    content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="messages"
    )
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )
