from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse

from action import utils


@login_required
def add_friend(request, friend_id: int):
    """
    Send a friend request to the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user to whom the friend request is sent.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """
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
    """
    Remove the specified user from the friend list.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user to be removed from the friend list.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """
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
    """
    Accept a friend request from the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user who sent the friend request.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """
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
    """
    Decline a friend request from the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user who sent the friend request.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """
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
    """
    Cancel a friend request sent to the specified user.

    Args:
        request (HttpRequest): The HTTP request object.
        friend_id (int): The ID of the user to whom the friend request was sent.

    Returns:
        HttpResponse: The HTTP response to be returned.
    """
    friend_status = utils.fetch_friend_status(request, friend_id)

    if friend_status.request_status == 'Pending' and request.user == friend_status.sender:
        friend_status.delete()
        messages.success(request, "Request cancelled.")
    elif friend_status.is_friend:
        messages.warning(request, "You are already friend with that person.")
    else:
        messages.warning(request, "There is no friend request for that person.")

    return redirect(reverse("action:add_view"))
