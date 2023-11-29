from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.views import generic

from action.models import FriendStatus, User


def get_user_friend_add_list(user: User) -> QuerySet[User]:
    """
    Get a list of users that the specified user can send friend requests to.

    Args:
        user (User): The user for whom to retrieve the friend add list.

    Returns:
        QuerySet[User]: A queryset of users that the specified user can send friend requests to.
    """
    # Exclude yourself from the list and people you are already friends with
    add_list = User.objects.exclude(id=user.id).exclude(id__in=user.friends)
    return add_list

def get_user_pending_request_list(user: User) -> QuerySet[User]:
    """
    Get a list of users who have sent friend requests to the specified user that are pending approval.

    Args:
        user (User): The user for whom to retrieve the pending friend request list.

    Returns:
        QuerySet[User]: A queryset of users who have sent friend requests to the specified user that are pending approval.
    """
    pending_request = FriendStatus.objects.filter(
        receiver=user,
        request_status='Pending'
    )

    pending_request_user_list = User.objects.filter(sender__id__in=pending_request)
    return pending_request_user_list


class AddFriendView(LoginRequiredMixin, generic.ListView):
    """View for displaying a list of users that the logged-in user can add as friends."""

    template_name = 'action/friends/add.html'
    context_object_name = 'friend_add_list'

    def get_queryset(self) -> QuerySet[User]:
        """
        Return the queryset of users that can be added as friends.

        Returns:
            QuerySet: The queryset of users.
        """
        query = self.request.GET.get('q')

        add_list = get_user_friend_add_list(self.request.user)
        return add_list.filter(username__icontains=query).distinct()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
        Return pending a request user list.

        Returns:
            dict: context with all pending requests
        """
        context = super().get_context_data(**kwargs)
        context['pending_request_user_list'] = get_user_pending_request_list(self.request.user)

        return context
