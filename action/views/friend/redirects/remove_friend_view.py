from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from action import utils


class RemoveFriendView(LoginRequiredMixin, View):
    """
    Remove the specified user from the friend list.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user to be removed from the friend list.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """

    def get(self, request: HttpRequest, friend_id: int) -> HttpResponse:
        friend_status = utils.fetch_friend_status(request, friend_id)

        if friend_status.is_friend:
            friend_status.request_status = None
            friend_status.is_friend = False
            friend_status.save()
            messages.success(request, "This person is no longer friend with you.")
        else:
            messages.warning(request, "This person is not friend with you.")

        return redirect(reverse("action:friends"))
