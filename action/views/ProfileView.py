from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic

from ..models import User
from ..utils import firebase_utils as fs_utils


# TODO refactor to separate file (utils.py + each views/models), especially get_queryset()
class ProfileView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = 'action/profile.html'

    def post(self, request, *args, **kwargs):
        if 'profile_picture' in request.FILES:
            user = request.user
            storage = fs_utils.get_firebase_instance().storage()
            image_file = request.FILES['profile_picture']
            image_name = f"{user.username}{user.id}"
            storage.child(f"Profile_picture/{image_name}").put(image_file)
            file_url = storage.child(f"Profile_picture/{image_name}").get_url(
                None)
            request.user.profile_picture = file_url
            request.user.save()
        return redirect('action:profile')
