from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.views import generic

from action.models import User


class FriendListView(LoginRequiredMixin, generic.ListView):
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
        user_friend: QuerySet[User] = self.request.user.friends.filter(username__icontains=query)

        return user_friend.distinct()