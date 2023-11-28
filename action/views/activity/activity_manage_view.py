from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from action.models import Activity


class ActivityManageView(LoginRequiredMixin, generic.ListView):
    """View for managing and displaying a list of activities owned by the current user."""

    template_name = 'action/activity/manage.html'
    context_object_name = 'activity_manage_list'

    def get_queryset(self):
        """Return the queryset of activities owned by the current user."""
        return Activity.objects.filter(owner=self.request.user)


@login_required
def delete_activity(request, activity_id: int):
    """
    View for deleting a specific activity owned by the user.

    Args:
        request (HttpRequest): The HTTP request object.
        activity_id (int): The ID of the activity to delete.


    Returns:
        HttpResponse: Redirect response to the activity manage view.
    """
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        messages.info(request, "Activity doesn't exist.")
        return redirect(reverse("action:manage"))

    if activity.owner.id is not request.user.id:
        messages.info(request, "You do not have permission to delete this activity")
    else:
        activity.delete()
        messages.success(request, "You have successfully deleted this activity.")

    return redirect(reverse("action:manage"))
