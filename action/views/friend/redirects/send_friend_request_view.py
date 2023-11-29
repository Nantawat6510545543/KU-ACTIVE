from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from action import utils


class SendFriendRequestView(LoginRequiredMixin, View):
    """
    Send a friend request to the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user to whom the friend request is sent.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """

    def get(self, request: HttpRequest, friend_id: int) -> HttpResponse:
        friend_status = utils.fetch_friend_status(request, friend_id)

        if friend_status.is_friend:
            messages.warning(request, "You are already friend with this person.")
        elif friend_status.sender == request.user and friend_status.request_status == "Pending":
            messages.warning(request, "You have already sent a friend request to that person.")
        elif friend_status.receiver == request.user and friend_status.request_status == "Pending":
            messages.warning(request, "That person has already sent a friend request to you.")
        else:
            friend_status.request_status = "Pending"
            friend_status.save()
            messages.success(request, "Request Sent.")

        return redirect(reverse("action:add_view"))
