from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class User(AbstractUser):
    profile_picture = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    event_encoder = models.JSONField(blank=True, null=True)

    @property
    def participated_activity(self):
        # Filter and return the Activity objects where the user has participated
        from .activity import Activity
        return Activity.objects.filter(
            activity__participants=self, activity__is_participated=True)

    @property
    def favorited_activity(self):
        # Filter and return the Activity objects where the user has favorited
        from .activity import Activity
        return Activity.objects.filter(
            activity__participants=self, activity__is_favorited=True)

    @property
    def friends(self):
        # First case, the friend request receiver is the current user
        # Second case, the friend request receiver is the current user
        # then both cases filter for only is_friend
        friend_objects = User.objects.filter(
            Q(sender__is_friend=True, sender__receiver=self) |
            Q(receiver__is_friend=True, receiver__sender=self)
        )
        return friend_objects

    def __str__(self):
        return self.username
