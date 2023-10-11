from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Activity, Participation, User


@login_required
def profile(request):
    return render(request, 'action/profile.html')


class IndexView(generic.ListView):
    template_name = 'action/index.html'
    context_object_name = 'activity_list'

    def get_queryset(self):
        """
        """
        return Activity.objects.filter(pub_date__lte=timezone.now()
                                       ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Activity
    template_name = 'action/detail.html'

    def get_queryset(self):
        """
        Excludes any activity that aren't published yet.
        """
        return Activity.objects.filter(pub_date__lte=timezone.now())

    # TODO refactor
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(request,
                           "Activity does not exist or is not published yet.")
            return redirect("action:index")

        user = request.user
        has_participated = False
        if user.is_authenticated:
            has_participated = Participation.objects.filter(
                participants=user, activity=self.object).exists()

        context = {"activity": self.object,
                   "has_participated": has_participated}
        return render(request, self.template_name, context)


@login_required
def participate(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    user = request.user

    if not activity.can_participate():
        messages.error(request, "Vote is not allow")
        return redirect("polls:index")

    new_participate, created = Participation.objects.get_or_create(
        participants=user, activity=activity)

    if created:
        messages.success(request, "You have successfully participated.")
    else:
        messages.info(request, "You are already participating.")

    return redirect(reverse("action:detail", args=(activity.id,)))


@login_required
def withdraw(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    user = request.user

    user_has_participated = Participation.objects.filter(
        participants=user, activity=activity).exists()

    if user_has_participated:
        Participation.objects.filter(participants=user,
                                     activity=activity).delete()
        messages.success(request, "You have departed from the activity.")
    else:
        messages.info(request,
                      "You are not currently participating in this activity.")

    return redirect(reverse("action:detail", args=(activity.id,)))
