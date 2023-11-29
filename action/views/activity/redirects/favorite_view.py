from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from action.utils import fetch_activity_status


class FavoriteView(LoginRequiredMixin, View):
    """
    View for allowing a user to mark a specific activity as a favorite.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to mark as a favorite.

    Returns:
        HttpResponse: Redirect response to the activity detail view.
    """

    def get(self, request: HttpRequest, activity_id: int) -> HttpResponse:
        activity_status = fetch_activity_status(request, activity_id)

        if activity_status.is_favorited:
            messages.info(request, "You have already favorited this activity.")
        else:
            activity_status.is_favorited = True
            activity_status.save()
            messages.success(request, "You have successfully favorited this activity.")

        return redirect(reverse("action:detail", args=(activity_id,)))
