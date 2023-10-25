from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from ..models import FriendStatus, User


class FriendView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/friends.html'


class AddFriendView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/friends_add.html'
    context_object_name = 'friend_add_list'

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


class RequestView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/friends_request.html'
    context_object_name = 'friend_request_list'

    def get_queryset(self):
        return FriendStatus.objects.filter(receiver=self.request.user,
                                           request_status='Pending')
