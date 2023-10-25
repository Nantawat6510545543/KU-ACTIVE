from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic

from ..models import Activity
from ..utils import activity_status_utils as asu


class DetailView(generic.DetailView):
    template_name = 'action/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.pk = self.kwargs['pk']
            context = {
                "activity": Activity.objects.get(pk=self.pk),
                "activity_status": asu.fetch_activity_status(request, self.pk)
            }
            return render(request, self.template_name, context)

        except Activity.DoesNotExist:
            messages.error(request,
                           "Activity does not exist or is not published yet.")
            return redirect("action:index")



