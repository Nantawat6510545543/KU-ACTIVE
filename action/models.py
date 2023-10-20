from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone
from decouple import config


# TODO use modelform
# TODO look into Manager and QuerySetManager class
# TODO use ABC for inheritance, not subclass

class User(AbstractUser):
    profile_picture = models.URLField(max_length=500,
                                      default=config("DEFAULT_IMAGE",
                                                     default=''))
    bio = models.TextField(blank=True)

    @property
    def participated_activity(self):
        return ActivityStatus.objects.filter(participants=self,
                                             is_participated=True)

    @property
    def favorited_activity(self):
        return ActivityStatus.objects.filter(participants=self,
                                             is_favorited=True)

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
    title = models.CharField(max_length=100, blank=True)
    date = models.DateTimeField('Date of Activity', null=True, blank=True)
    # TODO make default image, set blank=False
    picture = models.ImageField(blank=True)
    description = models.CharField('Description', max_length=200)
    participant_limit = models.IntegerField(null=True, blank=True,
                                            default=None)

    pub_date = models.DateTimeField('Date published',
                                    default=timezone.now)
    end_date = models.DateTimeField('Date ended',
                                    null=True, blank=True)
    full_description = models.TextField('Full Description', blank=True)
    # TODO make default picture, and change blank=False, don't delete this until done
    background_picture = models.ImageField(blank=True)
    place = models.CharField('Place', max_length=200, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def participants(self):
        participation = ActivityStatus.objects.filter(activity=self,
                                                      is_participated=True)
        participants = participation.values_list('participants__username',
                                                 flat=True)
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

    def __str__(self):
        return self.activity.title


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
