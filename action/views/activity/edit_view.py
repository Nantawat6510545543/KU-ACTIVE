from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from action.forms import ActivityForm
from action.models import Activity


class ActivityEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = ActivityForm
    template_name = 'action/activity/edit.html'

    def get(self, request, *args, **kwargs):
        # Get the activity object
        activity = self.get_object()

        # Check if the current user is the owner of the activity
        if request.user != activity.owner:
            messages.error(request, 'You do not have permission to edit this activity.')
            return redirect('action:index')

        return super().get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        return Activity.objects.get(pk=self.kwargs['activity_id'])

    def form_valid(self, form):
        super().form_valid(form)
        form.save()
        messages.success(self.request, 'Activity edited successfully.')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Render the form with errors if it's invalid
        messages.error(self.request,
                       'Activity edit failed. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Define the URL to redirect to on form success
        return reverse('action:manage')
