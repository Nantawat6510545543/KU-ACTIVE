from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from action import views

from .profile_urls import profile_patterns
from .activity_urls import activity_patterns
from .friends_urls import friends_patterns

app_name = 'action'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('activity/', include(activity_patterns)),
    path('profile/', include(profile_patterns)),
    path('friends/', include(friends_patterns)),
    path('calendar/', views.CalendarView.as_view(), name='calendar')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
