from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from action.forms import ActivityForm
from action.models import Activity


class ActivityEditView(LoginRequiredMixin, generic.UpdateView):
    """View for editing an existing activity."""

    form_class = ActivityForm
    template_name = 'action/activity/edit.html'

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Handle HTTP GET requests to display the form for editing the activity.

        Returns:
            HttpResponse: The HTTP response containing the rendered form.

        Notes:
            Redirects to the index page with an error message if the user does not have permission to edit the activity.
        """
        activity = self.get_object()

        # Check if the current user is the owner of the activity
        if request.user != activity.owner:
            messages.error(request, 'You do not have permission to edit this activity.')
            return redirect('action:index')

        return super().get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        """Retrieve the activity object based on activity_id."""
        return Activity.objects.get(pk=self.kwargs['activity_id'])

    def form_valid(self, form) -> HttpResponse:
        """Render the form with success messages if it's valid."""
        super().form_valid(form)
        form.save()
        messages.success(self.request, 'Activity edited successfully.')
        return redirect(self.get_success_url())

    def form_invalid(self, form) -> HttpResponse:
        """Render the form with errors if it's invalid."""
        messages.error(self.request, 'Activity edit failed. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self) -> str:
        """Define the URL to redirect to on form success."""
        return reverse('action:manage')
