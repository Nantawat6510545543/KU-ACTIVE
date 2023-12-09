from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from googleapiclient.errors import HttpError

from action.calendar import create_event
from action.models import Activity
from action.utils import fetch_activity_status
from action.utils.calendar_utils import user_is_login_with_google


class ActivityParticipateView(LoginRequiredMixin, View):
    """
    View for allowing a user to participate in a specific activity.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to participate in.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """

    def get(self, request: HttpRequest, activity_id: int) -> HttpResponse:
        activity = get_object_or_404(Activity, pk=activity_id)
        activity_status = fetch_activity_status(request, activity_id)

        if not activity.is_published():
            messages.info(request, "Registration for the activity has not yet opened.")
        elif not activity.can_participate():
            messages.info(request, "This activity can no longer be participated in.")
        elif activity_status.is_participated:
            messages.info(request, "You are already participating.")
        else:
            if user_is_login_with_google(request.user):
                try:
                    create_event(request, activity_id)  # Add activity to user calendar
                except HttpError:
                    messages.info(request, "Calendar is not working, please Login again.")

            activity_status.is_participated = True
            activity_status.save()
            messages.success(request, "You have successfully participated.")

        return redirect(reverse("action:detail", args=(activity_id,)))
