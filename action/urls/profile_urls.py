from django.urls import path

from action import views

profile_patterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('edit', views.EditProfileView.as_view(), name='edit_profile'),
    path('<int:user_id>', views.ProfileView.as_view(), name='profile'),
]
