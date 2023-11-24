from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from action.models import FriendStatus, User


class FriendView(LoginRequiredMixin, generic.ListView):
    """View for displaying the list of friends for the logged-in user."""

    template_name = 'action/friends/list.html'
    context_object_name = 'friend_list'

    def get_queryset(self):
        """
        Return the queryset of friends for the logged-in user.

        Returns:
            QuerySet: The queryset of friends.
        """
        query = self.request.GET.get('q')
        user_friend = self.request.user.friends

        if query:
            user_friend = user_friend.filter(username__icontains=query)
        return user_friend.distinct()


class AddFriendView(LoginRequiredMixin, generic.ListView):
    """View for displaying a list of users that the logged-in user can add as friends."""

    template_name = 'action/friends/add.html'
    context_object_name = 'friend_add_list'

    def get_queryset(self):
        """
        Return the queryset of users that can be added as friends.

        Returns:
            QuerySet: The queryset of users.
        """
        query = self.request.GET.get('q')
        user = self.request.user

        # Exclude yourself from the list and people you are already friends with
        add_list = User.objects.exclude(id=user.id).exclude(id__in=user.friends)

        add_list = add_list.filter(username__icontains=query)
        return add_list.distinct()

    def get_context_data(self, **kwargs):
        """
        Return pending a request user list.

        Returns:
            dict: context with all pending requests
        """
        context = super().get_context_data(**kwargs)
        pending_request = FriendStatus.objects.filter(
            sender=self.request.user,
            request_status='Pending'
        )

        pending_request_user_list = User.objects.filter(receiver__id__in=pending_request)
        context['pending_request_user_list'] = pending_request_user_list

        return context


class RequestView(LoginRequiredMixin, generic.ListView):
    """View for displaying a list of friend requests received by the logged-in user."""

    template_name = 'action/friends/request.html'
    context_object_name = 'friend_request_list'

    def get_queryset(self):
        """
        Return the queryset of friend requests that are in a 'Pending' state.

        Returns:
            QuerySet: The queryset of friend requests.
        """
        query = self.request.GET.get('q')

        friend_request = FriendStatus.objects.filter(
            receiver=self.request.user,
            request_status='Pending'
        )

        friend_request = friend_request.filter(sender__username__icontains=query)
        return friend_request.distinct()
