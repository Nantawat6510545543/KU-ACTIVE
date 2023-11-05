from django.contrib import admin
from django.db import models
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
    background_picture = models.TextField(blank=True, default='')
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def participants(self):
        participants = User.objects.filter(participants__activity=self,
                                           participants__is_participated=True)
        return participants

    # TODO delegate some of these to html
    @property
    @admin.display(description='Time remain')
    def time_remain(self):
        """
        Return the time remaining until registration close.

        Returns:
            str: A string representing the time remaining.
                 If the remaining time is zero or negative,
                 it returns "Registration closed"
        """
        now = timezone.now()
        time_difference = self.end_date - now
        if time_difference.total_seconds() > 0:
            days = time_difference.days
            hours, seconds = divmod(time_difference.seconds, 3600)
            return f"{days} days, {hours} hours"
        return "Registration closed"

    @property
    @admin.display(description='Count')
    def participant_count(self):
        """
        Get the count of participants for this activity.

        Returns:
            int: The number of participants.
        """
        return self.participants.count()

    @property
    @admin.display(description='Remaining')
    def remaining_space(self):
        """
       Calculate the number of remaining participant spaces in the activity.

       Returns:
           int/str: The number of remaining spaces if there is a limit,
                    or "No limit" if there's no limit.
       """
        limit = self.participant_limit
        if limit is None or limit == 0:
            return "No limit"
        return max(0, limit - self.participant_count)

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
    def can_participate(self):
        """
        checks if participation is allowed for this activity.

        Returns:
            bool: True if the current date are within the activity's time range
            and there are remaining participant spaces available.
        """
        now = timezone.now()
        is_within_time_range = self.pub_date <= now <= self.end_date
        remaining_space = self.remaining_space
        if remaining_space == "No limit":
            return is_within_time_range
        return is_within_time_range and remaining_space > 0
