from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from action import utils


class DeclineFriendRequestView(LoginRequiredMixin, View):
    """
    Decline a friend request from the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user who sent the friend request.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """

    def get(self, request: HttpRequest, friend_id: int) -> HttpResponse:
        friend_status = utils.fetch_friend_status(request, friend_id)

        if friend_status.is_friend:
            messages.warning(request, "You are already friend with this person.")
        else:
            friend_status.delete()
            messages.success(request, "You have declined this person.")

        return redirect(reverse("action:request_view"))
