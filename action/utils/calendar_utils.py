from allauth.socialaccount.models import SocialApp, SocialToken, SocialAccount
from django.http import HttpRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from decouple import config

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from action.models.activity import Activity

API_NAME = 'calendar'
API_VERSION = 'v3'
CHARSET = "0123456789abcdefghijklmnopqrstuv"


@login_required
def build_service(request) -> Resource:
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
    return build(API_NAME, API_VERSION, credentials=creds)


def get_event_json_data(activity_id, generate_event_id=False) -> dict[str, dict]:
    """
    Get JSON data for creating a Google Calendar event based on the activity details.

    Args:
        activity_id (int): ID of the activity.

    Returns:
        dict: JSON data for creating a Google Calendar event.
    """
    activity = get_object_or_404(Activity, pk=activity_id)

    data = {
        activity_id: {
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
        }
    }

    if generate_event_id:
        data[activity_id]['id'] = get_random_string(length=100, allowed_chars=CHARSET)
    return data

def get_event_id(request: HttpRequest, activity_id: str) -> str:  # return random string
    return request.user.event_encoder.get(activity_id, None)

def user_is_login_with_google(user) -> bool:
    """
    Check if the user is logged in with a Google social account.

    Args:
        user (User): The user object.

    Returns:
        bool: True if the user is logged in with Google, False otherwise.
    """
    return SocialAccount.objects.filter(user=user, provider='google').exists()
