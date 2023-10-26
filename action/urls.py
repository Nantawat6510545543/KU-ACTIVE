from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    Activity,
    ActivityCreateView,
    ActivityEditView,
    ActivityManageView,
    DetailView,
    EditProfileView,
    FriendStatus,
    FriendView,
    IndexView,
    ProfileView,
)

app_name = 'action'

urlpatterns = [
    path('', IndexView.IndexView.as_view(), name='index'),
    path('profile/', ProfileView.ProfileView.as_view(), name='profile'),
    path('profile/edit', EditProfileView.EditProfileView.as_view(), name='edit_profile'),

    path('friends/', FriendView.FriendView.as_view(), name='friends'),
    path('friends/add/', FriendView.AddFriendView.as_view(), name='add_view'),
    path('friends/requests/', FriendView.RequestView.as_view(), name='request_view'),
    path('friends/add/<int:friend_id>/', FriendStatus.add_friend, name='add_friend'),
    path('friends/remove/<int:friend_id>/', FriendStatus.remove_friend, name='remove_friend'),
    path('friends/requests/accept/<int:friend_id>', FriendStatus.accept_request, name='accept_request'),
    path('friends/requests/decline/<int:friend_id>', FriendStatus.decline_request, name='decline_request'),

    path('manage/', ActivityManageView.ActivityManageView.as_view(), name='manage'),
    path('create/', ActivityCreateView.ActivityCreateView.as_view(), name='create'),
    path('<int:pk>/', DetailView.DetailView.as_view(), name='detail'),
    path('edit/<int:activity_id>', ActivityEditView.ActivityEditView.as_view(), name='edit'),

    path('<int:activity_id>/participate/', Activity.participate, name='participate'),
    path('<int:activity_id>/leave/', Activity.leave, name='leave'),
    path('<int:activity_id>/favorite/', Activity.favorite, name='favorite'),
    path('<int:activity_id>/unfavorite/', Activity.unfavorite, name='unfavorite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
