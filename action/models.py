import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="friendship_requests_sent", )
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name="friendship_requests_received", )


class Activity(models.Model):
    """
    Represents an activity in the application.
    """
    owner = models.ForeignKey(User, related_name='owner',
                              on_delete=models.CASCADE)

    activity_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('Date published',
                                    default=timezone.now)
    end_date = models.DateTimeField('Date ended',
                                    null=True, blank=True)

    def __str__(self):
        """
        Returns a string of activity name.
        """
        return self.activity_name

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        """
        Checks if the activity was published recently.

        Returns:
            bool: True if the activity was published within the last day,
                  False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Is published?',
    )
    def is_published(self):
        """
        Checks if the activity is published.

        Returns:
            bool: True if the current date is on or after the activity's
            publication date.
        """
        now = timezone.now()
        return now >= self.pub_date

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Can participate?',
    )
    def can_participate(self):
        """
        checks if participation is allowed for this activity.

        Returns:
            bool: True if the current date/time
                  is between pub_date and end_date (if not null).
                  If end_date is null,
                  participation is allowed anytime after pub_date.
        """
        now = timezone.now()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date


class Participation(models.Model):
    participants = models.ForeignKey(User, related_name='participants',
                                     on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='activity',
                                 on_delete=models.CASCADE)
    participation_date = models.DateTimeField('Participation date',
                                              default=timezone.now)
