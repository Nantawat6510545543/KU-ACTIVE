from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from googleapiclient.errors import HttpError
from action.calendar import create_event, remove_event

from action.models import ActivityStatus, Activity
from action.utils import fetch_activity_status
from action.utils.calendar import user_is_login_with_google


@login_required
def participate(request, activity_id: int):
    """
    View for allowing a user to participate in a specific activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to participate in.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """
    activity = get_object_or_404(Activity, pk=activity_id)
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if not activity.is_published():
        messages.info(request, "Registration for the activity has not yet opened.")
    elif not activity.can_participate():
        messages.info(request, "This activity can no longer be participated in.")
    elif activity_status.is_participated:
        messages.info(request, "You are already participating.")
    else:
        if user_is_login_with_google(request):
            try:
                create_event(request, activity_id)  # Add activity to user calendar
            except HttpError:
                messages.info(request, "Calendar is not working, please Login again.")

        activity_status.is_participated = True
        activity_status.save()
        messages.success(request, "You have successfully participated.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def leave(request, activity_id: int):
    """
    View for allowing a user to leave a specific activity in which they are currently participating.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to leave.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_participated:
        activity_status.is_participated = False
        activity_status.save()
        messages.success(request, "You have left this activity.")

        if user_is_login_with_google(request):
            try:
                remove_event(request, activity_id)  # Remove activity from user calendar
            except HttpError:
                messages.info(request, "Calendar is not working, please Login again.")

    else:
        messages.info(request, "You are not currently participating in this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def favorite(request, activity_id: int):
    """
    View for allowing a user to mark a specific activity as a favorite.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to mark as a favorite.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_favorited:
        messages.info(request, "You have already favorited this activity.")
    else:
        activity_status.is_favorited = True
        activity_status.save()
        messages.success(request, "You have successfully favorited this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def unfavorite(request, activity_id: int):
    """
    View for allowing a user to remove a specific activity from their favorites.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to remove from favorites.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_favorited:
        activity_status.is_favorited = False
        activity_status.save()
        messages.success(request, "You have unfavorited this activity.")
    else:
        messages.info(request, "You have not currently favorite this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))
