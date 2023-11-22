from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from action.models import User


class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/profile/detail.html'
    context_object_name = 'profile'

    def get(self, request: HttpRequest, user_id=None):
        if user_id is None:  # Set default value to current user
            user_id = request.user.id

        try:
            profile = User.objects.get(id=user_id)
            context = {self.context_object_name: profile}
            return render(request, self.template_name, context)

        except User.DoesNotExist:
            messages.warning(request, "Invalid user id.")
            return redirect('action:index')