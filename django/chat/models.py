from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    name = models.CharField(max_length=20)
    members = models.ManyToManyField(User)

    def add_user(self, user):
        self.members.add(user)

    def remove_user(self, user):
        self.members.remove(user)


class Message(models.Model):
    content = models.CharField()
    date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name="messages"
    )
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages"
    )
