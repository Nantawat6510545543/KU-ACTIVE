from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from decouple import config
import pyrebase

from .forms import ActivityForm
from .models import Activity, ActivityStatus, FriendStatus, User
from .utils import fetch_activity_status, fetch_friend_status, \
    get_index_queryset

firebase = pyrebase.initialize_app({
    "apiKey": config('FIREBASE_API_KEY'),
    "authDomain": config('FIREBASE_AUTH_DOMAIN'),
    "projectId": config('FIREBASE_PROJECT_ID'),
    "storageBucket": config('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": config('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": config('FIREBASE_APP_ID'),
    "measurementId": config('FIREBASE_MEASUREMENT_ID'),
    "databaseURL": config('FIREBASE_DATABASE_URL')
})

storage = firebase.storage()


# TODO refactor to separate file (utils.py + each views/models), especially get_queryset()

class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/profile.html'

    def post(self, request, *args, **kwargs):
        if 'profile_picture' in request.FILES:
            username = request.user.username
            image_file = request.FILES['profile_picture']
            storage.child(f"Profile_picture/{username}").put(image_file)
            file_url = storage.child(f"Profile_picture/{username}").get_url(
                None)
            request.user.profile_picture = file_url
            request.user.save()
        return redirect('action:profile')


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        return get_index_queryset(self.request)


class ActivityCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = ActivityForm
    template_name = 'action/create_activity.html'

    def form_valid(self, form):
        # Save the form and redirect to the index on success
        messages.success(self.request, 'Activity created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        # Render the form with errors if it's invalid
        messages.error(self.request,
                       'Activity creation failed. Please check the form.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Define the URL to redirect to on form success
        return reverse('action:index')


class FriendView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/friends.html'


class AddFriendView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/friend_add.html'
    context_object_name = 'friend_add_list'

    def get_queryset(self):
        return User.objects.exclude(username=self.request.user)


class RequestView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/friend_request.html'
    context_object_name = 'friend_request_list'

    def get_queryset(self):
        return FriendStatus.objects.filter(receiver=self.request.user,
                                           request_status='Pending')


class DetailView(generic.DetailView):
    template_name = 'action/detail.html'

    def get(self, request, *args, **kwargs):
        try:
            self.pk = self.kwargs['pk']
            context = {
                "activity": Activity.objects.get(pk=self.pk),
                "activity_status": fetch_activity_status(request, self.pk)
            }
            return render(request, self.template_name, context)

        except Activity.DoesNotExist:
            messages.error(request,
                           "Activity does not exist or is not published yet.")
            return redirect("action:index")


@login_required
def participate(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request,
                                                            activity_id)

    if activity_status.is_participated:
        messages.info(request, "You are already participating.")
    else:
        activity_status.is_participated = True
        activity_status.save()
        messages.success(request, "You have successfully participated.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def leave(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request,
                                                            activity_id)

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
    activity_status: ActivityStatus = fetch_activity_status(request,
                                                            activity_id)

    if activity_status.is_favorited:
        messages.info(request, "You have already favorited this activity.")
    else:
        activity_status.is_favorited = True
        activity_status.save()
        messages.success(request,
                         "You have successfully favorited this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


@login_required
def unfavorite(request, activity_id: int):
    activity_status: ActivityStatus = fetch_activity_status(request,
                                                            activity_id)

    if activity_status.is_favorited:
        activity_status.is_favorited = False
        activity_status.save()
        messages.success(request, "You have un-favorited this activity.")
    else:
        messages.info(request,
                      "You have not currently favorite this activity.")

    return redirect(reverse("action:detail", args=(activity_id,)))


# TODO add check to not allow user to add themselves as friend
@login_required
def add_friend(request, friend_id: int):
    friend_status = fetch_friend_status(request, friend_id)

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
