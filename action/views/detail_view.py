from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic

from ..models import Activity
from .. import utils


class DetailView(generic.DetailView):
    template_name = 'action/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            activity_id = self.kwargs['activity_id']
            context = {
                "activity": Activity.objects.get(pk=activity_id),
                "activity_status": utils.fetch_activity_status(request,
                                                               activity_id)
            }
            return render(request, self.template_name, context)

        except Activity.DoesNotExist:
            messages.error(request,
                           "Activity does not exist or is not published yet.")
            return redirect("action:index")
