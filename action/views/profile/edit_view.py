from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views import generic

from action.forms import UserEditForm
from action.models import User


class EditProfileView(LoginRequiredMixin, generic.UpdateView):
    form_class = UserEditForm
    template_name = 'action/edit_profile.html'

    def get_object(self):
        return User.objects.get(pk=self.request.user.id)

    def form_valid(self, form):
        super().form_valid(form)

        messages.success(self.request, 'Profile edited successfully.')
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Render the form with errors if it's invalid
        messages.error(self.request,
                       'Profile edit failed. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Define the URL to redirect to on form success
        return reverse('action:profile')
