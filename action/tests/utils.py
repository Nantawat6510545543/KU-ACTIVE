from abc import ABC
from django.contrib.sites.models import Site
from django.utils import timezone
from django.test import RequestFactory, TestCase
from django.urls import reverse
from allauth.socialaccount.models import SocialApp

from action.models import User, Activity, ActivityStatus, FriendStatus, Category
from mysite.settings import SITE_ID, SITE_NAME, SITE_DOMAIN

USER_DATA_1 = {
    "username": "John",
    "password": "abc",
    "email": "test1@example.com"
}

USER_DATA_2 = {
    "username": "Jane",
    "password": "abc",
    "email": "test2@example.com"
}

SITE_DEFAULT_DATA = {
    'name': SITE_NAME,
    'domain': SITE_DOMAIN
}

SOCIAL_APP_DEFAULT_DATA = {
    'name': 'Login with Google OAuth',
    'client_id': "",
    'secret': "",
}

REQUEST_DEFAULT_DATA = {
    'tag': 'title',
    'q': 'test'
}


class FriendStatusViewSetup(ABC, TestCase):
    """Abstract base class for setting up test cases related to FriendStatus views."""

    def setUp(self) -> None:
        """Set up the test case by creating two user objects."""
        self.user_1 = create_user(**USER_DATA_1)
        self.user_2 = create_user(**USER_DATA_2)


def create_social_app():
    """
    Create a social app instance.

    Returns:
        SocialApp: The created SocialApp instance.
    """
    site, _ = Site.objects.get_or_create(
        id=SITE_ID, defaults=SITE_DEFAULT_DATA)

    social_app, _ = SocialApp.objects.get_or_create(
        provider='google', defaults=SOCIAL_APP_DEFAULT_DATA)

    social_app.sites.add(site)
    return social_app


def create_user(username='tester', password='password', **kwargs):
    """
    Create a user instance.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.
        **kwargs: Additional keyword arguments for customizing the user object.

    Returns:
        User: The created User instance.
    """
    user_fields = {
        "username": username,
        "password": password,
        "event_encoder": {},
        "email": kwargs.get("email", None),
        "first_name": kwargs.get("first_name", ""),
        "last_name": kwargs.get("last_name", ""),
        "is_active": kwargs.get("is_active", True)
    }

    return User.objects.create_user(**user_fields)


def create_category(name):
    """
    Create a category instance.

    Args:
        name (str): The name of the category.

    Returns:
        Category: The created Category instance.
    """
    return Category.objects.create(name=name)


def create_activity(owner, **kwargs):
    """
    Create an activity instance.

    Args:
        owner (User): The owner of the activity.
        **kwargs: Additional keyword arguments for customizing the activity object.

    Returns:
        Activity: The created Activity instance.
    """
    activity_data = {
        "owner": owner,
        "title": kwargs.get("title", "Test"),
        "pub_date": kwargs.get("pub_date", timezone.now()),
        "end_date": kwargs.get("end_date", timezone.now() + timezone.timedelta(days=1)),
        "start_date": kwargs.get("start_date", timezone.now() + timezone.timedelta(days=2)),
        "last_date": kwargs.get("last_date", timezone.now() + timezone.timedelta(days=3)),
        "description": kwargs.get("description", ""),
        "place": kwargs.get("place", None),
        "full_description": kwargs.get("full_description", None),
        "participant_limit": kwargs.get("participant_limit", None),
    }

    activity = Activity.objects.create(**activity_data)

    # Set categories after activity creation
    categories = kwargs.get("categories", None)
    if categories:
        activity.categories.set(categories)

    return activity


def create_activity_status(participants, activity, is_participated=True,
                           is_favorited=False):
    """
    Create an activity status instance.

    Args:
        participants (User): The user participating in the activity.
        activity (Activity): The activity object.
        is_participated (bool): Whether the user has participated in the activity. Default is True.
        is_favorited (bool): Whether the user has favorited the activity. Default is False.

    Returns:
        ActivityStatus: The created ActivityStatus instance.
    """
    activity_status = ActivityStatus.objects.create(
        participants=participants,
        activity=activity,
        is_participated=is_participated,
        is_favorited=is_favorited
    )
    return activity_status


def create_friend_status(sender: User, receiver: User,
                         request_status: str = None) -> FriendStatus:
    """
    Create a friend status record in the database.

    Args:
        sender (User): The User who initiated the friendship request.
        receiver (User): The User who received the friendship request.
        request_status (str, optional): The request status, which can be one of 'Pending',
            'Accepted', or 'Declined'. Defaults to None if not specified or if an invalid
            status is provided.

    Returns:
        FriendStatus: The created FriendStatus object representing the friendship request.

    Note:
        - The created FriendStatus object will have an 'is_friend' field set to True if the
          request_status is 'Accepted', indicating that the users are now friends.
    """
    STATUS_CHOICES = [choice[0] for choice in FriendStatus.STATUS_CHOICES]
    IS_FRIEND = (request_status == 'Accepted')

    if request_status and request_status.title() not in STATUS_CHOICES:
        request_status = None

    friend_status = FriendStatus.objects.create(
        sender=sender,
        receiver=receiver,
        request_status=request_status,
        is_friend=IS_FRIEND
    )

    return friend_status


def create_request(view, args, user=None, data=None):
    """
    Create a request instance for testing views.

    Args:
        view (str): The view name or URL pattern for which the request is intended.
        args (list): The positional arguments for the view.
        user (User, optional): The user associated with the request. Defaults to None.
        data (dict): The request data. Defaults to REQUEST_DEFAULT_DATA.

    Returns:
        HttpRequest: The created HttpRequest instance.
    """
    if data is None:
        data = REQUEST_DEFAULT_DATA
    request = RequestFactory().get(reverse(view, args=args), data)
    request.user = user
    return request


def quick_join(participants, activity):
    """
    Given participants name and activity object, automatically join an activity.

    Args:
        participants (str): The name of the participant.
        activity (Activity): The activity object.
    """
    create_activity_status(create_user(participants), activity,
                           is_participated=True)
