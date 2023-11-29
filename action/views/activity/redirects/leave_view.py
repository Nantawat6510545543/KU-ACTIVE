from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from googleapiclient.errors import HttpError

from action.calendar import remove_event
from action.utils import fetch_activity_status
from action.utils.calendar import user_is_login_with_google


class LeaveView(LoginRequiredMixin, View):
    """
    View for allowing a user to leave a specific activity in which they are currently participating.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to leave.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """

    def get(self, request: HttpRequest, activity_id: int) -> HttpResponse:
        activity_status = fetch_activity_status(request, activity_id)

        if activity_status.is_participated:
            activity_status.is_participated = False
            activity_status.save()
            messages.success(request, "You have left this activity.")

            if user_is_login_with_google(request.user):
                try:
                    remove_event(request, activity_id)  # Remove activity from user calendar
                except HttpError:
                    messages.info(request, "Calendar is not working, please Login again.")

        else:
            messages.info(request, "You are not currently participating in this activity.")

        return redirect(reverse("action:detail", args=(activity_id,)))
