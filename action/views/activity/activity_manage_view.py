from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views import generic

from action.models import Activity


class ActivityManageView(LoginRequiredMixin, generic.ListView):
    """View for managing and displaying a list of activities owned by the current user."""

    template_name = 'action/activity/activity_manage.html'
    context_object_name = 'activity_manage_list'

    def get_queryset(self) -> QuerySet[Activity]:
        """Return the queryset of activities owned by the current user."""
        return Activity.objects.filter(owner=self.request.user)
