from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    bio = models.TextField(blank=True)

    @property
    def participated_activity(self):
        participation = ActivityStatus.objects.filter(participants=self)
        participated_activity = participation.values_list('activity__title', flat=True)
        return participated_activity

    @property
    def friends(self):
        return FriendStatus.objects.filter(Q(is_friend=True) & 
            (Q(sender=self) | Q(receiver=self)))

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
    title = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField('Date of Activity',
                                default=timezone.now() +
                                timezone.timedelta(days=30))
    picture = models.ImageField(blank=True)  # TODO make default image, set blank=False<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    description = models.CharField('Description', max_length=200)
    participant_limit = models.IntegerField(null=True, blank=True, default=None)

    pub_date = models.DateTimeField('Date published',
                                    default=timezone.now)
    end_date = models.DateTimeField('Date ended',
                                    default=timezone.now() +
                                    timezone.timedelta(days=30))

    full_description = models.TextField('Full Description', blank=True)
    background_picture = models.ImageField(blank=True)  # TODO <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    place = models.CharField('Place', max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def participants(self):
        participation = ActivityStatus.objects.filter(activity=self)
        participants = participation.values_list('participants__username', flat=True)
        return participants

    @property
    def participant_count(self):
        return ActivityStatus.objects.filter(activity=self).count()

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
            bool: True if the current date/time
                  is between pub_date and end_date (if not null).
                  If end_date is null,
                  participation is allowed anytime after pub_date.
        """
        now = timezone.now()
        if self.end_date is None:
            return now >= self.pub_date
        return self.pub_date <= now <= self.end_date


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

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")

    request_status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, default=None)
    is_friend = models.BooleanField(default=False)
