from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from ..forms import ActivityForm
from ..models import Activity


class ActivityEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = ActivityForm
    template_name = 'action/edit_activity.html'

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
