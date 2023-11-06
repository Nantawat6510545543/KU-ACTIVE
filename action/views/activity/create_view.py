from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from action.forms import ActivityForm


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ActivityForm
    template_name = 'action/activity/create.html'

    def get_initial(self):
        # Set the initial value for the field
        initial = super().get_initial()
        initial['owner'] = self.request.user
        initial['pub_date'] = timezone.now()
        initial['end_date'] = timezone.now() + timedelta(days=1)
        initial['start_date'] = timezone.now() + timedelta(days=2)
        initial['last_date'] = timezone.now() + timedelta(days=3)
        return initial

    def form_valid(self, form):
        messages.success(self.request, 'Activity created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Render the form with errors if it's invalid
        messages.error(self.request,
                       'Activity creation failed. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Define the URL to redirect to on form success
        return reverse('action:index')
