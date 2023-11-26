import secrets

from allauth.socialaccount.models import SocialApp, SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from decouple import config
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from action.models.activity import Activity


@login_required
def build_service(request):
    """
    Build and return a Google Calendar API service instance for the authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
         Google Calendar API service instance.
    """
    app = SocialApp.objects.get(provider="google")
    token = SocialToken.objects.get(app=app, account__user=request.user)
    refresh_token = token.token_secret
    scope = ['https://www.googleapis.com/auth/calendar']
    user_info = {
        "client_id": config('GOOGLE_OAUTH_CLIENT_ID', str),
        "client_secret": config('GOOGLE_OAUTH_SECRET_KEY', str),
        "refresh_token": str(refresh_token),
    }
    creds = Credentials.from_authorized_user_info(info=user_info,
                                                  scopes=scope)
    return build('calendar', 'v3', credentials=creds)


def generate_random_id():
    """
    Generate a random alphanumeric string to be used as an event ID.

    Returns:
        str: Random alphanumeric string.
    """
    CHARSET = "0123456789abcdefghijklmnopqrstuv"
    random_indices = [secrets.randbelow(32) for _ in range(100)]
    random_string = ''.join([CHARSET[i] for i in random_indices])
    return random_string


def get_json_data(activity_id):
    """
    Get JSON data for creating a Google Calendar event based on the activity details.

    Args:
        activity_id (int): ID of the activity.

    Returns:
        dict: JSON data for creating a Google Calendar event.
    """
    activity = get_object_or_404(Activity, pk=activity_id)
    return {
        'summary': activity.title,
        'location': activity.place,
        'description': activity.description,
        'start': {
            'dateTime': activity.start_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': config('TIME_ZONE', default='UTC'),
        },
        'end': {
            'dateTime': activity.last_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': config('TIME_ZONE', default='UTC'),
        },
        'id': generate_random_id()  # new event code
    }


# TODO add update function + make a decorator 
@login_required
def create_event(request, activity_id):
    """
    Create a Google Calendar event for the specified activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): ID of the activity.
    """
    service = build_service(request)

    if service:
        data = get_json_data(activity_id)
        request.user.event_encoder[str(activity_id)] = data['id']
        request.user.save()
        service.events().insert(calendarId='primary', body=data).execute()


@login_required
def remove_event(request, activity_id):
    """
    Remove the Google Calendar event associated with the specified activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): ID of the activity.
    """
    event_id = str(activity_id)
    user = request.user
    service = build_service(request)

    if service and event_id in user.event_encoder:
        encoded_event = user.event_encoder[event_id]
        service.events().delete(calendarId='primary',
                                eventId=encoded_event).execute()
        del user.event_encoder[event_id]
        user.save()
