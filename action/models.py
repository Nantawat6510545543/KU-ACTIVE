from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone


class User(AbstractUser):
    profile_picture = models.TextField(blank=True)
    bio = models.TextField(blank=True)

    @property
    def participated_activity(self):
        # Filter and return the Activity objects where the user has participated
        return Activity.objects.filter(
            activity__participants=self, activity__is_participated=True)

    @property
    def favorited_activity(self):
        # Filter and return the Activity objects where the user has favorited
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


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


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
    background_picture = models.TextField(blank=True,default='')
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def participants(self):
        participants = User.objects.filter(
            participants__activity=self, participants__is_participated=True)
        return participants

    def __str__(self):
        """
        Returns a string of activity name.
        """
        return self.title

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
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

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
            bool: True if the current date and time are within the time range,
            and the number of participants is below the participant limit.
        """
        current_time = timezone.now()
        is_within_time_range = self.pub_date <= current_time <= self.end_date
        limit = self.participant_limit
        is_under_limit = (limit in (None, 0) or
                          self.participants.count() < limit)
        return is_within_time_range and is_under_limit


class ActivityStatus(models.Model):
    """
    Represents a participation for each user.
    """
    participants = models.ForeignKey(User, related_name='participants',
                                     on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, related_name='activity',
                                 on_delete=models.CASCADE)

    participation_date = models.DateTimeField('Participation date',
                                              default=timezone.now)

    is_participated = models.BooleanField(default=False)
    is_favorited = models.BooleanField(default=False)


class FriendStatus(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    )

    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="receiver")

    request_status = models.CharField(max_length=50, choices=STATUS_CHOICES,
                                      null=True, default=None)
    is_friend = models.BooleanField(default=False)
