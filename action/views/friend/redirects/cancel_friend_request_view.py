from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.http import HttpRequest, HttpResponse
from action import utils


class CancelFriendRequestView(LoginRequiredMixin, View):
    """
    Cancel a friend request sent to the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user to whom the friend request was sent.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """

    def get(self, request: HttpRequest, friend_id: int) -> HttpResponse:
        friend_status = utils.fetch_friend_status(request, friend_id)

        if friend_status.request_status == 'Pending' and request.user == friend_status.sender:
            friend_status.delete()
            messages.success(request, "Request cancelled.")
        elif friend_status.is_friend:
            messages.warning(request, "You are already friends with that person.")
        else:
            messages.warning(request, "There is no friend request for that person.")

        return redirect(reverse("action:add_view"))
