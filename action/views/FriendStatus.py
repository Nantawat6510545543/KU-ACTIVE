from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from ..utils import friend_status_utils as fs_utils


# TODO add check to not allow user to add themselves as friend
@login_required
def add_friend(request, friend_id: int):
    friend_status = fs_utils.fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    else:
        friend_status.request_status = 'Pending'
        friend_status.save()
        messages.success(request, "Request Sent.")

    return redirect(reverse("action:add_view"))


# TODO add check to not allow user to remove themselves as friend
@login_required
def remove_friend(request, friend_id: int):
    friend_status = fs_utils.fetch_friend_status(request, friend_id)

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
    friend_status = fs_utils.fetch_friend_status(request, friend_id)

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
    friend_status = fs_utils.fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    else:
        friend_status.request_status = 'Declined'
        friend_status.save()
        messages.success(request, "You have declined this person.")

    return redirect(reverse("action:request_view"))
