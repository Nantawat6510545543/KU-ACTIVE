from datetime import timedelta

from django.contrib import admin
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from .user import User
from .tag import Tag


class Activity(models.Model):
    """
    Represents an activity in the application.
    """
    owner = models.ForeignKey(User, related_name='owner',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField('Date published', default=timezone.now)
    end_date = models.DateTimeField('Application Deadline', null=True,
                                    blank=True)
    start_date = models.DateTimeField('Date of Activity', null=True,
                                      blank=True)
    last_date = models.DateTimeField('Last date of activity', null=True,
                                     blank=True)
    description = models.CharField('Description', max_length=200)
    participant_limit = models.PositiveIntegerField(null=True, blank=True,
                                                    default=None)
    place = models.CharField('Place', max_length=200, blank=True)
    full_description = models.TextField('Full Description', blank=True)
    picture = models.TextField(blank=True, default='')
    background_picture = models.JSONField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def participants(self) -> QuerySet[User]:
        participants = User.objects.filter(participants__activity=self,
                                           participants__is_participated=True)
        return participants

    @property
    @admin.display(description='Count')
    def participant_count(self) -> int:
        """
        Get the count of participants for this activity.

        Returns:
            int: The number of participants.
        """
        return self.participants.count()

    @property
    @admin.display(description='Time remain')
    def time_remain(self) -> timedelta:
        """
        Return the time remaining until registration close.

        Returns:
            str: A string representing the time remaining.
                 If the remaining time is zero or negative,
                 it returns "0" second difference
        """
        time_diff = self.end_date - timezone.now()
        zero_diff = timezone.timedelta(seconds=0)
        return max(zero_diff, time_diff)

    @property
    @admin.display(description='Remaining')
    def remaining_space(self) -> int | None:
        """
       Calculate the number of remaining participant spaces in the activity.

       Returns:
           int: The number of remaining spaces if there is a limit,
                    or None if there's no limit.
       """
        if self.participant_limit:
            return self.participant_limit - self.participant_count  # Normal case
        return None  # If no limit is set

    def __str__(self):
        """
        Returns a string of activity name.
        """
        return self.title

    @admin.display(boolean=True, description='Published recently?')
    def was_published_recently(self) -> bool:
        """
        Checks if the activity was published recently.

        Returns:
            bool: True if the activity was published within the last day,
                  False otherwise.
        """
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    @admin.display(boolean=True, description='Is published?')
    def is_published(self) -> bool:
        """
        Checks if the activity is published.

        Returns:
            bool: True if the current date is on or after the activity's
                  publication date.
        """
        now = timezone.now()
        return now >= self.pub_date

    @admin.display(boolean=True, description='Can participate?')
    def can_participate(self) -> bool:
        """
        checks if participation is allowed for this activity.

        Returns:
            bool: True if the current date are within the activity's time range
            and there are remaining participant spaces available.
        """
        if self.remaining_space == 0:
            return False
        return self.pub_date <= timezone.now() <= self.end_date
