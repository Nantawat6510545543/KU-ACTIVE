from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from action.models import User


def get_profile(request, user_id) -> QuerySet[User]:
    """
    Retrieve the user profile based on the provided user ID or default to the currently authenticated user.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (Optional[int]): The ID of the user to retrieve the profile for,
        or None to use the currently authenticated user.

    Returns:
        Optional[User]: The user profile if found, or None if the user does not exist.
    """
    user_id = user_id or request.user.id  # Set default value to current user

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


def guest_view_their_profile(request, user_id) -> bool:
    """
    Check if a guest is attempting to view their own profile.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (Optional[int]): The ID of the user to check, or None if not specified.

    Returns:
        bool: True if the user is a guest attempting to view their own profile, False otherwise.
    """
    # Get the current user profile, but guests don't have profiles
    return user_id is None and request.user.id is None


class ProfileDetailView(generic.ListView):
    """View for displaying user profiles."""

    template_name = 'action/profile/detail.html'
    context_object_name = 'profile'

    def get(self, request: HttpRequest, user_id=None) -> HttpResponse:
        """
        Handle HTTP GET requests to display the user profile.

        Returns:
            HttpResponse: The HTTP response to be returned.

        Notes:
            If the user ID is not provided, the profile of the currently authenticated user is displayed.
            Redirects to the login page if the user is not logged in and attempts to view their own profile.
            Redirects to the index page with a warning message if the user ID is invalid.
        """
        if guest_view_their_profile(request, user_id):
            return redirect('login')

        profile = get_profile(request, user_id)

        if profile is None:  # Case where there's no user profile with that id
            messages.warning(request, "Invalid user id.")
            return redirect('action:index')

        # Normal Case
        context = {self.context_object_name: profile}
        return render(request, self.template_name, context)
