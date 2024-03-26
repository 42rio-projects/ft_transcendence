from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q


class IsFriendsWith(models.Model):
    user1 = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user1'
    )
    user2 = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user2'
    )

    def save(self, *args, **kwargs):
        if IsFriendsWith.objects.filter(
                user1=self.user2, user2=self.user1
        ).exists():
            # Friendship already exists, don't create a duplicate entry
            pass
        else:
            super().save(*args, **kwargs)

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


class IsBlockedBy(models.Model):
    blocker = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='blocks'
    )
    blocked = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='blocked_by'
    )

    def save(self, *args, **kwargs):
        friendship = IsFriendsWith.objects.filter(
            user1=self.blocker, user2=self.blocked
        )
        if friendship.exists():
            friendship[0].delete()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["blocker", "blocked"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_block",
                check=~models.Q(blocker=models.F("blocked")),
            ),
        ]


class FriendInvite(models.Model):
    sender = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='friend_invites_sent'
    )
    receiver = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='friend_invites_received'
    )

    def clean(self):
        """
        Custom validation to prevent sending invites to friends.
        """
        if IsFriendsWith.objects.filter(
            Q(user1=self.sender, user2=self.receiver) |
            Q(user1=self.receiver, user2=self.sender)
        ).exists():
            raise ValidationError(
                'You cannot send a friend invite to a friend.'
            )

    def save(self, *args, **kwargs):
        """
        Overridden save method to enforce validation
        """
        self.clean()
        invite = FriendInvite.objects.filter(
            sender=self.receiver, receiver=self.sender
        )
        if invite.exists():
            invite[0].respond(accepted=True)
        else:
            super().save(*args, **kwargs)

    def respond(self, accepted):
        if accepted is True:
            friendship = IsFriendsWith(user1=self.sender, user2=self.receiver)
            friendship.save()
        self.delete()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="%(app_label)s_%(class)s_unique_relationships",
                fields=["sender", "receiver"]
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_prevent_self_invite",
                check=~models.Q(sender=models.F("receiver")),
            ),
        ]
