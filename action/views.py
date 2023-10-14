from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone


from .models import Activity, ActivityStatus, FriendStatus, User


class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/profile.html'


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        """
        """
        return Activity.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')


class FriendView(generic.ListView):
    model = User
    template_name = 'action/friends.html'


class AddFriendView(generic.ListView):
    template_name = 'action/friend_add.html'
    context_object_name = 'friend_add_list'

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


class RequestView(generic.ListView):
    template_name = 'action/friend_request.html'
    context_object_name = 'friend_request_list'

    def get_queryset(self):
        return FriendStatus.objects.filter(receiver=self.request.user, request_status='Pending')


# TODO refactor
class DetailView(generic.DetailView):
    model = Activity
    template_name = 'action/detail.html'

    def get_queryset(self):
        """
        Excludes any activity that aren't published yet.
        """
        return Activity.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request,
                           "Activity does not exist or is not published yet.")
            return redirect("action:index")

        context = {
            "activity": self.object,
            "activity_status": fetch_activity_status(request, self.object.id)
        }

        return render(request, self.template_name, context)


@login_required
def participate(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_participated:
        messages.info(request, "You are already participating.")
    else:
        activity_status.is_participated = True
        activity_status.save()
        messages.success(request, "You have successfully participated.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def leave(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_participated:
        activity_status.is_participated = False
        activity_status.save()
        messages.success(request, "You have left this activity.")
    else:
        messages.info(request,
                      "You are not currently participating in this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def favorite(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_favorited:
        messages.info(request, "You have already favorited this activity.")
    else:
        activity_status.is_favorited = True
        activity_status.save()
        messages.success(request, "You have successfully favorited this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def unfavorite(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request, activity_id)

    if activity_status.is_favorited:
        activity_status.is_favorited = False
        activity_status.save()
        messages.success(request, "You have un-favorited this activity.")
    else:
        messages.info(request, "You have not currently favorite this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def fetch_activity_status(request, activity_id: int):
    activity = get_object_or_404(Activity, pk=activity_id)
    user = request.user

    # TODO factor out the activity part
    # if not activity.can_participate():
    #     messages.error(request, "You can't participate in this activity.")
    #     return redirect("action:index")

    try:
        activity_status = ActivityStatus.objects.\
            get(participants=user, activity=activity)

    except ActivityStatus.DoesNotExist:
        activity_status = ActivityStatus.objects.\
            create(participants=user, activity=activity)

    return activity_status


@login_required
def fetch_friend_status(request, friend_id: int) -> FriendStatus:
    user1 = request.user
    user2 = User.objects.get(id=friend_id)

    try:
        friend_status = FriendStatus.objects.\
            get(Q(sender=user1, receiver=user2) | Q(sender=user2, receiver=user1))

    except FriendStatus.DoesNotExist:
        friend_status = FriendStatus.objects.\
            create(sender=user1, receiver=user2)

    return friend_status


# TODO add check to not allow user to add themselves as friend
@login_required
def add_friend(request, friend_id: int):
    friend_status = fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    else:
        friend_status.request_status = 'Pending'
        friend_status.save()
        messages.success(request, "Request Sent")

    return redirect(reverse("action:add_view"))


# TODO add check to not allow user to add themselves as friend
@login_required
def remove_friend(request, friend_id: int):
    friend_status = fetch_friend_status(request, friend_id)

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
    friend_status = fetch_friend_status(request, friend_id)

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
    friend_status = fetch_friend_status(request, friend_id)

    if friend_status.is_friend:
        messages.warning(request, "You are already friend with this person.")
    else:
        friend_status.request_status = 'Declined'
        friend_status.save()
        messages.success(request, "You have declined this person.")

    return redirect(reverse("action:request_view"))
