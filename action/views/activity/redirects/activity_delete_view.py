from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from action.models import Activity


class ActivityDeleteView(LoginRequiredMixin, View):
    """
    View for deleting a specific activity owned by the user.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to delete.

    Returns:
        HttpResponse: Redirect response to the activity manage view.
    """

    def get(self, request: HttpRequest, activity_id: int) -> HttpResponse:
        try:
            activity = Activity.objects.get(id=activity_id)
        except Activity.DoesNotExist:
            messages.info(request, "Activity doesn't exist.")
            return redirect(reverse("action:index"))

        if activity.owner.id != request.user.id:
            messages.info(request, "You do not have permission to delete this activity.")
        else:
            activity.delete()
            messages.success(request, "You have successfully deleted this activity.")

        return redirect(reverse("action:manage"))
