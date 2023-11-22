from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from action.models import User


class ProfileView(generic.ListView):
    template_name = 'action/profile/detail.html'
    context_object_name = 'profile'

    def get(self, request: HttpRequest, user_id=None):
        if user_id is None:  # Set default value to current user
            user_id = request.user.id

        try:  # Loading a profile view
            profile = User.objects.get(id=user_id)
            context = {self.context_object_name: profile}
            return render(request, self.template_name, context)

        except User.DoesNotExist:
            # Case where user try to view their profile but not logged in
            if not request.user.is_authenticated:
                return redirect('login')

            # Case where there's no user profile with that id
            messages.warning(request, "Invalid user id.")
            return redirect('action:index')
