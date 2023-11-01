from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'action'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/edit', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile'),

    path('friends/', views.FriendView.as_view(), name='friends'),
    path('friends/add/', views.AddFriendView.as_view(), name='add_view'),
    path('friends/requests/', views.RequestView.as_view(), name='request_view'),
    path('friends/add/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('friends/remove/<int:friend_id>/', views.remove_friend, name='remove_friend'),
    path('friends/requests/accept/<int:friend_id>', views.accept_request, name='accept_request'),
    path('friends/requests/decline/<int:friend_id>', views.decline_request, name='decline_request'),

    path('manage/', views.ActivityManageView.as_view(), name='manage'),
    path('create/', views.ActivityCreateView.as_view(), name='create'),
    path('<int:activity_id>/', views.DetailView.as_view(), name='detail'),
    path('edit/<int:activity_id>', views.ActivityEditView.as_view(), name='edit'),
    path('delete/<int:activity_id>', views.delete_activity, name='delete_activity'),

    path('participate/<int:activity_id>', views.participate, name='participate'),
    path('leave/<int:activity_id>', views.leave, name='leave'),
    path('favorite/<int:activity_id>', views.favorite, name='favorite'),
    path('unfavorite/<int:activity_id>', views.unfavorite, name='unfavorite'),

    path('calendar/', views.CalendarView.as_view(), name='calendar')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
