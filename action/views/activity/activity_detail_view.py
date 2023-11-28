from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from action.models import Activity
from action import utils


class ActivityDetailView(generic.DetailView):
    """DetailView for displaying details of a specific Activity."""

    model = Activity
    template_name = 'action/activity/detail.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Handle GET requests and render the activity details.

        Returns:
            HttpResponse: Rendered activity details.

        Notes:
            Redirects to the index page with an error message if the Activity is not found.
        """
        try:
            activity_object = self.get_object()
        except Http404:
            messages.error(request, "Activity does not exist.")
            return redirect("action:index")

        context = {
            "activity": activity_object,
            "activity_status": utils.fetch_activity_status(request, self.kwargs['pk'])
        }
        return render(request, self.template_name, context)
