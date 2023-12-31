from django.urls import path

from action import views

profile_patterns = [
    path('', views.ProfileDetailView.as_view(), name='profile'),
    path('edit', views.ProfileEditView.as_view(), name='edit_profile'),
    path('<int:user_id>', views.ProfileDetailView.as_view(), name='profile'),
]
