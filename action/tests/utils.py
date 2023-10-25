from django.test import TestCase
from django.contrib.sites.models import Site
from decouple import config
from django.utils import timezone
from allauth.socialaccount.models import SocialApp
from action.models import User, Activity, ActivityStatus, FriendStatus, Tag
from mysite.settings import SITE_ID, SITE_NAME, SITE_DOMAIN


class Tester(TestCase):
    """
    Utility class for creating test cases.
    """

    def setUp(self):
        """
        Set up the test environment.
        """
        super().setUp()
        site, _ = Site.objects.get_or_create(
            id=SITE_ID,
            defaults={
                'name': SITE_NAME,
                'domain': SITE_DOMAIN,
            },
        )

        self.social_app, _ = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Login with Google OAuth',
                'client_id': config('GOOGLE_OAUTH_CLIENT_ID'),
                'secret': config('GOOGLE_OAUTH_SECRET_KEY'),
            },
        )
        self.social_app.sites.add(site)
        self.social_app.save()

    @staticmethod
    def create_user(username, password, first_name):
        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.save()
        return user

    @staticmethod
    def create_tag(name):
        tag = Tag(name=name)
        tag.save()
        return tag

    @staticmethod
    def create_activity(owner, date=None, pub_date=None, end_date=None,
                        participant_limit=-1, tags=None):
        activity = Activity.objects.create(owner=owner)

        if date is None:
            activity.date = timezone.now() + timezone.timedelta(days=2)
        if pub_date is None:
            activity.pub_date = timezone.now()
        if end_date is None:
            activity.end_date = timezone.now() + timezone.timedelta(days=1)
        if participant_limit > -1:
            activity.participant_limit = participant_limit
        if tags is not None:
            activity.tags.set(tags)

        activity.save()
        return activity

    @staticmethod
    def create_activity_status(participants, activity, participated=True,
                               favorite=False):
        activity_status = ActivityStatus.objects.create(
            participants=participants,
            activity=activity,
            is_participated=participated,
            is_favorited=favorite
        )
        activity_status.save()

        return activity_status

    @staticmethod
    def create_friend_status(sender, receiver, choices="Pending"):
        friend_status = FriendStatus.objects.create(
            sender=sender,
            receiver=receiver,
            choices=choices,
        )
        friend_status.save()
        return friend_status
