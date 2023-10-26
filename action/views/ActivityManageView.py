from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from ..models import Activity


class ActivityManageView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/manage_activity.html'
    context_object_name = 'activity_manage_list'

    def get_queryset(self):
        return Activity.objects.filter(owner=self.request.user)
