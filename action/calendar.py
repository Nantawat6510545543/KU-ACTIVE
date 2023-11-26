from django.contrib.auth.decorators import login_required
from action.utils import build_service, get_json_data


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


# @login_required
# def update_event(request, activity_id):
#     # Get the existing event
#     service = build_service(request)
#     event_id = str(activity_id)
#     event = service.events().get(calendarId='primary', eventId=event_id).execute()

#     # Update the event properties
#     event.update(get_json_data(activity_id))

#     # Update the event in Google Calendar
#     service.events().update(calendarId='primary', eventId=event_id, body=event).execute()


# @login_required
# Iterate through each user
# for user in users:
#     # Retrieve the user's stored credentials from your database
#     stored_credentials = get_user_credentials(user.id)

#     # Check if the stored credentials are expired, and refresh if necessary
#     if stored_credentials and stored_credentials.expired and stored_credentials.refresh_token:
#         stored_credentials.refresh(Request())

#     # Build the Google Calendar API service
#     service = build('calendar', 'v3', credentials=stored_credentials)

#     # Update the event in the user's calendar
#     updated_event = service.events().update(calendarId='primary', eventId=event_id, body=new_event_data).execute()


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
