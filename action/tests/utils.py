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
    def create_user(username='tester', password='password', **kwargs):
        user = User.objects.create_user(username=username, password=password)

        user_fields = {
            "email": None,
            "first_name": None,
            "last_name": None,
            "active": None,
        }

        user_fields.update(kwargs)

        if user_fields["email"] is not None:
            user.email = user_fields["email"]

        if user_fields["first_name"] is not None:
            user.first_name = user_fields["first_name"]

        if user_fields["last_name"] is not None:
            user.last_name = user_fields["last_name"]

        if user_fields["active"] is not None:
            user.active = user_fields["active"]

        user.save()
        return user

    @staticmethod
    def create_tag(name):
        tag = Tag(name=name)
        tag.save()
        return tag

    @staticmethod
    def create_activity(owner, **kwargs):
        defaults = {
            "title": "Test",
            "date": timezone.now() + timezone.timedelta(days=2),
            "pub_date": timezone.now(),
            "end_date": timezone.now() + timezone.timedelta(days=1),
            "description": None,
            "place": None,
            "full_description": None,
            "participant_limit": -1,
            "tags": None,
        }

        defaults.update(kwargs)

        activity = Activity.objects.create(
            owner=owner,
            title=defaults["title"],
            date=defaults["date"],
            pub_date=defaults["pub_date"],
            end_date=defaults["end_date"]
        )

        if defaults["description"] is not None:
            activity.description = defaults["description"]

        if defaults["place"] is not None:
            activity.place = defaults["place"]

        if defaults["full_description"] is not None:
            activity.full_description = defaults["full_description"]

        if (defaults["participant_limit"] is not None and
                defaults["participant_limit"] > 0):
            activity.participant_limit = defaults["participant_limit"]

        if defaults["tags"] is not None:
            activity.tags.set(defaults["tags"])

        activity.save()

        return activity

    @staticmethod
    def create_activity_status(participants, activity, **kwargs):
        defaults = {
            'participated': None,
            'favorite': None,
        }

        defaults.update(kwargs)

        activity_status = ActivityStatus.objects.create(
            participants=participants,
            activity=activity,
            is_participated=defaults['participated'],
            is_favorited=defaults['favorite']
        )

        activity_status.save()

        return activity_status

    @staticmethod
    def create_friend_status(sender, receiver, **kwargs):
        defaults = {
            'choices': None,
            'is_friend': None,
        }

        defaults.update(kwargs)

        friend_status = FriendStatus.objects.create(
            sender=sender,
            receiver=receiver,
            choices=defaults['choices'],
            is_friend=defaults['is_friend']
        )

        friend_status.save()

        return friend_status

