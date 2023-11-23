from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from action import utils


@login_required
def add_friend(request, friend_id: int):
    friend_status = utils.fetch_friend_status(request, friend_id)

    # Can't use (friend_status.receiver is request.user)
    # Ex: A -> B, A -> C; these two A's are not the same user instances
    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    elif friend_status.sender == request.user and friend_status.request_status == "Pending":
        messages.warning(request, "You have already sent a friend request to that person.")
    elif friend_status.receiver == request.user and friend_status.request_status == "Pending":
        messages.warning(request, "That person have already sent a friend request to you.")
    else:
        friend_status.request_status = "Pending"
        friend_status.save()
        messages.success(request, "Request Sent.")

    return redirect(reverse("action:add_view"))


@login_required
def remove_friend(request, friend_id: int):
    friend_status = utils.fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        friend_status.request_status = None
        friend_status.is_friend = False
        friend_status.save()
        messages.success(request, "This person is no longer friend with you.")
    else:
        messages.warning(request, "This person is not friend with you.")

    return redirect(reverse("action:friends"))


@login_required
def accept_request(request, friend_id: int):
    friend_status = utils.fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    else:
        friend_status.request_status = 'Accepted'
        friend_status.is_friend = True
        friend_status.save()
        messages.success(request, "You are now friend with this person.")

    return redirect(reverse("action:request_view"))


@login_required
def decline_request(request, friend_id: int):
    friend_status = utils.fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    else:
        friend_status.request_status = 'Declined'
        friend_status.save()
        messages.success(request, "You have declined this person.")

    return redirect(reverse("action:request_view"))


@login_required
def cancel_request(request, friend_id: int):
    friend_status = utils.fetch_friend_status(request, friend_id)

    if friend_status.request_status == 'Pending':
        friend_status.delete()
        messages.success(request, "Request cancelled.")
    else:
        messages.warning(request, "You have not sent a friend request to that person.")

    return redirect(reverse("action:add_view"))