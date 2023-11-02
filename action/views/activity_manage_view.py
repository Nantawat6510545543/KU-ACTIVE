from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic


from action.models import Activity


class ActivityManageView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/manage_activity.html'
    context_object_name = 'activity_manage_list'

    def get_queryset(self):
        return Activity.objects.filter(owner=self.request.user)


@login_required
def delete_activity(request, activity_id: int):
    try:
        activity = Activity.objects.get(id=activity_id)
    except Activity.DoesNotExist:
        messages.info(request, "Activity doesn't exists")
        return redirect(reverse("action:manage"))

    if activity.owner.id is not request.user.id:
        messages.info(request, "You do not have permission to delete this activity")
        return redirect(reverse("action:manage"))

    activity.delete()
    messages.success(request, "You have succesfully deleted this activity.")
    return redirect(reverse("action:manage"))