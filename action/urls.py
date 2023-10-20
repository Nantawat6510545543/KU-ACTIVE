from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

app_name = 'action'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.ActivityCreateView.as_view(), name='create'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('friends/', views.FriendView.as_view(), name='friends'),
    path('friends/add/', views.AddFriendView.as_view(), name='add_view'),
    path('friends/requests/', views.RequestView.as_view(),
         name='request_view'),
    path('friends/add/<int:friend_id>/', views.add_friend, name='add_friend'),
    path('friends/remove/<int:friend_id>/', views.remove_friend,
         name='remove_friend'),
    path('friends/requests/accept/<int:friend_id>', views.accept_request,
         name='accept_request'),
    path('friends/requests/decline/<int:friend_id>', views.decline_request,
         name='decline_request'),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:activity_id>/participate/', views.participate,
         name='participate'),
    path('<int:activity_id>/leave/', views.leave,
         name='leave'),
    path('<int:activity_id>/favorite/', views.favorite,
         name='favorite'),
    path('<int:activity_id>/unfavorite/', views.unfavorite,
         name='unfavorite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
