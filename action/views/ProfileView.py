from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic

from ..models import User
from ..utils import encoder


# TODO refactor to separate file (utils.py + each views/models), especially get_queryset()


class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/profile.html'

    def post(self, request, *args, **kwargs):
        if 'profile_picture' in request.FILES:
            image_file = request.FILES['profile_picture']
            request.user.profile_picture = encoder.image_to_base64(image_file)
            request.user.save()
        return redirect('action:profile')
