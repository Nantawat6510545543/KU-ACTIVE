from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views import generic

from action.models import User
from action import utils


# TODO refactor to separate file (utils.py + each views/models), especially get_queryset()

# TODO try get_context_data()?
class ProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'action/profile.html'
    context_object_name = 'profile'

    def get(self, request: HttpRequest, user_id=None):
        # Set default value to current user
        if user_id is None:
            user_id = request.user.id

        try:
            profile = User.objects.get(id=user_id)
            context = {self.context_object_name: profile}
            return render(request, self.template_name, context)

        except User.DoesNotExist:
            messages.warning(request, "Invalid user id.")
            return redirect('action:index')

    def post(self, request, *args, **kwargs):
        if 'profile_picture' in request.FILES:
            image_file = request.FILES['profile_picture']
            request.user.profile_picture = utils.image_to_base64(image_file)
            request.user.save()
        return redirect('action:profile')
