from django.contrib.sites.models import Site
from django.utils import timezone
from allauth.socialaccount.models import SocialApp
from action.models import User, Activity, ActivityStatus, FriendStatus, Tag
from mysite.settings import SITE_ID, SITE_NAME, SITE_DOMAIN


def create_social_app():
    site, _ = Site.objects.get_or_create(
        id=SITE_ID,
        defaults={
            'name': SITE_NAME,
            'domain': SITE_DOMAIN,
        },
    )

    social_app, _ = SocialApp.objects.get_or_create(
        provider='google',
        defaults={
            'name': 'Login with Google OAuth',
            'client_id': "",
            'secret': "",
        },
    )
    social_app.sites.add(site)
    return social_app

def create_user(username='tester', password='password', **kwargs):
    user = User.objects.create_user(username=username, password=password)

    user_fields = {
        "event_encoder": {},
        "email": None,
        "first_name": None,
        "last_name": None,
        "active": None
    }

    user_fields.update(kwargs)

    user.email = user_fields["event_encoder"]

    if user_fields["email"] is not None:
        user.email = user_fields["email"]

    if user_fields["first_name"] is not None:
        user.first_name = user_fields["first_name"]

    if user_fields["last_name"] is not None:
        user.last_name = user_fields["last_name"]

    if user_fields["active"] is not None:
        user.active = user_fields["active"]

    return user

def create_tag(name):
    tag = Tag(name=name)
    tag.save()
    return tag

def create_activity(owner, **kwargs):
    defaults = {
        "title": "Test",
        "start_date": timezone.now(),
        "last_date": timezone.now() + timezone.timedelta(days=1),
        "pub_date": timezone.now() + timezone.timedelta(days=2),
        "end_date": timezone.now() + timezone.timedelta(days=3),
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
        start_date=defaults["start_date"],
        last_date=defaults["last_date"],
        pub_date=defaults["pub_date"],
        end_date=defaults["end_date"]
    )

    if defaults["description"] is not None:
        activity.description = defaults["description"]

    if defaults["place"] is not None:
        activity.place = defaults["place"]

    if defaults["full_description"] is not None:
        activity.full_description = defaults["full_description"]

    if (defaults["participant_limit"] is not None):
        activity.participant_limit = defaults["participant_limit"]

    if defaults["tags"] is not None:
        activity.tags.set(defaults["tags"])

    return activity

def create_activity_status(participants, activity, participated=True,
                           favorite=None):
    activity_status = ActivityStatus.objects.create(
        participants=participants,
        activity=activity,
        is_participated=participated
    )

    if favorite is not None:
        activity_status.is_favorited = favorite

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
    if (request_status is not None and
            request_status.title() not in ['Pending', 'Accepted', 'Declined']):
        request_status = None

    friend_status = FriendStatus.objects.create(
        sender=sender,
        receiver=receiver,
    )
    if request_status is not None:
        friend_status.request_status = request_status
        friend_status.is_friend = request_status == 'Accepted'

    return friend_status
