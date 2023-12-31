from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import CreateView

from action.forms import UserForm


class SignupView(CreateView):
    """View for user registration and authentication."""

    form_class = UserForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """
        Handle the case when the form is valid.

        Args:
            form (UserForm): The user registration form.

        Returns:
            HttpResponseRedirect: Redirects to the success URL.
        """
        super().form_valid(form)

        username = form.cleaned_data.get('username')
        raw_passwd = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_passwd)
        login(self.request, user)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        """
        Handle the case when the form is invalid.

        Args:
            form (UserForm): The user registration form.

        Returns:
            HttpResponse: Render the registration page with errors.
        """
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        Get the success URL after a successful registration.

        Returns:
            str: The success URL.
        """
        return reverse('action:index')  # Set the success URL
