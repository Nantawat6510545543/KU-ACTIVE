from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q, QuerySet


class User(AbstractUser):
    """Custom User model extending AbstractUser for additional features."""

    profile_picture = models.TextField(blank=True)
    background_picture = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    event_encoder = models.JSONField(blank=True, default=dict)

    @property
    def participated_activity(self) -> QuerySet['Activity']:
        """
        Filter and return the Activity objects where the user has participated.

        Returns:
            QuerySet: Filtered Activity objects.
        """
        from .activity import Activity
        return Activity.objects.filter(
            activity__participants=self, activity__is_participated=True)

    @property
    def favorited_activity(self) -> QuerySet['Activity']:
        """
        Filter and return the Activity objects where the user has favorited.

        Returns:
            QuerySet: Filtered Activity objects.
        """
        from .activity import Activity
        return Activity.objects.filter(
            activity__participants=self, activity__is_favorited=True)

    @property
    def friends(self) -> QuerySet['User']:
        """
        Get a QuerySet of User objects representing friends of the current user.

        Returns:
            QuerySet: User objects representing friends.
        """
        friend_objects = User.objects.filter(
            Q(sender__is_friend=True, sender__receiver=self) |
            Q(receiver__is_friend=True, receiver__sender=self)
        )
        return friend_objects.distinct()

    def __str__(self):
        """
        Return the username as the string representation of the user.

        Returns:
            str: The username.
        """
        return self.username
