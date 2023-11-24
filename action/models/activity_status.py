from django.db import models
from django.utils import timezone

from .user import User
from .activity import Activity


class ActivityStatus(models.Model):
    """Represents the participation status of a user in a specific activity."""

    participants = models.ForeignKey(User, related_name='participants',
                                     on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='activity',
                                 on_delete=models.CASCADE)

    participation_date = models.DateTimeField('Participation date',
                                              default=timezone.now)

    is_participated = models.BooleanField(default=False)
    is_favorited = models.BooleanField(default=False)
