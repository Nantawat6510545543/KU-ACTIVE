from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic
import base64

from ..models import User
from ..utils import encoder


# TODO refactor to separate file (utils.py + each views/models), especially get_queryset()
def post(request):
    if 'profile_picture' in request.FILES:
        image_file = request.FILES['profile_picture']
        request.user.profile_picture = encoder.image_to_base64(image_file)
        request.user.save()
    return redirect('action:profile')


class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/profile.html'
