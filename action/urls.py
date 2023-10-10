from django.urls import path

from . import views

app_name = 'action'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.profile, name='profile'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]