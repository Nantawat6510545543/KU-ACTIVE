from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views import generic

from action.models import FriendStatus


class FriendRequestView(LoginRequiredMixin, generic.ListView):
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
