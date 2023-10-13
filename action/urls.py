from django.urls import path

from . import views

app_name = 'action'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:activity_id>/participate/', views.participate,
         name='participate'),
    path('<int:activity_id>/leave/', views.leave,
         name='leave'),
    path('<int:activity_id>/favorite/', views.favorite,
         name='favorite'),
    path('<int:activity_id>/unfavorite/', views.unfavorite,
         name='unfavorite'),
]
