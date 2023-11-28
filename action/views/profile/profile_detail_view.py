from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from action.models import User


class ProfileDetailView(generic.ListView):
    """View for displaying user profiles."""

    template_name = 'action/profile/detail.html'
    context_object_name = 'profile'

    def get(self, request: HttpRequest, user_id=None):
        """
        Handle HTTP GET requests to display the user profile.

        Returns:
            HttpResponse: The HTTP response to be returned.

        Notes:
            If the user ID is not provided, the profile of the currently authenticated user is displayed.
            Redirects to the login page if the user is not logged in and attempts to view their own profile.
            Redirects to the index page with a warning message if the user ID is invalid.
        """
        if user_id is None:  # Set default value to current user
            user_id = request.user.id

        try:  # Loading a profile view
            profile = User.objects.get(id=user_id)
            context = {self.context_object_name: profile}
            return render(request, self.template_name, context)

        except User.DoesNotExist:
            # Case where user try to view their profile but not logged in
            if not request.user.is_authenticated:
                return redirect('login')

            # Case where there's no user profile with that id
            messages.warning(request, "Invalid user id.")
            return redirect('action:index')
