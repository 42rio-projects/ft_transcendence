from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.core.exceptions import ValidationError


class User(AbstractUser):
    friends = models.ManyToManyField(
        'self',
        through="IsFriendsWith",
        symmetrical=True
    )
    blocked_list = models.ManyToManyField(
        'self',
        through="IsBlockedBy",
        symmetrical=False
    )
    friend_invites = models.ManyToManyField(
        'self',
        through='FriendInvite',
        symmetrical=False,
        related_name='friend_invites_set'
    )

    def get_friends(self):
        friendships = IsFriendsWith.objects.filter(
            Q(user1=self) | Q(user2=self)
        ).prefetch_related('user1', 'user2')
        friends = []
        for friendship in friendships:
            if friendship.user1 != self:
                friends.append(friendship.user1)
            elif friendship.user2 != self:
                friends.append(friendship.user2)
        return friends


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

    def save(self, *args, **kwargs):
        if IsFriendsWith.objects.filter(user1=self.user2, user2=self.user1).exists():
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
        User,
        on_delete=models.CASCADE,
        related_name='blocks'
    )
    blocked = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blocked_by'
    )

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
        User,
        on_delete=models.CASCADE,
        related_name='friend_invites_sent'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friend_invites_received'
    )

    def clean(self):
        """
        Custom validation to prevent sending invites to fiends.
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
        Overridden save method to enforce validation and superclass save.
        """
        self.clean()  # Call the custom validation
        super().save(*args, **kwargs)

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
