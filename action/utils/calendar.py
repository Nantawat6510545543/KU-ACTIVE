from allauth.socialaccount.models import SocialApp, SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from decouple import config
import secrets


def build_service(request):
    if request.user.email:
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
    charset = "0123456789abcdefghijklmnopqrstuv"
    random_indices = [secrets.randbelow(32) for _ in range(100)]
    random_string = ''.join([charset[i] for i in random_indices])
    return random_string


def create_event(request, activity_id, **kwargs):
    service = build_service(request)
    if service is not None:
        new_event_code = generate_random_id()
        kwargs['id'] = new_event_code
        request.user.event_encoder[str(activity_id)] = new_event_code
        request.user.save()
        service.events().insert(calendarId='primary', body=kwargs).execute()


def remove_event(request, activity_id):
    event_id = str(activity_id)
    user = request.user
    service = build_service(request)
    if service is not None:
        if event_id in user.event_encoder:
            encoded_event = user.event_encoder[event_id]
            service.events().delete(calendarId='primary',
                                    eventId=encoded_event).execute()
            user.event_encoder[event_id] = generate_random_id()
            del user.event_encoder[event_id]
            user.save()
