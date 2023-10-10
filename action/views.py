from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile, Activity, Participation


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

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
