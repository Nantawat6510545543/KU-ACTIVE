from django.contrib.auth.decorators import login_required
from action.utils import build_service, create_event_json_data, create_event_json_data_without_event_id


@login_required
def create_event(request, activity_id):
    """
    Create a Google Calendar event for the specified activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): ID of the activity.
    """
    activity_id = str(activity_id)  # use string, too late to use (int) now
    service = build_service(request)

    if service:
        data = create_event_json_data(activity_id)
        request.user.event_encoder[activity_id] = data[activity_id]['id']
        request.user.save()
        service.events().insert(calendarId='primary', body=data[activity_id]).execute()


@login_required
def update_event(request, activity_id):
    activity_id = str(activity_id)  # use string, too late to use (int) now

    # Get the existing event
    service = build_service(request)

    event_id = request.user.event_encoder[activity_id]
    event = service.events().get(calendarId='primary', eventId=event_id).execute()

    # Update the event properties
    updated_event = create_event_json_data_without_event_id(activity_id)
    print(f"{updated_event =}")
    event.update(updated_event[activity_id])

    # Update the event in Google Calendar
    service.events().update(calendarId='primary', eventId=event_id, body=updated_event[activity_id]).execute()


@login_required
def remove_event(request, activity_id):
    """
    Remove the Google Calendar event associated with the specified activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): ID of the activity.
    """
    activity_id = str(activity_id)  # use string, too late to use (int) now
    user = request.user
    service = build_service(request)

    if service and activity_id in user.event_encoder:
        encoded_event = user.event_encoder[activity_id]
        service.events().delete(calendarId='primary',
                                eventId=encoded_event).execute()
        del user.event_encoder[activity_id]
        user.save()
